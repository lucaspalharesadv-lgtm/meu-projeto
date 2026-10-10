# -*- coding: utf-8 -*-
"""Grava um lote novo na base (LOTE=8 python3 add7.py ...; padrao 7, o primeiro lote feito com este script).
Uso: python3 add7.py cc7_rows_out.json [retirar.json]
1) tira as linhas que a revisao mandou retirar (lista de e-mails em retirar.json, com o motivo);
2) valida o MX de todos os dominios em paralelo (DNS por HTTPS, sem enviar nada);
3) pros2.add() (deduplica contra as tres planilhas) e remove quem ficou sem MX (mesma regra do dropbad.py);
4) grava estado/lote<LOTE>_emails.json e as colunas de personalizacao (enrich_cache.json) a partir do perfil
   ja lido no site oficial durante a visita (nada novo e inventado)."""
import sys, os, json, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pros2
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(HERE, 'estado')
LOTE = int(os.environ.get('LOTE', '7'))
rows = json.load(open(sys.argv[1]))
retirar = {}
if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
    retirar = {d['email'].lower(): d.get('motivo', '') for d in json.load(open(sys.argv[2]))}
antes = len(rows)
fora = [r for r in rows if r['email'].lower() in retirar]
rows = [r for r in rows if r['email'].lower() not in retirar]
# endereco "cortado" por erro de digitacao do proprio site (ex.: link mailto:contato@x.com e texto contato@x.com.br):
# troca pela versao completa SO quando ela tambem esta escrita literalmente na pagina e e o dominio do proprio site.
import web, urllib.parse
trocas = 0
for r in rows:
    pg = web._cache_read(r['fonte'])
    if not pg:
        continue
    e = r['email'].lower(); h = pg['html'].lower()
    site = urllib.parse.urlsplit(pg.get('final') or r['fonte']).netloc.lower().replace('www.', '')
    for suf in set(re.findall(re.escape(e) + r'(\.[a-z]{2,6})\b', h)):
        if e.split('@')[1] + suf == site:
            r['email'] = e + suf
            r['obs'] += f' (Endereco completo {e + suf}, escrito na pagina; o site tambem traz a forma incompleta {e}.)'
            trocas += 1
            break
print('enderecos completados (versao literal da pagina)', trocas, flush=True)

# e-mail repetido (mesmo endereco achado em varios sites do mesmo escritorio) e no maximo 2 por dominio de e-mail
WEBMAIL = pros2.WEBMAIL | {'outlook.com.br', 'hotmail.com.br', 'yahoo.com', 'live.com'}
vistos, pordom, uniq = set(), {}, []
for r in rows:
    e = r['email'].lower(); dm = e.split('@')[1]
    if e in vistos:
        continue
    if dm not in WEBMAIL and pordom.get(dm, 0) >= 2:
        continue
    vistos.add(e); pordom[dm] = pordom.get(dm, 0) + 1; uniq.append(r)
print('linhas', antes, '| retiradas pela revisao', len(fora), '| unicas (max 2 por dominio de e-mail)', len(uniq), flush=True)
rows = uniq

# 2) MX em paralelo (pros2.mx guarda no cache; add() depois so le o cache)
doms = sorted({r['email'].split('@')[1].lower() for r in rows})
with ThreadPoolExecutor(32) as ex:
    res = list(ex.map(lambda d: pros2.mx('x@' + d), doms))
falhas = [d for d, v in zip(doms, res) if v == 'Falha na consulta']
for d in falhas:                      # segunda tentativa, em serie
    pros2.mx('x@' + d)
print('dominios', len(doms), '| MX ok', sum(1 for d in doms if pros2._mx.get(d, '').startswith('MX ok')), flush=True)

# lotes anteriores (para saber quem e novo)
old = set()
for n in range(1, LOTE):
    old |= {e.strip().lower() for e in json.load(open(os.path.join(EST, f'lote{n}_emails.json')))}
pros2.add(rows)

# 3) sem MX -> sai da base e vai para 'outros' (igual dropbad.py)
P = list(csv.reader(open(pros2.P, encoding='utf-8-sig'))); h, b = P[0], P[1:]
bad = [r for r in b if not r[15].startswith('MX ok')]
b = [r for r in b if r[15].startswith('MX ok')]
for i, r in enumerate(b, 1):
    r[0] = f'{i:03d}'
with open(pros2.P + '.tmp', 'w', newline='', encoding='utf-8-sig') as fh:
    csv.writer(fh).writerows([h] + b)
os.replace(pros2.P + '.tmp', pros2.P)
O = list(csv.reader(open(pros2.OUT, encoding='utf-8-sig')))
oset = {r[0].strip().lower() for r in O[1:]}
for r in bad:
    if r[3].lower() not in oset:
        O.append([r[3], r[1], '', r[9], r[10], r[13], 'DOMINIO SEM SERVIDOR DE E-MAIL: ' + r[15]])
for r in fora:                        # retirados pela revisao ficam registrados (para nunca voltarem)
    if r['email'].lower() not in oset:
        O.append([r['email'], r['org'], '', r.get('cidade', ''), r.get('uf', ''), r['fonte'],
                  f'REVISAO DO LOTE {LOTE}: ' + retirar[r['email'].lower()][:200]])
with open(pros2.OUT + '.tmp', 'w', newline='', encoding='utf-8-sig') as fh:
    csv.writer(fh).writerows(O)
os.replace(pros2.OUT + '.tmp', pros2.OUT)
print('sem MX retirados', len(bad), [r[3] for r in bad][:10], flush=True)

# 4) lote 7 + personalizacao
novos = sorted(r[3].strip().lower() for r in b if r[3].strip().lower() not in old)
json.dump(novos, open(os.path.join(EST, f'lote{LOTE}_emails.json'), 'w'))
cands = json.load(open(os.path.join(HERE, 'cc7_cands_all.json') if os.path.exists(os.path.join(HERE, 'cc7_cands_all.json')) else os.path.join(EST, f'cc7_cands_lote{LOTE}.json')))
by_email = {}
for d, c in cands.items():
    for e, *_ in c['picked']:
        by_email.setdefault(e.lower(), c)
ENRP = os.path.join(HERE, 'enrich_cache.json')
enr = json.load(open(ENRP)) if os.path.exists(ENRP) else {}
uf_of = {r[3].strip().lower(): r[10] for r in b}
for e in novos:
    c = by_email.get(e)
    if not c or not c.get('perfil'):
        continue
    p = c['perfil']; uf = uf_of.get(e, '')
    ufs = {x.split('/')[-1] for x in p.get('cidades', [])}
    alerta = ''
    if uf and uf not in ('BR', '') and ufs and uf not in ufs:
        alerta = f"CONFERIR LOCAL: a planilha diz {uf}, mas o site cita {', '.join(p['cidades'][:3])}"
    enr[e] = {'site': c['site'], 'perfil': p, 'alerta': alerta}
json.dump(enr, open(ENRP, 'w'), ensure_ascii=False)
print(f'LOTE {LOTE}:', len(novos), 'e-mails novos | total na base', len(b), '| com perfil', sum(1 for e in novos if e in enr), flush=True)
