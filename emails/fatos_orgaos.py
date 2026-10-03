#!/usr/bin/env python3
"""Extrai FATOS INSTITUCIONAIS reais de cada orgao (site oficial) para personalizar os e-mails.

Para cada dominio de e-mail da lista: baixa a pagina inicial e paginas 'sobre', e extrai
  - atribuicao: 1 frase do proprio site sobre a funcao/competencia/missao do orgao
  - aviso: ate 2 chamadas de edital / processo seletivo / concurso / chamamento visiveis no site
Nada de dados pessoais. Saida: publico/fatos.json
"""
import csv, json, os, re, ssl, sys, urllib.parse, urllib.request, concurrent.futures as cf
from lxml import html as LH

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
PATHS = ["", "/sobre", "/institucional", "/quem-somos", "/a-instituicao", "/o-tribunal", "/competencias", "/atribuicoes", "/institucional/sobre"]
KW = re.compile(r"\b(compete|competência|competências|atribui[cç][oõ]es|atribuição|finalidade|miss[aã]o|respons[aá]vel por|tem por objetivo|tem como objetivo|atua |atuação|órgão|instituição|exerce)\b", re.I)
BAD = re.compile(r"cookie|javascript|copyright|todos os direitos|acessibilidade|política de privacidade|lgpd|fale conosco|menu|clique|navegador|©|whatsapp|siga-nos|newsletter|login|senha|cadastre", re.I)
AVISO = re.compile(r"\b(edital|processo seletivo|concurso p[uú]blico|chamamento|sele[cç][aã]o p[uú]blica|credenciamento|inscri[cç][oõ]es abertas)\b", re.I)

def get(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        raw = r.read(1_200_000); enc = r.headers.get_content_charset() or "utf-8"
        return raw.decode(enc, errors="ignore"), r.geturl()

def clean(t): return re.sub(r"\s+", " ", t or "").strip()

def parse(page, base):
    doc = LH.fromstring(page)
    for bad in doc.xpath("//script|//style|//nav|//footer|//noscript|//header//form"): bad.getparent().remove(bad)
    meta = [clean(m.get("content")) for m in doc.xpath("//meta[@name='description' or @property='og:description']") if m.get("content")]
    blocks = [clean(e.text_content()) for e in doc.xpath("//p|//li|//h2|//h3|//div[contains(@class,'description') or contains(@class,'sobre') or contains(@class,'about')]")]
    cand = [t for t in meta + blocks if 60 <= len(t) <= 420 and KW.search(t) and not BAD.search(t)]
    avisos = []
    for a in doc.xpath("//a[@href]"):
        t = clean(a.text_content())
        if 18 <= len(t) <= 150 and AVISO.search(t) and not BAD.search(t):
            href = urllib.parse.urljoin(base, a.get("href"))
            avisos.append((t, href))
    title = clean((doc.xpath("//title/text()") or [""])[0])
    return cand, avisos, title

def frase(t):
    t = clean(t)
    m = re.match(r"(.{50,230}?[\.;])(\s|$)", t)
    s = (m.group(1) if m else t[:200]).rstrip(" ;")
    return s[:230]

def fatos_dominio(dom):
    hosts = [dom, "www." + dom]
    cands, avisos, title, ok_url = [], [], "", ""
    for h in hosts:
        got = False
        for p in PATHS:
            url = f"https://{h}{p}"
            try: page, final = get(url)
            except Exception: continue
            got = True
            try: c, a, t = parse(page, final)
            except Exception: continue
            cands += c; avisos += a; title = title or t; ok_url = ok_url or final
            if len(cands) >= 6 and avisos: break
        if got: break
    # escolher melhor atribuicao: preferir a que mencione 'compete|finalidade|miss'
    best = ""
    ranked = sorted(cands, key=lambda t: (0 if re.search(r"compete|finalidade|miss[aã]o|atribui", t, re.I) else 1, abs(len(t) - 150)))
    if ranked: best = frase(ranked[0])
    seen, av = set(), []
    for t, u in avisos:
        k = t.lower()
        if k in seen: continue
        seen.add(k); av.append({"texto": t, "url": u, "recente": bool(re.search(r"202[56]", t + u))})
    av.sort(key=lambda x: (not x["recente"], len(x["texto"])))
    return {"site": ok_url, "titulo": title[:120], "atribuicao": best, "avisos": av[:2]}

def main():
    res = list(csv.DictReader(open(f"{HERE}/publico/resultado_publico.csv", encoding="utf8")))
    doms = sorted({x["email"].split("@")[1] for x in res})
    out_path = f"{HERE}/publico/fatos.json"
    out = json.load(open(out_path)) if os.path.exists(out_path) else {}
    todo = [d for d in doms if d not in out]
    print(f"{len(doms)} dominios | {len(doms)-len(todo)} em cache | {len(todo)} para buscar", flush=True)
    with cf.ThreadPoolExecutor(16) as ex:
        for i, (d, r) in enumerate(zip(todo, ex.map(fatos_dominio, todo))):
            out[d] = r
            if i % 25 == 0:
                print(f"  {i}/{len(todo)}", flush=True); json.dump(out, open(out_path, "w"), ensure_ascii=False)
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
    com_atr = sum(1 for v in out.values() if v["atribuicao"]); com_av = sum(1 for v in out.values() if v["avisos"])
    print(f"\nconcluido: {len(out)} orgaos | com atribuicao: {com_atr} | com aviso de edital/processo: {com_av}")

if __name__ == "__main__":
    main()
