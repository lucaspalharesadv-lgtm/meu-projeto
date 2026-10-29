# -*- coding: utf-8 -*-
"""Lista A: minera o cache de paginas ja baixadas (8,5 GB, 113 mil hosts) procurando SINAL DE EMPREGADOR,
nao mais volume de e-mail. Nada de rede: le so o que esta em disco.
Pontua cada site por: endereco de RH (rh@, vagas@, curriculo@, talentos@, selecao@...), area de carreiras,
mencao a trabalho remoto ou home office na pagina, vaga de advogado escrita no site, contencioso de massa e
atuacao nacional. Guarda tambem empresa que nao e escritorio mas tem departamento juridico, que e o que o
Lucas pediu ("qualquer empresa que precise de juridico") e que os filtros das rodadas anteriores descartavam.
Saida: mina_empregadores.json, ordenado por pontuacao."""
import json, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web
from fixenc import fix

RH = re.compile(r'^(rh|vagas?|curriculos?|talentos?|recrutamento|selecao|sele[cç][aã]o|carreiras?|trabalheconosco|'
                r'trabalhe|pessoas|dp|gentee?gestao|gestaodepessoas|recursoshumanos)@', re.I)
REMOTO = re.compile(r'home.?office|100% remoto|trabalho remoto|totalmente remoto|remotamente|teletrabalho|'
                    r'anywhere office|modelo h[ií]brido|trabalho h[ií]brido|vaga remota|atua[cç][aã]o remota', re.I)
VAGA_ADV = re.compile(r'(vaga|oportunidade|contrata[- ]?se|estamos contratando|buscamos|procuramos|selecionamos)'
                      r'[^.]{0,80}(advogad|jur[ií]dic|estagi[aá]ri)', re.I)
DEPTO = re.compile(r'departamento jur[ií]dico|juridico interno|jur[ií]dico pr[oó]prio|equipe jur[ií]dica|'
                   r'setor jur[ií]dico|assessoria jur[ií]dica pr[oó]pria', re.I)
CARREIRA_PG = re.compile(r'trabalhe.?conosco|fa[cç]a parte|banco de talentos|carreiras?|oportunidades|'
                         r'junte-se|venha ser', re.I)

def paginas(v):
    us = [v.get('site')]
    for e, tipo, pg, ctx in (v.get('picked') or []):
        us.append(pg)
    for x in (v.get('pages') or []):
        us.append(x[0] if isinstance(x, (list, tuple)) else x)
    out, seen = [], set()
    for u in us:
        if u and u not in seen:
            seen.add(u); out.append(u)
    return out[:8]

sites = {}
for f in sorted(glob.glob('cc7_cands_*.json') + glob.glob('cc_cands*.json') + glob.glob('jv_cands*.json')):
    try: c = json.load(open(f))
    except Exception: continue
    for k, v in c.items():
        if k not in sites: sites[k] = v
print('sites em cache:', len(sites), flush=True)

res = []
n = 0
for host, v in sites.items():
    n += 1
    if n % 2000 == 0: print('  lidos', n, flush=True)
    picked = v.get('picked') or []
    if not picked: continue
    p = v.get('perfil') or {}
    txt = ''
    for u in paginas(v):
        d = web._cache_read(u)
        if d: txt += ' ' + fix(web.text_of(d['html']))[:40000]
    tl = txt.lower()
    rh = [e for e, *_ in picked if RH.search(e)]
    pts = 0
    por = []
    if rh: pts += 4; por.append('endereco de RH: ' + ', '.join(sorted(set(rh))[:3]))
    if p.get('carreiras'): pts += 2; por.append("site tem 'trabalhe conosco'")
    m = REMOTO.search(txt)
    if m: pts += 4; por.append('site fala de trabalho remoto: "%s"' % m.group(0)[:40])
    m2 = VAGA_ADV.search(txt)
    if m2: pts += 4; por.append('vaga juridica escrita no site: "%s"' % re.sub(r'\s+', ' ', m2.group(0))[:70])
    m3 = DEPTO.search(txt)
    if m3: pts += 3; por.append('tem departamento juridico proprio: "%s"' % m3.group(0)[:40])
    if p.get('volume'): pts += 2; por.append('contencioso de massa')
    if p.get('nacional'): pts += 1; por.append('atua em todo o Brasil')
    if pts >= 4:
        res.append({'host': host, 'pontos': pts, 'porque': por, 'emails': [list(x) for x in picked],
                    'rh': sorted(set(rh)), 'perfil': p, 'site': v.get('site'), 'title': v.get('title', '')})
res.sort(key=lambda x: -x['pontos'])
json.dump(res, open('mina_empregadores.json', 'w'), ensure_ascii=False)
from collections import Counter
print('sites com sinal de empregador (4+ pontos):', len(res))
print('distribuicao de pontos:', sorted(Counter(x['pontos'] for x in res).items(), reverse=True))
print('com endereco de RH:', sum(1 for x in res if x['rh']))
print('que falam de remoto:', sum(1 for x in res if any('remoto' in y for y in x['porque'])))
print('com vaga juridica escrita:', sum(1 for x in res if any('vaga juridica' in y for y in x['porque'])))
print('com departamento juridico proprio:', sum(1 for x in res if any('departamento juridico' in y for y in x['porque'])))
