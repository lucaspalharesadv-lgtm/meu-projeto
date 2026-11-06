# -*- coding: utf-8 -*-
"""Validate (syntax + DNS) and assemble the bulk lists: CSVs per tab, one XLSX, Instantly-ready CSVs per template."""
import csv, json, os, re, sys, ssl, urllib.request, urllib.parse, collections, random
from concurrent.futures import ThreadPoolExecutor
import openpyxl
COLS = ["saudacao","nome_contato","tratamento","escritorio","cidade","estado","email","tipo_email","idioma_email","modelo","personalizacao","telefone","site","areas","idiomas","fonte_url","regiao","prioridade","status","enviado_em","follow_up_1","follow_up_2","resposta","observacoes"]
EMAIL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._%+\-']{0,63}@(?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,24}$")
ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
proxy = os.environ.get("HTTPS_PROXY")
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"https": proxy}), urllib.request.HTTPSHandler(context=ctx))
cache = {}
try: cache = json.load(open("dns_cache_bulk.json"))
except Exception: pass
def dns(domain):
    if domain in cache: return cache[domain]
    res = "erro"
    for typ in ("MX", "A"):
        try:
            with opener.open("https://dns.google/resolve?" + urllib.parse.urlencode({"name": domain, "type": typ}), timeout=15) as r:
                d = json.loads(r.read().decode())
            if d.get("Status") == 0 and d.get("Answer"): res = typ; break
            if d.get("Status") == 3: res = "NXDOMAIN"; break
            res = "sem_resposta"
        except Exception: res = "erro"
    cache[domain] = res; return res

rows = list(csv.DictReader(open("bulk_rows.csv", encoding="utf-8", newline=""), delimiter=";"))
rows = [r for r in rows if EMAIL_RE.match(r["email"])]
doms = sorted({r["email"].split("@")[1] for r in rows})
todo = [d for d in doms if d not in cache]
print("linhas:", len(rows), "| domínios:", len(doms), "| a consultar:", len(todo), flush=True)
with ThreadPoolExecutor(max_workers=24) as ex:
    for i, _ in enumerate(ex.map(dns, todo)):
        if i % 500 == 0: print("  dns", i, flush=True); json.dump(cache, open("dns_cache_bulk.json", "w"))
json.dump(cache, open("dns_cache_bulk.json", "w"))
ok = [r for r in rows if cache.get(r["email"].split("@")[1]) in ("MX", "A")]
bad = [r for r in rows if r not in ok]
print("válidos:", len(ok), "| inválidos:", len(bad))
# tabs
def tab(r):
    if r["modelo"] == "BR_PT": return "BR_PT"
    return "INT_EN" if r["idioma_email"] == "EN" else "INT_PT"
order_reg = {"Brasil SP":0,"Brasil RJ":1,"Brasil MG":2,"Brasil PR":3,"Brasil RS":4,"Brasil SC":5,"Brasil DF":6,"Brasil GO":7,"Brasil BA":8,"Brasil PE":9,"Brasil CE":10,"Brasil ES":11,"Brasil MT":12,"Brasil MS":13,"Brasil RO":14}
for r in ok: r["_tab"] = tab(r)
ok.sort(key=lambda r: (r["_tab"], int(r["prioridade"]), order_reg.get(r["regiao"], 50), r["regiao"], r["escritorio"].lower()))
counts = collections.Counter(r["_tab"] for r in ok)
print("por aba:", dict(counts)); print("por modelo:", dict(collections.Counter(r["modelo"] for r in ok))); print("por tipo:", dict(collections.Counter(r["tipo_email"] for r in ok)))
print("por país/UF:", collections.Counter(r["regiao"] for r in ok).most_common(40))
os.makedirs("out", exist_ok=True)
for t in ("BR_PT", "INT_EN", "INT_PT"):
    sub = [r for r in ok if r["_tab"] == t]
    with open(f"out/Lista_massa_{t}.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, delimiter=";", extrasaction="ignore"); w.writeheader(); w.writerows(sub)
for m in sorted({r["modelo"] for r in ok}):
    sub = [r for r in ok if r["modelo"] == m]
    with open(f"out/Instantly_{m}.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["email","saudacao","escritorio","personalizacao","nome_contato","cidade","estado","site"], delimiter=",", extrasaction="ignore"); w.writeheader(); w.writerows(sub)
with open("out/Lista_massa_completa.csv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["aba"] + COLS, delimiter=";", extrasaction="ignore"); w.writeheader()
    for r in ok: w.writerow({"aba": r["_tab"], **r})
wb = openpyxl.Workbook(); ws0 = wb.active; ws0.title = "Resumo"
ws0.append(["Lista em massa", "Gerada em 05/11/2026 por rastreamento dos sites dos escritórios. Só e-mails publicados; DNS verificado."])
ws0.append(["Aba", "Contatos"]); [ws0.append([t, counts.get(t, 0)]) for t in ("BR_PT", "INT_EN", "INT_PT")]
ws0.append(["Total", len(ok)]); ws0.append([]); ws0.append(["Coluna modelo", "EN, PT, OPS_EN, OPS_PT ou BR_PT: qual rascunho e qual currículo usar."])
for t in ("BR_PT", "INT_EN", "INT_PT"):
    ws = wb.create_sheet(t); ws.append(COLS)
    for r in ok:
        if r["_tab"] == t: ws.append([r.get(c, "") for c in COLS])
wb.save("out/Lista_massa_10k.xlsx")
with open("out/rejeitados_dns.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["email", "dns", "escritorio", "site"], delimiter=";"); w.writeheader()
    for r in bad: w.writerow({"email": r["email"], "dns": cache.get(r["email"].split("@")[1]), "escritorio": r["escritorio"], "site": r["site"]})
json.dump({"total": len(ok), "por_aba": dict(counts), "por_modelo": dict(collections.Counter(r["modelo"] for r in ok)), "por_tipo": dict(collections.Counter(r["tipo_email"] for r in ok)), "invalidos": len(bad)}, open("out/stats.json", "w"), ensure_ascii=False, indent=1)
print("arquivos em out/")
