#!/usr/bin/env python3
"""Coletor de contatos INSTITUCIONAIS de orgaos publicos.

Entrada (emails/publico/urls/):
  *.txt          URL<TAB>ORGAO<TAB>UF<TAB>CIDADE<TAB>DETALHE
  *_emails.tsv   EMAIL<TAB>URL<TAB>ORGAO<TAB>CARGO_SETOR<TAB>UF<TAB>CIDADE
Saida: emails/publico/resultado_publico.csv

Regras: so caixas publicadas pelo proprio orgao e ligadas a cargo/setor; nada de webmail pessoal,
ouvidoria, imprensa, LGPD, e-SIC; dominio com MX; em Ji-Parana so contatos gerais (RH, protocolo,
secretaria), nunca gestores; no maximo 5 por dominio.
"""
import csv, glob, html, os, re, ssl, sys, json, datetime, urllib.parse, urllib.request, concurrent.futures as cf
from collections import Counter
import dns.resolver

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = f"{HERE}/publico"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}")
FREE = {"gmail.com","hotmail.com","outlook.com","yahoo.com","yahoo.com.br","uol.com.br","bol.com.br","live.com","icloud.com",
        "terra.com.br","ig.com.br","msn.com","globo.com","r7.com","outlook.com.br","hotmail.com.br"}
BAD_DOM = {"example.com","email.com","sentry.io","wixpress.com","seudominio.com.br","dominio.com.br","exemplo.com.br","w3.org","schema.org"}
BAD_EXT = (".png",".jpg",".jpeg",".gif",".webp",".svg",".css",".js",".pdf",".woff",".woff2",".ico")
BAD_LOCAL = ("ouvidoria","imprensa","comunicacao","assessoriadeimprensa","asscom","lgpd","dpo","privacidade","esic","e-sic","sic@",
             "transparencia","denuncia","corregedoria","suporte","helpdesk","sac","webmaster","noreply","no-reply","donotreply",
             "postmaster","abuse","seuemail","exemplo","teste","contato.ti","cpd@","informatica","sistemas","ti@")
SUBPATHS = ("contato","fale-conosco","contatos","institucional/contato")
JIPA = re.compile(r"ji[\s\-]?paran[aá]", re.I)
BADSETOR = re.compile(
    r"estagi|distribu|f[oó]rum digital|\bfd[a-z]{4,}|gex[a-z]{2,3}@|ger[eê]ncia.executiva|superintend[eê]ncia regional|cart[oó]rio|"
    r"biblioteca|plant[aã]o|cejusc|hospitalar|ambulat|escola|esmaf|\beje\b|eje@|museu|cerimonial|eventos|discente|vestibular|"
    r"divis[aã]o de capta|dicap|corregedoria|inteligencia|casamilitar|defesacivil|datasus|agenda|atend\.?judicial|apoiosaab|canais|"
    r"inscri|seadi|auditoria|secom|arquivo|recepcao|crs(leste|sul|norte|oeste|centro)|gabinetesaude|(^|[._-])ti([._@-]|$)|diretoria\.saude|falecom|procuradoriadamulher|rtv@|dio@|esesp|informacao|ouv",
    re.I)
TARGET = 600
FIRSTNAMES = set("""alan alex alexandre ana andre andrea angela antonio augusto beatriz bruno camila carlos carolina claudia claudio cristiano daniel daniela david debora diego edilson edson eduardo elaine elisa eurico fabio fabiana felipe fernanda fernando flavio francisco gabriel gabriela gustavo helena henrique igor isabela jorge jose joao julia juliana julio larissa leandro leonardo lucas luciana luis luiz marcelo marcello marcia marcio marco marcos maria mariana mario mauricio miguel monica nadja nereida natalia nelson patricia paulo pedro rafael rafaela renata ricardo roberto rodrigo rogerio ronaldo sandra sergio silvia simone sonia tereza thiago vanessa vicente victor vinicius vitor wagner walter wilson guilherme""".split())
SURNAMES = set("calazans badaro moraes esteves terto vicentini pessoa mendes barroso fux gilmar toffoli lewandowski zanin dino cristianozanin".split())
PERSON_PREFIX = re.compile(r"^(sen|dep|ver|des|min|juiz|prom|cons)[._-]|conselheir|desembargador|ministro\b|procuradoreu", re.I)
GENERIC = set("gabinete presidencia vice secretaria geral protocolo juridico juridica procuradoria consultoria diretoria gestao pessoas pessoal rh recursos humanos folha atendimento administracao administrativo assessoria assessor chefia chefe sgp dgp segep sead seplag casa civil contato fale conosco legislativo legislativa executivo procurador procuradora adjunto adjunta subprocuradoria subchefia".split())
def is_person(local):
    if PERSON_PREFIX.search(local): return True
    toks = [t for t in re.split(r"[._\-]", local) if t]
    for t in toks:
        if t in SURNAMES or any(t.startswith(sn) and len(sn) >= 8 for sn in SURNAMES): return True
        if t in FIRSTNAMES and len(toks) > 1: return True
        for fn in FIRSTNAMES:
            if len(fn) >= 5 and len(t) > len(fn) and (t.startswith(fn) or t.endswith(fn)): return True
    if len(toks) == 2 and all(t.isalpha() and len(t) >= 4 for t in toks) and not any(t in GENERIC for t in toks): return True
    m = re.match(r"^gab([a-z]{4,})$", local)
    if m and not local.startswith("gabinete") and m.group(1) not in ("sgp","dg","pres","presidencia","vice","pc","secretaria") and not any(g in m.group(1) for g in GENERIC): return True
    return False
