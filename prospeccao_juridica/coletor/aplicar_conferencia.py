# -*- coding: utf-8 -*-
"""Aplica a conferencia humana da amostra (pagina "Conferencia dos Lotes 7 e 8").
Uso: python3 aplicar_conferencia.py PASTA_EXPORTADA
PASTA_EXPORTADA = saida do ArtifactData 'list' com out_dir (um JSON por documento em conferencia/).
1) cada contato marcado "Tem problema" sai da base e vai para outros_emails_capturados.csv com o motivo;
2) mostra a taxa de erro de cada lote, com intervalo de 95% (Wilson), para decidir se o lote precisa
   de nova revisao completa ou se a amostra confirma a qualidade."""
import sys, os, json, glob, csv, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pros2
HERE = os.path.dirname(os.path.abspath(__file__))
MOT = {'nao_aparece': 'e-mail nao aparece na pagina', 'nao_escritorio': 'nao e escritorio/advogado', 'terceiro': 'e-mail de outra empresa',
       'estrangeiro': 'fora do Brasil', 'site_fora': 'site fora do ar', 'outro': 'outro motivo'}
amostra = {d['id']: d for d in json.load(open(os.path.join(HERE, 'estado', 'amostra_conferencia.json')))}
conf = {}
for f in glob.glob(os.path.join(sys.argv[1], '**', '*.json'), recursive=True):
    j = json.load(open(f)); doc = j.get('data', j)
    conf[os.path.splitext(os.path.basename(f))[0]] = doc
def wilson(k, n, z=1.96):
    if not n: return (0, 0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)
for lote in (8, 7):
    ids = [i for i, a in amostra.items() if a['lote'] == lote]
    feitos = [i for i in ids if i in conf]
    bad = [i for i in feitos if conf[i].get('status') == 'problema']
    lo, hi = wilson(len(bad), len(feitos))
    print(f'Lote {lote}: conferidos {len(feitos)}/{len(ids)} | com problema {len(bad)} | taxa de erro estimada {100*lo:.0f}% a {100*hi:.0f}%')
    for i in bad:
        print('   ', amostra[i]['email'], '|', MOT.get(conf[i].get('motivo'), conf[i].get('motivo')), '|', (conf[i].get('nota') or '')[:120])
retirar = {amostra[i]['email'].lower(): conf[i] for i in conf if i in amostra and conf[i].get('status') == 'problema'}
if retirar:
    P = list(csv.reader(open(pros2.P, encoding='utf-8-sig'))); h, b = P[0], P[1:]
    O = list(csv.reader(open(pros2.OUT, encoding='utf-8-sig')))
    fica = []
    for r in b:
        c = retirar.get(r[3].lower())
        if c:
            O.append([r[3], r[1], (c.get('nota') or '')[:300], r[9], r[10], r[13], 'CONFERENCIA HUMANA DA AMOSTRA: ' + MOT.get(c.get('motivo'), str(c.get('motivo')))])
        else:
            fica.append(r)
    for i, r in enumerate(fica, 1): r[0] = f'{i:03d}'
    with open(pros2.P + '.tmp', 'w', newline='', encoding='utf-8-sig') as fh: csv.writer(fh).writerows([h] + fica)
    os.replace(pros2.P + '.tmp', pros2.P)
    with open(pros2.OUT + '.tmp', 'w', newline='', encoding='utf-8-sig') as fh: csv.writer(fh).writerows(O)
    os.replace(pros2.OUT + '.tmp', pros2.OUT)
    print('retirados da base:', len(b) - len(fica), '| depois rode build_xlsx_500.py')
