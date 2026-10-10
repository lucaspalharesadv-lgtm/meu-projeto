# -*- coding: utf-8 -*-
"""Base nova (500) - parceria / associado / correspondencia.
Deduplica contra a base antiga de 400 e contra a lista 'outros'.
add() recebe DICTS (evita o bug de ordem de tupla da rodada anterior)."""
import csv, json, os
from collections import Counter
import dns.resolver

BASE = "/home/user/meu-projeto/prospeccao_juridica"
OLD = f"{BASE}/PROSPECCAO_JURIDICA_BRASIL.csv"
P = f"{BASE}/PARCERIAS_ASSOCIADO_500.csv"
OUT = f"{BASE}/outros_emails_capturados.csv"
MXC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estado", "mx_cache.json")

COLS = ["ID", "Escritorio/Empresa", "Nome do contato", "E-mail", "Confirmacao", "Tipo de e-mail",
        "Modelo de ganho", "Atuacao remota", "Areas de atuacao", "Cidade", "Estado", "Regiao",
        "Tipo de oportunidade", "Fonte (link)", "Prioridade", "Dominio valido (MX)", "Observacao"]
OCOLS = ["E-mail", "Nome", "Contexto", "Cidade", "Estado", "Fonte (link)", "Motivo de nao entrar nos 500"]
REG = {"AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte", "RO": "Norte", "RR": "Norte", "TO": "Norte",
       "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste", "PB": "Nordeste", "PE": "Nordeste",
       "PI": "Nordeste", "RN": "Nordeste", "SE": "Nordeste", "DF": "Centro-Oeste", "GO": "Centro-Oeste",
       "MT": "Centro-Oeste", "MS": "Centro-Oeste", "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste",
       "SP": "Sudeste", "PR": "Sul", "RS": "Sul", "SC": "Sul", "BR": "Nacional"}
WEBMAIL = {"gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br", "yahoo.com", "live.com", "uol.com.br",
           "bol.com.br", "terra.com.br", "icloud.com", "hotmail.com.br", "outlook.com.br", "ig.com.br"}

for path, cols in ((P, COLS), (OUT, OCOLS)):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:
            csv.writer(fh).writerow(cols)

_mx = json.load(open(MXC)) if os.path.exists(MXC) else {}


import threading as _th
_mxlock = _th.Lock()
_DOH = ("https://dns.google/resolve", "https://cloudflare-dns.com/dns-query")


def _doh(dom, typ):
    """Consulta DNS por HTTPS (o DNS local deste ambiente nao responde MX). Nao envia nada ao dominio.
    Devolve 'ok', 'nx', 'vazio' ou None (falha da consulta)."""
    import requests
    for u in _DOH:
        try:
            r = requests.get(u, params={"name": dom, "type": typ}, headers={"accept": "application/dns-json"},
                             timeout=15, verify="/root/.ccr/ca-bundle.crt")
            j = r.json()
        except Exception:
            continue
        if j.get("Status") == 3:
            return "nx"
        if j.get("Status") != 0:
            continue
        ans = [a for a in j.get("Answer", []) if a.get("type") == (15 if typ == "MX" else 1)]
        if typ == "MX":
            ans = [a for a in ans if a.get("data", "").split()[-1:] not in (["."], [])]   # MX nulo (RFC 7505) nao conta
        return "ok" if ans else "vazio"
    return None


def mx(email):
    dom = email.split("@", 1)[1].lower()
    if dom in _mx:
        return _mx[dom]
    if os.environ.get("MX_DOH", "1") == "1":
        st = _doh(dom, "MX")
        if st == "ok":
            v = "MX ok (webmail)" if dom in WEBMAIL else "MX ok"
        elif st == "nx":
            v = "DOMINIO INEXISTENTE"
        elif st == "vazio":
            v = "Sem MX (so A) - risco" if _doh(dom, "A") == "ok" else "SEM MX E SEM A"
        else:
            return "Falha na consulta"
        with _mxlock:
            _mx[dom] = v
            with open(MXC + ".tmp", "w") as fh:
                json.dump(_mx, fh)
            os.replace(MXC + ".tmp", MXC)
        return v
    r = dns.resolver.Resolver()
    r.lifetime = r.timeout = 8
    try:
        ans = r.resolve(dom, "MX")
        v = "MX ok (webmail)" if dom in WEBMAIL else "MX ok"
    except dns.resolver.NXDOMAIN:
        v = "DOMINIO INEXISTENTE"
    except dns.resolver.NoAnswer:
        try:
            r.resolve(dom, "A")
            v = "Sem MX (so A) - risco"
        except Exception:
            v = "SEM MX E SEM A"
    except Exception as e:
        v = "Falha na consulta"
    if v == "Falha na consulta":
        import time
        time.sleep(2)
        try:
            r.lifetime = r.timeout = 15
            r.resolve(dom, "MX")
            v = "MX ok (webmail)" if dom in WEBMAIL else "MX ok"
        except dns.resolver.NXDOMAIN:
            v = "DOMINIO INEXISTENTE"
        except Exception:
            return "Falha na consulta"          # nao memoriza falha momentanea
    _mx[dom] = v
    with open(MXC, "w") as fh:
        json.dump(_mx, fh)
    return v