VARA = re.compile(r"vara|fr[uo]m|forum|comarca|juizado|promotoria|jvd|vepma|criminal|execucao|cartorio", re.I)

def get(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        raw = r.read(1_500_000)
        return raw.decode(r.headers.get_content_charset() or "utf-8", errors="ignore")

def cf_decode(h):
    try:
        b = bytes.fromhex(h); k = b[0]
        return "".join(chr(x ^ k) for x in b[1:])
    except Exception:
        return ""

def deob(t):
    for m in re.finditer(r'data-cfemail="([0-9a-fA-F]+)"|email-protection#([0-9a-fA-F]+)', t):
        d = cf_decode(m.group(1) or m.group(2))
        if "@" in d: t += " " + d
    t = html.unescape(t)
    t = re.sub(r"\s*[\[\(]\s*(?:at|arroba)\s*[\]\)]\s*", "@", t, flags=re.I)
    t = re.sub(r"\s*\(\s*ponto\s*\)\s*", ".", t, flags=re.I)
    return re.sub(r"mailto:", " ", t, flags=re.I)

def clean(e):
    e = re.sub(r"^(?:u003[ce]|x3[ce]|&gt;|&lt;)+", "", e.strip().lower())
    e = e.strip(".,;:-_%+").lower()
    if e.endswith(BAD_EXT): return None
    local, _, dom = e.partition("@")
    if not local or dom in FREE or dom in BAD_DOM or ".." in e or len(local) > 45: return None
    if any(b in local for b in BAD_LOCAL): return None
    return e

def root(host):
    p = host.lower().removeprefix("www.").split(".")
    return ".".join(p[-3:]) if len(p) >= 3 and p[-2] in ("gov","jus","leg","mp","def","tc","edu","org","com","net") else ".".join(p[-2:])

def scrape(url):
    """devolve (emails_na_pagina, texto_menciona_jiparana)"""
    p = urllib.parse.urlparse(url if "//" in url else "https://" + url)
    base = f"{p.scheme}://{p.netloc}"
    found, jip = set(), False
    for u in [url] + [f"{base}/{s}" for s in SUBPATHS]:
        try: t = get(u)
        except Exception: continue
        jip = jip or bool(JIPA.search(t))
        for e in EMAIL_RE.findall(deob(t)):
            e = clean(e)
            if e: found.add(e)
        if len(found) >= 12: break
    return found, jip

_mx = {}
def mx_ok(d):
    if d not in _mx:
        try: dns.resolver.resolve(d, "MX", lifetime=6); _mx[d] = True
        except Exception:
            try: dns.resolver.resolve(d, "A", lifetime=6); _mx[d] = True
            except Exception: _mx[d] = False
    return _mx[d]

def tipo(local, cargo=""):
    s = (local + " " + cargo).lower()
    if re.search(r"(^|[^a-z])(rh|gdp|dgp|sgp|dp)([^a-z]|$)|pessoa|recursos.?humanos|recrut|selec|folha|pessoal|talento|gente", s): return "RH/Pessoas"
    if re.search(r"juridic|procurador|consultoria|advocacia|assessoria.?jur|contencios", s): return "Juridico/Procuradoria"
    if re.search(r"gabinete|chefia|presid|diretoria|dirgeral|secretaria.?geral|secretario|vice", s): return "Gabinete/Chefia"
    if re.search(r"protocolo|secretaria|atendimento|administra|recepcao|expediente|geral|contato|faleconosco|fale", s): return "Secretaria/Protocolo"
    return "Nominal (cargo)"

UFS = "ac al am ap ba ce df es go ma mg ms mt pa pb pe pi pr rj rn ro rr rs sc se sp to".split()
def rotulo_dominio(dom):
    lab = dom.split(".")[0].lower(); sfx = dom.lower()
    m = re.match(r"^(tj|tre|mp|dpe|pge|tce|cge|al|tjm)-?([a-z]{2})$", lab)
    uf = m.group(2) if m and m.group(2) in UFS else ""
    nomes = {"tj": "Tribunal de Justiça", "tre": "TRE", "mp": "Ministério Público", "dpe": "Defensoria Pública", "pge": "PGE", "tce": "TCE", "cge": "CGE", "al": "Assembleia Legislativa", "tjm": "TJM"}
    if m: return (f"{nomes[m.group(1)]} {uf.upper()}", uf.upper())
    m = re.match(r"^(trt|trf)(\d+)?$", lab)
    if m: return (f"{m.group(1).upper()}{'-' + m.group(2) + 'ª Região' if m.group(2) else ''}", "")
    return (lab.upper(), "")

def categoria_por_dominio(dom, cat):
    d = dom.lower()
    if d.endswith(".jus.br"):
        return "judiciario_federal" if re.match(r"^(trf|trt|tre|tst|tse|stj|stf|stm|cnj|cjf)", d.split(".")[0]) else "judiciario_estadual"
    if d.endswith(".mp.br") or d.endswith(".def.br"): return "mp_defensorias"
    return cat

def esfera(orgao, uf):
    o = orgao.lower()
    if re.search(r"municipal|prefeitura|munic[ií]pio|c[aâ]mara municipal", o): return "municipal"
    if uf in ("", "BR") or re.search(r"federal|uni[aã]o|nacional|supremo|superior|senado|c[aâ]mara dos deputados|minist[eé]rio|agu\b|cgu\b|tcu\b|stf|stj|tst|tse|stm|cnj|cnmp|dpu|trf|trt|tre-|ifro|inss|caixa|petrobras|correios", o): return "federal"
    return "estadual"

def main():
    meta, agent_rows, order = {}, [], []     # meta[url] = dict
    for f in sorted(glob.glob(f"{PUB}/urls/*.txt")):
        cat = os.path.basename(f)[:-4]
        for l in open(f, encoding="utf8", errors="ignore"):
            c = (l.rstrip("\n").split("\t") + [""] * 5)[:5]
            if not c[0].startswith("http"): continue
            meta.setdefault(c[0], {"cat": cat, "orgao": c[1], "uf": c[2].upper(), "cidade": c[3], "detalhe": c[4]})
    for f in sorted(glob.glob(f"{PUB}/urls/*_emails.tsv")):
        cat = os.path.basename(f)[:-11]
        for l in open(f, encoding="utf8", errors="ignore"):
            c = (l.rstrip("\n").split("\t") + [""] * 6)[:6]
            if "@" in c[0]: agent_rows.append((cat, *c))
    urls = list(meta) + [r[2] for r in agent_rows if r[2].startswith("http") and r[2] not in meta]
    urls = list(dict.fromkeys(urls))
    cpath = f"{PUB}/visited.json"
    cache = json.load(open(cpath)) if os.path.exists(cpath) else {}
    todo = [u for u in urls if u not in cache]
    print(f"{len(urls)} paginas | {len(urls)-len(todo)} em cache | {len(todo)} novas | {len(agent_rows)} e-mails vindos das buscas", flush=True)
    with cf.ThreadPoolExecutor(24) as ex:
        for i, (u, res) in enumerate(zip(todo, ex.map(lambda u: scrape(u), todo))):
            cache[u] = {"found": sorted(res[0]), "jipa": res[1]}
            if i % 100 == 0: print(f"  {i}/{len(todo)}", flush=True)
    json.dump(cache, open(cpath, "w"), ensure_ascii=False)

    rows = {}
    def add(email, url, cat, orgao, uf, cidade, cargo, detalhe, conf):
        email = clean(email)
        if not email or email in rows: return
        local, dom = email.split("@")
        cat = categoria_por_dominio(dom, cat)
        try: src_root = root(urllib.parse.urlparse(url).netloc)
        except Exception: src_root = ""
        if src_root and root(dom) != src_root:                       # pagina lista contatos de outros orgaos
            orgao, uf2 = rotulo_dominio(dom); uf = uf2 or ""; cidade = ""
        t = tipo(local, cargo)
        ji = bool(JIPA.search(cidade)) or ("ji-paran" in (orgao or "").lower())
        if re.search(r"estagi", cargo + " " + email, re.I): return
        if re.match(r"^[a-z][._-]", local): return
        if re.match(r"^\d", local) or is_person(local) or ("@" in email and VARA.search(local) and "jipa" not in local and not JIPA.search(cidade)): return
        if BADSETOR.search(cargo + " " + email + " " + (orgao or "")): return
        if re.match(r"^gabinete\d|^gabinetede[a-z]{8,}|^pj[a-z]|^pr[a-z]{2}-|oficio", local): return
        if dom.endswith("cnj.jus.br") and local.startswith(("gabinete", "gab.")): return
        if t == "Nominal (cargo)" and not cargo: return                  # sem cargo/setor publicado: nao entra
        if ji and t in ("Gabinete/Chefia", "Juridico/Procuradoria", "Nominal (cargo)"): return   # Ji-Parana: so contatos gerais
        rows[email] = dict(orgao=orgao, esfera=esfera(orgao, uf), uf=uf, cidade=cidade, categoria=cat, setor_cargo=cargo or t,
                           email=email, tipo=t, fonte=url, data=datetime.date.today().isoformat(), confianca=conf,
                           ji_parana="sim" if ji else "nao", detalhe_institucional=detalhe)
    # 1) e-mails achados pelo proprio coletor nas paginas oficiais (confianca alta)
    for u, m in meta.items():
        for e in cache.get(u, {}).get("found", []):
            if root(e.split("@")[1]) == root(urllib.parse.urlparse(u).netloc) or e.split("@")[1].endswith((".gov.br", ".jus.br", ".leg.br", ".mp.br", ".def.br", ".tc.br")):
                add(e, u, m["cat"], m["orgao"], m["uf"], m["cidade"], "", m["detalhe"], "alta")
    # 2) e-mails vindos das buscas (alta se a pagina confirma, senao media); exigem cargo/setor
    for cat, e, u, orgao, cargo, uf, cidade in agent_rows:
        m = meta.get(u, {})
        conf = "alta" if clean(e) in cache.get(u, {}).get("found", []) else "media"
        add(e, u, m.get("cat", cat), orgao or m.get("orgao", ""), (uf or m.get("uf", "")).upper(), cidade or m.get("cidade", ""), cargo, m.get("detalhe", ""), conf)

    doms = sorted({r["email"].split("@")[1] for r in rows.values()})
    with cf.ThreadPoolExecutor(32) as ex: list(ex.map(mx_ok, doms))
    prio = {"RH/Pessoas": 0, "Juridico/Procuradoria": 1, "Gabinete/Chefia": 2, "Secretaria/Protocolo": 3, "Nominal (cargo)": 4}
    cand = [r for r in rows.values() if mx_ok(r["email"].split("@")[1])]
    cand.sort(key=lambda r: (prio[r["tipo"]], r["confianca"] != "alta"))
    per, out = {}, []
    for r in cand:
        d = r["email"].split("@")[1]
        suf = ".".join(d.split(".")[-3:]) if d.endswith((".gov.br", ".leg.br", ".jus.br")) else d
        if per.get(d, 0) < 5 and per.get("sfx:" + suf, 0) < 14:
            per[d] = per.get(d, 0) + 1; per["sfx:" + suf] = per.get("sfx:" + suf, 0) + 1; out.append(r)
    while len(out) > TARGET:
        cnt = Counter(r["categoria"] for r in out if r["ji_parana"] != "sim" and r["categoria"] != "ji_parana_regiao")
        big = cnt.most_common(1)[0][0]
        idx = max((i for i, r in enumerate(out) if r["categoria"] == big and r["ji_parana"] != "sim"),
                  key=lambda i: (prio[out[i]["tipo"]], out[i]["confianca"] != "alta", i))
        out.pop(idx)
    cols = ["orgao","esfera","uf","cidade","categoria","setor_cargo","email","tipo","fonte","data","confianca","ji_parana","detalhe_institucional"]
    with open(f"{PUB}/resultado_publico.csv", "w", newline="", encoding="utf8") as fh:
        w = csv.DictWriter(fh, cols); w.writeheader(); w.writerows(out)
    print(f"\nTOTAL: {len(out)} contatos institucionais ({len(rows)-len(cand)} sem MX, {len(cand)-len(out)} cortados pelo limite por dominio)")
    print("por categoria:", dict(Counter(r["categoria"] for r in out)))
    print("por tipo:", dict(Counter(r["tipo"] for r in out)))
    print("por UF (top):", Counter(r["uf"] or "?" for r in out).most_common(8))
    print("confianca:", dict(Counter(r["confianca"] for r in out)), "| Ji-Parana:", sum(r["ji_parana"] == "sim" for r in out))

if __name__ == "__main__":
    main()
