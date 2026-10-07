# -*- coding: utf-8 -*-
"""Apoio ao radar de respostas e ao follow-up.
  python3 radar.py contatados            -> JSON {email: {escritorio, data, assunto, abordagem, status}} de todos ja contatados
  python3 radar.py followup [dias=7]     -> contatos com rascunho criado ha >= N dias e sem follow-up/resposta registrados
  python3 radar.py marcar <email> <status> [nota]  -> atualiza a coluna Status da ultima linha daquele e-mail
Status usados: 'rascunho criado' | 'enviado' | 'follow-up criado' | 'respondeu: positivo' | 'respondeu: negativo' | 'respondeu: pediu tabela' | 'respondeu: outro' | 'bounce'"""
import csv, json, os, sys, datetime
B = os.path.dirname(os.path.abspath(__file__)); CTRL = os.path.join(B, 'controle_envios.csv')
COLS = ['Data', 'E-mail', 'Escritorio', 'Assunto', 'Abordagem', 'Lote', 'Planilha', 'Link do rascunho', 'Status', 'Nota']

def ler():
    if not os.path.exists(CTRL): return []
    rows = list(csv.DictReader(open(CTRL, encoding='utf-8-sig')))
    for r in rows: r.setdefault('Nota', '')
    return rows

def gravar(rows):
    with open(CTRL + '.tmp', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction='ignore'); w.writeheader(); w.writerows(rows); fh.flush(); os.fsync(fh.fileno())
    os.replace(CTRL + '.tmp', CTRL)

def contatados():
    out = {}
    for r in ler():
        out[r['E-mail'].lower()] = {k: r.get(k, '') for k in ('Escritorio', 'Data', 'Assunto', 'Abordagem', 'Status', 'Nota')}
    return out

def followup(dias=7):
    hoje = datetime.date.today(); out = []
    for r in ler():
        try: d = datetime.date.fromisoformat(r['Data'])
        except Exception: continue
        st = (r.get('Status') or '').lower()
        if (hoje - d).days >= dias and st in ('rascunho criado', 'enviado'):
            out.append({k: r.get(k, '') for k in ('E-mail', 'Escritorio', 'Data', 'Assunto', 'Abordagem', 'Status')})
    return out

def marcar(email, status, nota=''):
    rows = ler(); ok = False
    for r in reversed(rows):
        if r['E-mail'].lower() == email.lower():
            r['Status'] = status
            if nota: r['Nota'] = (r.get('Nota', '') + ' | ' + nota).strip(' |')
            ok = True; break
    if ok: gravar(rows)
    return ok

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'contatados'
    if cmd == 'contatados': print(json.dumps(contatados(), ensure_ascii=False, indent=1))
    elif cmd == 'followup': print(json.dumps(followup(int(sys.argv[2]) if len(sys.argv) > 2 else 7), ensure_ascii=False, indent=1))
    elif cmd == 'marcar': print('ok' if marcar(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else '') else 'nao encontrado')
