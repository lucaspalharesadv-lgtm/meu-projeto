# -*- coding: utf-8 -*-
"""Junta os resultados dos processos paralelos do Lote 7 e registra todos os dominios visitados em hosts_ja_vistos.json
(para nunca visitar de novo). Saida: cc7_cands_all.json (entrada do final_add7.py)."""
import glob, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(HERE, 'estado')
cands = {}
for f in sorted(glob.glob(os.path.join(HERE, 'cc7_cands_*.json'))):
    if f.endswith('_all.json'):
        continue
    cands.update(json.load(open(f)))
json.dump(cands, open(os.path.join(HERE, 'cc7_cands_all.json'), 'w'), ensure_ascii=False)
VIS = os.path.join(EST, 'hosts_ja_vistos.json')
vis = json.load(open(VIS)); antes = len(vis); vs = set(vis)
for f in sorted(glob.glob(os.path.join(EST, 'cc7_done_*.json'))):
    for d in json.load(open(f)):
        if d not in vs:
            vis.append(d); vs.add(d)
with open(VIS + '.tmp', 'w') as fh:
    json.dump(sorted(vis), fh)
os.replace(VIS + '.tmp', VIS)
print('candidatos com e-mail', len(cands), '| hosts_ja_vistos', antes, '->', len(vis))
