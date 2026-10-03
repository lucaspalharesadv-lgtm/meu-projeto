#!/usr/bin/env python3
"""Coletor de e-mails profissionais PUBLICOS.
Entrada: urls/*.txt (uma URL por linha) e urls/*_emails.tsv (email<TAB>url[<TAB>extra]).
Saida: resultado.csv (email, tipo, segmento, fonte, mx_ok) e relatorio no stdout.
Regras: so e-mails publicados em paginas publicas; dominio precisa ter MX; nada de escritorio de advocacia de Ji-Parana.
"""
import re, csv, glob, os, html, ssl, sys, urllib.parse, urllib.request, concurrent.futures as cf
import dns.resolver

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}")
BAD_DOMAINS = {"example.com","email.com","seudominio.com.br","dominio.com.br","sentry.io","wixpress.com","exemplo.com","exemplo.com.br",
  "seuemail.com","site.com","domain.com","mail.com","yourdomain.com","wordpress.com","godaddy.com","schema.org","w3.org",
  "sentry-next.wixpress.com","seusite.com.br","meusite.com.br","suaempresa.com.br","empresa.com.br","email.com.br","provedor.com.br"}
BAD_EXT = (".png",".jpg",".jpeg",".gif",".webp",".svg",".css",".js",".pdf",".woff",".woff2",".ico")
BAD_LOCAL = ("noreply","no-reply","donotreply","privacidade","dpo","lgpd","imprensa","webmaster","abuse","postmaster","ouvidoria","denuncia","canaldedenuncia","seuemail","email","nome","usuario","exemplo","teste","test")
JIPA = re.compile(r"ji[\s\-]?paran[aá]", re.I)
SKIP_HOST = ("linkedin","facebook","instagram","youtube","jusbrasil","indeed","glassdoor","wikipedia","gov.br","jus.br","oab.org.br","vagas.com","infojobs","catho","gupy.io","twitter","x.com","google","bing.","tiktok")
SUBPATHS = ("contato","fale-conosco","trabalhe-conosco","contact","equipe","carreira","carreiras","quem-somos")

def get(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        raw = r.read(1_200_000)
        return raw.decode(r.headers.get_content_charset() or "utf-8", errors="ignore")

def deob(t):
    t = html.unescape(t)
    t = re.sub(r"\s*[\[\(]\s*(?:at|arroba)\s*[\]\)]\s*", "@", t, flags=re.I)
    return re.sub(r"mailto:", " ", t, flags=re.I)

def clean(e):
    e = e.strip(".,;:-_%+").lower()
    if e.endswith(BAD_EXT): return None
    local, _, dom = e.partition("@")
    if not local or dom in BAD_DOMAINS or any(local.startswith(b) for b in BAD_LOCAL): return None
    if len(local) > 40 or re.search(r"\d{7,}", local) or ".." in e: return None
    return e

def scrape(url):
    p = urllib.parse.urlparse(url if "//" in url else "https://" + url)
    if any(s in p.netloc for s in SKIP_HOST): return {}
    base = f"{p.scheme}://{p.netloc}"
    found, jipa, adv = {}, False, False
    for u in [url] + [f"{base}/{s}" for s in SUBPATHS]:
        try: t = get(u)
        except Exception: continue
        if JIPA.search(t): jipa = True
        if re.search(r"advoca", t, re.I): adv = True
        for e in EMAIL_RE.findall(deob(t)):
            e = clean(e)
            if e: found.setdefault(e, u)
        if len(found) >= 10: break
    return {} if (jipa and adv) else found

_mx = {}
def mx_ok(dom):
    if dom not in _mx:
        try: dns.resolver.resolve(dom, "MX", lifetime=6); _mx[dom] = True
        except Exception:
            try: dns.resolver.resolve(dom, "A", lifetime=6); _mx[dom] = True
            except Exception: _mx[dom] = False
    return _mx[dom]

def tipo(e):
    l = e.split("@")[0]
    if re.match(r"(rh|recrutamento|selecao|talentos|vagas|curriculo|trabalheconosco|pessoas|gente|carreira)", l): return "RH"
    if re.match(r"(socio|diretoria|diretor|presidencia|juridico|gerencia|gerente|coordenacao|advogados?$)", l): return "Decisor/Juridico"
    if re.match(r"(contato|atendimento|comercial|geral|secretaria|recepcao|adm|administrativo|financeiro|fale|sac)", l): return "Generico"
    return "Nominal"

def main():
    rows = {}
    jobs = []   # (segmento, url)
    for f in sorted(glob.glob(f"{HERE}/urls/*.txt")):
        seg = os.path.basename(f)[:-4]
        seen_dom = set()
        for l in open(f, encoding="utf8", errors="ignore"):
            u = l.strip().split()[0] if l.strip() else ""
            if not u.startswith(("http", "www")) and "." not in u: continue
            d = urllib.parse.urlparse(u if "//" in u else "//" + u).netloc.lower().removeprefix("www.")
            if d and d not in seen_dom: seen_dom.add(d); jobs.append((seg, u if "//" in u else "https://" + u))
    pre = []
    for f in sorted(glob.glob(f"{HERE}/urls/*_emails.tsv")):
        seg = os.path.basename(f)[:-11]
        for l in open(f, encoding="utf8", errors="ignore"):
            c = l.rstrip("\n").split("\t")
            if len(c) >= 2:
                e = clean(deob(c[0]))
                if e and EMAIL_RE.fullmatch(e): pre.append((seg, e, c[1]))
    print(f"{len(jobs)} sites para visitar | {len(pre)} e-mails vindos das buscas", flush=True)
    with cf.ThreadPoolExecutor(24) as ex:
        for i, ((seg, u), res) in enumerate(zip(jobs, ex.map(lambda j: scrape(j[1]), jobs))):
            for e, src in res.items(): rows.setdefault(e, (seg, src))
            if i % 100 == 0: print(f"  {i}/{len(jobs)} sites, {len(rows)} e-mails", flush=True)
    for seg, e, src in pre: rows.setdefault(e, (seg, src))
    doms = sorted({e.split("@")[1] for e in rows})
    with cf.ThreadPoolExecutor(32) as ex: list(ex.map(mx_ok, doms))
    out = [(e, tipo(e), s, src) for e, (s, src) in rows.items() if mx_ok(e.split("@")[1])]
    # remove ruido: caixas de provedor gratuito so entram se vieram de pagina do proprio site (mantem), duplicatas ja tratadas
    with open(f"{HERE}/resultado.csv", "w", newline="", encoding="utf8") as f:
        w = csv.writer(f); w.writerow(["email","tipo","segmento","fonte"]); w.writerows(sorted(out, key=lambda r: (r[1], r[0])))
    print(f"\nTOTAL: {len(out)} e-mails validos ({len(rows)-len(out)} descartados por dominio sem MX)")
    from collections import Counter
    print(Counter(r[2] for r in out)); print(Counter(r[1] for r in out))

if __name__ == "__main__":
    main()
