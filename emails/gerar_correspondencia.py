#!/usr/bin/env python3
"""Monta a lista de 200 contatos para oferta de servicos de correspondente juridico (Ji-Parana/RO) + textos.
Fontes: (1) emails lidos nos sites de plataformas/escritorios de correspondencia; (2) escritorios de advocacia
da coleta anterior (emails/resultado.csv). Uma caixa por dominio, so caixas institucionais."""
import csv, re, os, sys, urllib.parse, hashlib, concurrent.futures as cf
import coletor_publico as cp
HERE = os.path.dirname(os.path.abspath(__file__)); D = f"{HERE}/correspondencia"
LEGAL = re.compile(r"adv|advoc|juris|\bjur|law|legal|direito|sociedade|corresp|diligen|audienc", re.I)
GOOD = re.compile(r"^(correspondente|correspondentes|parcerias?|comercial|contato|contatos|juridico|atendimento|diligencia|cadastro|geral|advogados|secretaria|relacionamento|recrutamento|dmk|totem|info)", re.I)
BADD = ("wixpress.com", "sentry", "meuemail.com", "builderallwppro.com")
def root(h): return cp.root(h)
def prio(local):
    for i, k in enumerate(("correspondente", "parceria", "comercial", "contato", "juridico", "atendimento", "diligencia", "geral", "advogados", "secretaria", "relacionamento", "recrutamento")):
        if local.startswith(k): return i
    return 50
def pick(key, opts): return opts[int(hashlib.md5(key.encode()).hexdigest(), 16) % len(opts)]
alts = {}
cands = {}   # dominio -> (prio, email, empresa, site, categoria)
# (1) correspondencia
for x in csv.DictReader(open(f"{D}/emails_correspondencia.csv", encoding="utf8")):
    e = x["email"]; l, d = e.split("@")
    if any(b in d for b in BADD) or d.endswith((".pt",)) or cp.is_person(l) or re.match(r"^[a-z]{2,3}$", l) is None and False: continue
    if root(d) != root(urllib.parse.urlparse(x["site"]).netloc): continue         # so e-mail do proprio dominio
    if l in ("angola", "portugal", "marketing", "conteudo", "financeiro", "bd", "acordos"): continue
    if re.match(r"^[a-z]{2}$", l): continue                                          # caixas de filial por UF (al@, am@...)
    k = root(d); p = prio(l); alts.setdefault(k, []).append((p, e, x["empresa"], x["site"]))
    if k not in cands or p < cands[k][0]: cands[k] = (p, e, x["empresa"], x["site"], "Plataforma / correspondência" if True else "")
n1 = len(cands)
# (2) escritorios da coleta anterior
for x in csv.DictReader(open(f"{HERE}/resultado.csv", encoding="utf8")):
    if x["segmento"] not in ("sudeste_escritorios", "sul_co_escritorios", "ne_norte_escritorios", "rankings", "empresas_juridico"): continue
    e = x["email"]; l, d = e.split("@"); host = urllib.parse.urlparse(x["fonte"]).netloc
    esc = x["segmento"] != "empresas_juridico"          # segmentos de escritorios ja foram coletados como escritorios
    if not (esc or LEGAL.search(d) or LEGAL.search(host)) or cp.is_person(l) or x["tipo"] == "Nominal": continue
    if re.match(r"^(gerencia|rh|recrutamento|talentos|vagas|curriculo|financeiro|marketing|imprensa)", l): continue
    k = root(d); p = prio(l)
    if k not in cands or p < cands[k][0]: cands[k] = (p, e, "", f"https://{host}", "Escritório de advocacia")
print(f"{n1} da correspondência + {len(cands)-n1} escritórios = {len(cands)} candidatos (1 por domínio)", flush=True)
# titulos dos sites -> nome da empresa
def titulo(site):
    try:
        t = cp.get(site, 8)
        m = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
        return re.sub(r"\s+", " ", cp.html.unescape(m.group(1))).strip() if m else ""
    except Exception: return ""
items = sorted(cands.items(), key=lambda kv: (kv[1][4] != "Plataforma / correspondência", kv[1][0], kv[0]))
with cf.ThreadPoolExecutor(16) as ex: tits = list(ex.map(lambda kv: titulo(kv[1][3]) if not kv[1][2] else "", items))
def nome(titulo_, dom):
    t = re.split(r"\s[\|\-–—•·:]\s", titulo_)[0].strip() if titulo_ else ""
    t = re.sub(r"(?i)\b(home|página inicial|inicio|início|bem[- ]vindo[s]?|seja bem[- ]vindo|site oficial)\b", "", t).strip(" -|")
    if 3 <= len(t) <= 42 and not re.search(r"(?i)404|erro|error|just a moment|wordpress|index of|domain|hospedagem", t): return t
    return ""
