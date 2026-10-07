# -*- coding: utf-8 -*-
"""Registra rascunhos criados. Uso: python3 registrar.py lote.json  (lista de {email, escritorio, assunto, abordagem, lote, planilha, draft_url})"""
import csv, json, os, sys, datetime
B = os.path.dirname(os.path.abspath(__file__)); CTRL = os.path.join(B, 'controle_envios.csv')
COLS = ['Data', 'E-mail', 'Escritorio', 'Assunto', 'Abordagem', 'Lote', 'Planilha', 'Link do rascunho', 'Status']
novo = not os.path.exists(CTRL)
with open(CTRL, 'a', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh)
    if novo: w.writerow(COLS)
    for x in json.load(open(sys.argv[1])):
        w.writerow([datetime.date.today().isoformat(), x['email'].lower(), x.get('escritorio', ''), x.get('assunto', ''), x.get('abordagem', ''), x.get('lote', ''), x.get('planilha', ''), x.get('draft_url', ''), 'rascunho criado'])
print('registrados', len(json.load(open(sys.argv[1]))))
