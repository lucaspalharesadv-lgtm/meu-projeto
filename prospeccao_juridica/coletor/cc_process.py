# -*- coding: utf-8 -*-
"""Hosts .adv.br (Common Crawl) -> site oficial -> e-mails + perfil. Gera cc_cands.json para revisao."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web, perfil as PF, jv_process as J
from fixenc import fix
from concurrent.futures import ThreadPoolExecutor
LEGAL = re.compile(r'advog|advocacia|jur[ií]dic|direito|escrit[oó]rio|oab', re.I)
PARKED = re.compile(r'dom[ií]nio (est[aá] )?(registrado|[àa] venda)|this domain|parked|em constru[cç][aã]o|coming soon|site em manuten|hostgator|locaweb.*(default|padr[aã]o)|index of /', re.I)
hosts = json.load(open(sys.argv[1]))
done = json.load(open('cc_done.json')) if os.path.exists('cc_done.json') else {}
cands = json.load(open('cc_cands.json')) if os.path.exists('cc_cands.json') else {}
todo = [h for h in hosts if h not in done]
# um host por site (sem www duplicado)
seen = set(); T = []
for h in todo:
    k = h.replace('www.', '')
    if k in seen: continue
    seen.add(k); T.append(h)
print('hosts a visitar', len(T), flush=True)

def work(h):
    try:
        home = 'https://' + h + '/'
        p = web.site_profile(home, max_pages=4)
        if not p:
            p = web.site_profile('http://' + h + '/', max_pages=4)
        if not p:
            return h, {'st': 'sem acesso'}
        hd = web.fetch(p['final'])
        txt = fix(web.text_of(hd['html']))[:20000] if hd else ''
        if PARKED.search(txt[:3000]) and not p['ctx']:
            return h, {'st': 'estacionado'}
        if not (LEGAL.search(p['title'] + ' ' + txt[:6000])):
            return h, {'st': 'nao juridico', 'title': p['title']}
        picked = J.pick(p)
        if not picked:
            return h, {'st': 'sem email', 'title': p['title']}
        pr = PF.perfil(p['final'])
        return h, {'st': 'ok', 'site': p['final'], 'title': fix(p['title']), 'picked': [(e, t, u, fix(c)) for e, t, u, c in picked], 'perfil': pr}
    except Exception as ex:
        return h, {'st': 'erro', 'err': str(ex)[:120]}

with ThreadPoolExecutor(48) as ex:
    for n, (h, r) in enumerate(ex.map(work, T), 1):
        done[h] = r['st']
        if r['st'] == 'ok':
            cands[h] = r
        if n % 25 == 0:
            json.dump(done, open('cc_done.json', 'w')); json.dump(cands, open('cc_cands.json', 'w'), ensure_ascii=False)
            print(n, 'visitados |', len(cands), 'com e-mail', flush=True)
json.dump(done, open('cc_done.json', 'w')); json.dump(cands, open('cc_cands.json', 'w'), ensure_ascii=False)
print('FIM', len(cands), 'com e-mail', flush=True)
