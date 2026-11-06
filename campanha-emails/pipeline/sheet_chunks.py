# -*- coding: utf-8 -*-
"""Write JSON chunks (35 rows each) of the first N rows of each mass list, for Google Sheets append_values."""
import csv, json, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
COLS = ["saudacao","nome_contato","tratamento","escritorio","cidade","estado","email","tipo_email","idioma_email","modelo","personalizacao","telefone","site","areas","idiomas","fonte_url","regiao","prioridade","status","enviado_em","follow_up_1","follow_up_2","resposta","observacoes"]
for tab in ("BR_PT", "INT_EN", "INT_PT"):
    rows = list(csv.DictReader(open(f"out/Lista_massa_{tab}.csv", encoding="utf-8-sig", newline=""), delimiter=";"))[:N]
    vals = []
    for r in rows:
        row = []
        for c in COLS:
            v = r.get(c, "") or ""
            if v[:1] in ("+", "=", "-", "@"): v = "'" + v
            row.append(v)
        vals.append(row)
    for i in range(0, len(vals), 35):
        json.dump(vals[i:i+35], open(f"out/chunk_{tab}_{i//35+1}.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(tab, len(vals), "linhas,", (len(vals)+34)//35, "chunks")