def seen_all():
    s = set()
    for path in (OLD, P, OUT):
        if os.path.exists(path):
            rows = list(csv.reader(open(path, encoding="utf-8-sig")))
            if not rows:
                continue
            idx = rows[0].index("E-mail")
            s |= {r[idx].strip().lower() for r in rows[1:] if len(r) > idx}
    return s


import re as _re
# Escritorios que o usuario pediu para ignorar (nunca incluir em nenhuma lista)
BLOQUEADOS = _re.compile(r"\bmbt\b|mbtadvoca|mbtadvogados|ernesto ?borges|ernestoborges|pessoa ?(&|e) ?pessoa|pessoaepessoa", _re.I)


def add(items):
    """items: lista de dicts com chaves:
       org, contato, email, conf, tipo, modelo, remoto, areas, cidade, uf, oport, fonte, prior, obs"""
    rows = list(csv.reader(open(P, encoding="utf-8-sig")))
    h, b = rows[0], rows[1:]
    seen = seen_all()
    novos, dup = 0, []
    for d in items:
        e = d["email"].strip().lower()
        if BLOQUEADOS.search(e + " " + d.get("org", "") + " " + d.get("fonte", "")):
            continue
        if not e or e in seen:
            dup.append(e)
            continue
        seen.add(e)
        novos += 1
        uf = d.get("uf", "BR") or "BR"
        b.append(["", d["org"], d.get("contato", ""), e, d.get("conf", "Confirmado"), d.get("tipo", ""),
                  d.get("modelo", ""), d.get("remoto", "Nao informado"), d.get("areas", ""), d.get("cidade", ""),
                  uf, REG.get(uf, "Nacional"), d.get("oport", ""), d["fonte"], d.get("prior", "Media"),
                  mx(e), d.get("obs", "")])
    ordem = {"Norte": 0, "Nordeste": 1, "Centro-Oeste": 2, "Sudeste": 3, "Sul": 4, "Nacional": 5}
    pord = {"Alta": 0, "Media": 1, "Baixa": 2}
    b.sort(key=lambda r: (ordem.get(r[11], 9), r[10], pord.get(r[14], 9), r[1].lower()))
    for i, r in enumerate(b, 1):
        r[0] = f"{i:03d}"
    tmp = P + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(h)
        w.writerows(b)
        fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, P)
    print(f"+{novos} novos | TOTAL: {len(b)} | dup/ja existentes: {len(dup)}")
    print("  regiao:", dict(Counter(r[11] for r in b)))
    print("  prioridade:", dict(Counter(r[14] for r in b)), "| modelo:", dict(Counter(r[6] for r in b)))
    bad = [r[3] for r in b if not r[15].startswith("MX ok")]
    if bad:
        print("  ATENCAO MX:", bad[-10:])
    return novos


def outros(items):
    """Guarda e-mails capturados que NAO contam para os 500 (ex.: advogado buscando emprego)."""
    rows = list(csv.reader(open(OUT, encoding="utf-8-sig")))
    seen = seen_all()
    n = 0
    for d in items:
        e = d["email"].strip().lower()
        if e in seen:
            continue
        seen.add(e)
        n += 1
        rows.append([e, d.get("nome", ""), d.get("ctx", "")[:300], d.get("cidade", ""), d.get("uf", ""),
                     d["fonte"], d.get("motivo", "")])
    with open(OUT + ".tmp", "w", newline="", encoding="utf-8-sig") as fh:
        csv.writer(fh).writerows(rows); fh.flush(); os.fsync(fh.fileno())
    os.replace(OUT + ".tmp", OUT)
    print(f"outros: +{n} (total {len(rows) - 1})")