OPEN = "Prezados"
rows = []
for (k, (p, e, emp, site, cat)), tit in zip(items, tits):
    emp = emp or nome(tit, k)
    rows.append([cat, emp, e, site])
rows = rows[:200]
if len(rows) < 200:                                   # completa com 2a caixa de dominios da correspondencia
    usados = {r[2] for r in rows}
    for k, lst in sorted(alts.items()):
        for p_, e_, emp_, site_ in sorted(lst):
            if e_ not in usados and len(rows) < 200: rows.append(["Plataforma / correspondência", emp_, e_, site_]); usados.add(e_)
ASS = ["Correspondente jurídico em Ji-Paraná/RO{para}", "Advogado correspondente em Rondônia (Ji-Paraná){para}", "Audiências e diligências em Ji-Paraná/RO{para}"]
PL_ASS = ["Cadastro de correspondente jurídico: Ji-Paraná/RO", "Advogado de Ji-Paraná/RO interessado em atuar como correspondente"]
def corpo(cat, emp, e):
    key = e
    fem = {"advocacia", "sociedade", "assessoria", "consultoria", "banca", "associação", "plataforma", "logística", "rede", "central", "empresa", "firma"}
    art = "da" if emp and emp.split()[0].lower() in fem else "do"
    sal = f"Prezada equipe {art} {emp}," if emp else "Prezados,"
    if cat.startswith("Plataforma"):
        abre = pick(key + "a", ["Sou advogado (OAB/RO 11.037), de Ji-Paraná/RO, e gostaria de me cadastrar como correspondente jurídico para audiências, diligências, cópias processuais e protocolos na minha região.",
                                "Escrevo para me colocar à disposição como correspondente jurídico em Ji-Paraná/RO (audiências, diligências, cópias e protocolos). Sou advogado, OAB/RO 11.037."])
        fecha = pick(key + "f", ["Peço que me informem como funciona o cadastro, os valores por serviço e o prazo de pagamento.", "Agradeço se puderem me orientar sobre o cadastro, os valores por serviço e o prazo de pagamento."])
    else:
        abre = pick(key + "a", ["Sou advogado (OAB/RO 11.037), de Ji-Paraná/RO, e atuo como correspondente jurídico na região, para escritórios e departamentos jurídicos que não têm estrutura em Rondônia.",
                                "Escrevo para oferecer meus serviços de correspondência jurídica em Ji-Paraná/RO, atendendo escritórios e departamentos jurídicos de outros estados. Sou advogado, OAB/RO 11.037."])
        fecha = pick(key + "f", ["Se precisarem de apoio em Rondônia, ou quiserem me incluir no cadastro de correspondentes, envio valores e condições.",
                                 "Caso haja demanda em Rondônia, ou interesse em manter um correspondente na região, fico à disposição para enviar valores e condições."])
    meio = pick(key + "m", ["Realizo audiências, diligências, cópias processuais e protocolos, com acompanhamento no PJe, e-SAJ, eproc e Projudi. Tenho mais de 5 anos de contencioso, com audiências e sustentações orais.",
                            "Faço audiências, diligências, cópias e protocolos, em processos físicos e digitais (PJe, e-SAJ, eproc e Projudi). São mais de 5 anos de contencioso, incluindo audiências e sustentações orais."])
    jf = pick(key + "j", ["Estagiei na Justiça Federal e na AGU/Procuradoria Federal em Ji-Paraná, e por isso conheço bem a rotina desses órgãos por aqui. Atuo com pontualidade e comunicação clara.",
                          "Fui estagiário da Justiça Federal e da AGU/Procuradoria Federal em Ji-Paraná, o que me dá familiaridade com esses órgãos na região. Trabalho com pontualidade e comunicação clara."])
    return "\n\n".join([sal, abre, meio, jf, fecha, "Meu currículo segue em anexo.", "Se preferirem não receber novas mensagens, basta responder e não voltarei a escrever.",
                        "Atenciosamente,\nLucas Alexandre Horas Palhares\nAdvogado | OAB/RO 11.037\n(69) 99335-9788 | lucaspalharesadv@gmail.com"])
out = []
for i, (cat, emp, e, site) in enumerate(rows, 1):
    a = pick(e + "s", PL_ASS) if cat.startswith("Plataforma") else pick(e + "s", ASS).format(para="")
    out.append({"n": i, "categoria": cat, "empresa": emp, "email": e, "site": site, "assunto": a, "corpo": corpo(cat, emp, e), "status": ""})
with open(f"{D}/lista_200.csv", "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, list(out[0])); w.writeheader(); w.writerows(out)
import collections
print(len(out), "contatos |", dict(collections.Counter(o["categoria"] for o in out)), "| com nome da empresa:", sum(bool(o["empresa"]) for o in out))
