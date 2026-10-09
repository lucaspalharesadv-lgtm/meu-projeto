# -*- coding: utf-8 -*-
"""Enriquece cada e-mail das planilhas com perfil do site oficial. Resultado em enrich_cache.json (chave = e-mail)."""
import sys, os, re, csv, json, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web, perfil as PF
from concurrent.futures import ThreadPoolExecutor
BASE = '/home/user/meu-projeto/prospeccao_juridica'
WEBMAIL = {'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br', 'yahoo.com', 'live.com', 'uol.com.br', 'bol.com.br', 'terra.com.br', 'icloud.com', 'hotmail.com.br', 'outlook.com.br', 'ig.com.br'}
AGGR = re.compile(r'oab|jurisvagas|rotajuridica|indeed|bne\.com|infojobs|gupy|nunchi|vagas\.com|linkedin|facebook|instagram|migalhas|jusbrasil|google', re.I)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'enrich_cache.json')
cache = json.load(open(OUT)) if os.path.exists(OUT) else {}

def site_for(email, fonte):
    dom = email.split('@')[1].lower()
    c = []
    if dom not in WEBMAIL:
        c += [f'https://www.{dom}/', f'https://{dom}/']
    if fonte and fonte.startswith('http'):
        fd = urllib.parse.urlsplit(fonte).netloc
        if not AGGR.search(fd):
            c.insert(0 if dom in WEBMAIL else len(c), f'https://{fd}/')
    return list(dict.fromkeys(c))

def one(args):
    email, fonte, uf = args
    for s in site_for(email, fonte):
        try:
            p = PF.perfil(s)
        except Exception:
            p = None
        if p:
            ufs = {c.split('/')[-1] for c in p['cidades']}
            alerta = ''
            if uf and uf not in ('BR', '') and ufs and uf not in ufs:
                alerta = f"CONFERIR LOCAL: a planilha diz {uf}, mas o site cita {', '.join(p['cidades'][:3])}"
            return email, {'site': s, 'perfil': p, 'alerta': alerta}
    return email, {'site': '', 'perfil': None, 'alerta': ''}

def run(files):
    todo = []
    for f in files:
        rows = list(csv.reader(open(f, encoding='utf-8-sig'))); h = rows[0]
        ie, ifo, iuf = h.index('E-mail'), h.index('Fonte (link)'), h.index('Estado')
        for r in rows[1:]:
            if r[ie] not in cache:
                todo.append((r[ie], r[ifo], r[iuf]))
    print('a enriquecer', len(todo), flush=True)
    with ThreadPoolExecutor(12) as ex:
        for n, (e, r) in enumerate(ex.map(one, todo), 1):
            cache[e] = r
            if n % 25 == 0:
                json.dump(cache, open(OUT, 'w'), ensure_ascii=False); print(n, flush=True)
    json.dump(cache, open(OUT, 'w'), ensure_ascii=False)
    print('FIM', len(cache), 'com perfil:', sum(1 for v in cache.values() if v['perfil']), flush=True)

if __name__ == '__main__':
    run(sys.argv[1:])
