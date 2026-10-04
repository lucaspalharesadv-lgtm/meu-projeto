#!/usr/bin/env python3
"""Le os SITES das empresas/escritorios de correspondencia e extrai e-mails institucionais publicados."""
import csv, re, os, sys, urllib.parse, concurrent.futures as cf
import coletor_publico as cp   # reaproveita get(), deob(), clean(), mx_ok()
HERE = os.path.dirname(os.path.abspath(__file__)); D = f"{HERE}/correspondencia"
PATHS = ["", "/contato", "/contatos", "/fale-conosco", "/faleconosco", "/trabalhe-conosco", "/seja-correspondente", "/seja-nosso-correspondente",
         "/correspondentes", "/correspondente", "/cadastro", "/cadastro-correspondente", "/quem-somos", "/sobre", "/institucional", "/parceiros"]
FREE = cp.FREE
def scrape(site):
    p = urllib.parse.urlparse(site if "//" in site else "https://" + site); base = f"{p.scheme}://{p.netloc}"
    found = {}
    for path in PATHS:
        for u in ([site] if path == "" else [base + path]):
            try: t = cp.get(u)
            except Exception: continue
            for e in cp.EMAIL_RE.findall(cp.deob(t)):
                e = cp.clean(e)
                if e and e.split("@")[1] not in FREE: found.setdefault(e, u)
        if len(found) >= 10: break
    return found
def main():
    orgs = []
    for f in ("plataformas.tsv", "escritorios.tsv"):
        for l in open(f"{D}/{f}", encoding="utf8"):
            c = (l.rstrip("\n").split("\t") + [""] * 8)[:8]
            if c[0] and c[0] != "ORGANIZACAO" and c[2].startswith("http"): orgs.append((c[0], c[2]))
    extra = f"{D}/sites_extra.txt"
    if os.path.exists(extra):
        for l in open(extra, encoding="utf8"):
            l = l.strip().split("\t")
            if l and l[0].startswith("http"): orgs.append((l[1] if len(l) > 1 else l[0], l[0]))
    orgs = list({s: (n, s) for n, s in orgs}.values())
    print(len(orgs), "sites para ler", flush=True)
    out = {}
    with cf.ThreadPoolExecutor(16) as ex:
        for (n, s), res in zip(orgs, ex.map(lambda o: scrape(o[1]), orgs)):
            for e, u in res.items():
                if cp.mx_ok(e.split("@")[1]): out.setdefault(e, (n, s, u))
    rows = sorted(out.items(), key=lambda x: (x[1][0].lower(), x[0]))
    with open(f"{D}/emails_correspondencia.csv", "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh); w.writerow(["empresa", "site", "email", "fonte"])
        for e, (n, s, u) in rows: w.writerow([n, s, e, u])
    print(f"TOTAL: {len(rows)} e-mails de {len({v[0] for v in out.values()})} empresas")
if __name__ == "__main__": main()
