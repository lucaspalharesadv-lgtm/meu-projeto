# -*- coding: utf-8 -*-
"""Discover law-firm websites with Yahoo search, by city and query variant. Writes JSONL incrementally. Usage: python3 -I discover.py BR|INT"""
import sys, json, time, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engines, cities, cities2
mode = sys.argv[1]
shard, nshard = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 1)
out = open(f"disc_{mode}.jsonl", "a", encoding="utf-8")
done = set()
import glob
for f in glob.glob(f"disc_{mode}*.done"):
    done |= set(open(f).read().split("\n"))
donef = open(f"disc_{mode}_{shard}.done", "a")
CAPS = {"SP","RJ","DF","BA","CE","MG","AM","PR","PE","GO","PA","RS","MA","AL","MS","RN","PI","PB","SE","MT","SC","ES","AP","RO","AC","RR","TO"}
capitals = {"São Paulo","Rio de Janeiro","Brasília","Salvador","Fortaleza","Belo Horizonte","Manaus","Curitiba","Recife","Goiânia","Belém","Porto Alegre","São Luís","Maceió","Campo Grande","Natal","Teresina","João Pessoa","Aracaju","Cuiabá","Florianópolis","Vitória","Macapá","Porto Velho","Rio Branco","Boa Vista","Palmas"}
tasks = []
if mode == "BR2":
    variants = ["escritório de advocacia {c} {uf}", "advogados {c} {uf}", "advocacia {c} {uf} contato", "advogado previdenciário {c}", "advogado trabalhista {c}"]
    for c, uf in cities2.BR2:
        for v in variants:
            for p in (1, 2):
                tasks.append(("BR", c, uf, v.format(c=c, uf=uf), p, "pt-BR,pt;q=0.9,en;q=0.8"))
elif mode == "BR3":
    variants = ["advogado {c}", "advocacia {c}", "escritorio advocacia {c} site", "advogado imobiliário {c}", "advogado criminalista {c}", "advogado tributarista {c}", "advogado bancário {c}", "advogado saúde planos de saúde {c}", "advogado INSS {c}", "advogado contratos {c}"]
    for c, uf in cities.BR:
        for v in variants:
            for p in ((1, 2) if c in capitals else (1,)):
                tasks.append(("BR", c, uf, v.format(c=c, uf=uf), p, "pt-BR,pt;q=0.9,en;q=0.8"))
elif mode == "INT3":
    V3 = {"US": ["law firm {c} attorneys"], "CA": ["law firm {c} lawyers"], "UK": ["solicitors {c} law firm"], "IE": ["solicitors {c} law firm"], "AU": ["law firm {c} lawyers"], "NZ": ["law firm {c} lawyers"], "PT": ["sociedade de advogados {c}"], "ES": ["despacho de abogados {c}"], "IT": ["studio legale {c}"], "FR": ["cabinet d'avocats {c}"], "DE": ["law firm {c} English speaking"], "NL": ["law firm {c} English speaking"], "BE": ["law firm {c} English speaking"], "CH": ["law firm {c} English speaking"], "LU": ["law firm {c} English speaking"], "JP": ["law firm {c} English speaking"], "AE": ["law firm {c} English speaking"]}
    L3 = {"US":"en-US,en;q=0.9","CA":"en-CA,en;q=0.9","UK":"en-GB,en;q=0.9","IE":"en-IE,en;q=0.9","AU":"en-AU,en;q=0.9","NZ":"en-NZ,en;q=0.9","PT":"pt-PT,pt;q=0.9","ES":"es-ES,es;q=0.9","IT":"it-IT,it;q=0.9","FR":"fr-FR,fr;q=0.9","DE":"en-US,en;q=0.9","NL":"en-US,en;q=0.9","BE":"en-US,en;q=0.9","CH":"en-US,en;q=0.9","LU":"en-US,en;q=0.9","JP":"en-US,en;q=0.9","AE":"en-US,en;q=0.9"}
    for cc, cs in cities.INT.items():
        for c in cs:
            for v in V3[cc]:
                for p in (1, 2):
                    tasks.append((cc, c, "", v.format(c=c), p, L3[cc]))
elif mode == "INT2":
    V2 = {"US": ["immigration lawyer {c}", "immigration attorney {c} Portuguese", "Brazilian lawyer {c}"], "CA": ["immigration lawyer {c}", "immigration consultant {c} Portuguese"], "UK": ["immigration solicitor {c}", "immigration lawyer {c} Portuguese"], "IE": ["immigration solicitor {c}", "solicitors {c} Portuguese"], "AU": ["migration agent {c}", "immigration lawyer {c}"], "NZ": ["immigration lawyer {c}", "immigration adviser {c}"], "PT": ["advogados {c}", "advogado imigração {c}", "escritório de advogados {c} brasileiros"], "ES": ["abogado extranjería {c}", "abogados {c} brasileños"], "IT": ["avvocato immigrazione {c}", "avvocato cittadinanza {c}"], "FR": ["avocat immigration {c}", "avocat {c} brésilien"], "DE": ["immigration lawyer {c}"], "NL": ["immigration lawyer {c}"], "BE": ["immigration lawyer {c}"], "CH": ["immigration lawyer {c}"], "LU": ["immigration lawyer {c}"], "JP": ["advogado brasileiro {c}", "immigration lawyer {c} Portuguese"], "AE": ["immigration lawyer {c}"]}
    L2 = {"US":"en-US,en;q=0.9","CA":"en-CA,en;q=0.9","UK":"en-GB,en;q=0.9","IE":"en-IE,en;q=0.9","AU":"en-AU,en;q=0.9","NZ":"en-NZ,en;q=0.9","PT":"pt-PT,pt;q=0.9","ES":"es-ES,es;q=0.9","IT":"it-IT,it;q=0.9","FR":"fr-FR,fr;q=0.9","DE":"de-DE,de;q=0.9,en;q=0.8","NL":"en-US,en;q=0.9","BE":"en-US,en;q=0.9","CH":"en-US,en;q=0.9","LU":"en-US,en;q=0.9","JP":"pt-BR,pt;q=0.9,en;q=0.8","AE":"en-US,en;q=0.9"}
    for cc, cs in cities2.INT2.items():
        for c in cs:
            for v in V2[cc]:
                for p in (1, 2):
                    tasks.append((cc, c, "", v.format(c=c), p, L2[cc]))
elif mode == "BR":
    variants = ["escritório de advocacia {c} {uf}", "advogados associados {c}", "advogado cível {c}", "advogado previdenciário {c}", "advogado trabalhista {c}", "advogado direito do consumidor {c}", "advogado empresarial {c}", "advogado de família {c}", "advocacia {c} contato"]
    for c, uf in cities.BR:
        pages = 3 if c in capitals else 2
        for v in variants:
            for p in range(1, pages + 1):
                tasks.append(("BR", c, uf, v.format(c=c, uf=uf), p, "pt-BR,pt;q=0.9,en;q=0.8"))
else:
    V = {"US": ["immigration lawyer {c}", "immigration attorney {c} Portuguese speaking", "Brazilian lawyer {c}", "advogado brasileiro {c}"],
         "CA": ["immigration lawyer {c}", "immigration consultant {c} Portuguese", "advogado brasileiro {c} Canadá"],
         "UK": ["immigration solicitor {c}", "immigration lawyer {c} Portuguese speaking", "advogado brasileiro {c} Reino Unido"],
         "IE": ["immigration solicitor {c}", "immigration lawyer {c} Portuguese", "advogado brasileiro {c} Irlanda"],
         "AU": ["migration agent {c}", "immigration lawyer {c}", "migration agent {c} Portuguese Brazilian"],
         "NZ": ["immigration lawyer {c}", "immigration adviser {c} Portuguese"],
         "PT": ["advogado imigração {c}", "advogados {c} brasileiros", "escritório de advogados {c}", "advogado nacionalidade portuguesa {c}"],
         "ES": ["abogado extranjería {c}", "abogado brasileños {c}", "abogado nacionalidad española {c}"],
         "IT": ["avvocato immigrazione {c}", "avvocato cittadinanza italiana {c}", "avvocato brasiliani {c}"],
         "FR": ["avocat immigration {c}", "avocat brésilien {c}", "avocat droit des étrangers {c}"],
         "DE": ["immigration lawyer {c} English", "Rechtsanwalt Aufenthaltsrecht {c}"], "NL": ["immigration lawyer {c}"], "BE": ["immigration lawyer {c}"], "CH": ["immigration lawyer {c}"], "LU": ["immigration lawyer {c}"],
         "JP": ["advogado brasileiro {c} Japão", "immigration lawyer {c} Portuguese"], "AE": ["immigration lawyer {c} Portuguese", "advogado brasileiro {c}"]}
    L = {"US":"en-US,en;q=0.9","CA":"en-CA,en;q=0.9","UK":"en-GB,en;q=0.9","IE":"en-IE,en;q=0.9","AU":"en-AU,en;q=0.9","NZ":"en-NZ,en;q=0.9","PT":"pt-PT,pt;q=0.9","ES":"es-ES,es;q=0.9","IT":"it-IT,it;q=0.9","FR":"fr-FR,fr;q=0.9","DE":"de-DE,de;q=0.9,en;q=0.8","NL":"en-US,en;q=0.9","BE":"en-US,en;q=0.9","CH":"en-US,en;q=0.9","LU":"en-US,en;q=0.9","JP":"pt-BR,pt;q=0.9,en;q=0.8","AE":"en-US,en;q=0.9"}
    for cc, cs in cities.INT.items():
        for c in cs:
            for v in V[cc]:
                for p in (1, 2):
                    tasks.append((cc, c, "", v.format(c=c), p, L[cc]))
print(mode, "tarefas:", len(tasks), "já feitas:", len(done), flush=True)
blocked_streak = 0; n = 0
tasks = [t for i, t in enumerate(tasks) if i % nshard == shard]
out = open(f"disc_{mode}_{shard}.jsonl", "a", encoding="utf-8")
for cc, c, uf, q, p, lang in tasks:
    key = f"{q}|{p}"
    if key in done: continue
    urls = None
    for attempt in range(4):
        try:
            urls, blocked = engines.yahoo(q, p, lang); break
        except Exception as e:
            print("ERR", attempt, q, p, e, flush=True); time.sleep(2 + 2 * attempt)
    if urls is None: continue
    if blocked:
        blocked_streak += 1; print("BLOQUEADO?", q, p, flush=True); time.sleep(90 * blocked_streak)
        if blocked_streak >= 4: print("parando: bloqueio persistente", flush=True); break
        continue
    blocked_streak = 0
    for u in urls:
        out.write(json.dumps({"cc": cc, "city": c, "uf": uf, "q": q, "p": p, "url": u}, ensure_ascii=False) + "\n")
    out.flush(); donef.write(key + "\n"); donef.flush(); n += 1
    if n % 50 == 0: print(time.strftime("%H:%M:%S"), "consultas:", n, "última:", q, p, len(urls), flush=True)
print("FIM", mode, n, flush=True)
