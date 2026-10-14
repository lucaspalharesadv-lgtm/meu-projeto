# -*- coding: utf-8 -*-
"""Nova tentativa nos hosts que deram 'sem acesso'. Mesmo criterio do cc7_process.
Uso: TAG=r1 THREADS=60 SHARD=k/n python3 retry_pass.py [limite] [arquivo_de_hosts]"""
import sys, os, re, json, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web, perfil as PF, jv_process as J
from fixenc import fix
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); EST = os.path.join(HERE, 'estado')
TAG = os.environ.get('TAG', 'r')
DONE_P = os.path.join(EST, f'retry_done_{TAG}.json'); CAND_P = os.path.join(HERE, f'retry_cands_{TAG}.json')
LEGAL = re.compile(r'advog|advocacia|jur[ií]dic|direito|escrit[oó]rio|oab', re.I)
PARKED = re.compile(r'dom[ií]nio (est[aá] )?(registrado|[àa] venda)|this domain|parked|em constru[cç][aã]o|coming soon|site em manuten|index of /|domain (is )?for sale|comprar este dom[ií]nio', re.I)
hosts = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(EST, 'sem_acesso_pri.json')))
done = json.load(open(DONE_P)) if os.path.exists(DONE_P) else {}
cands = json.load(open(CAND_P)) if os.path.exists(CAND_P) else {}
T = [h for h in hosts if h not in done]
if os.environ.get('SHARD'):
    k, n = map(int, os.environ['SHARD'].split('/')); T = T[k::n]
if len(sys.argv) > 1 and sys.argv[1] != '0': T = T[:int(sys.argv[1])]
print('hosts a revisitar', len(T), flush=True)
lock = threading.Lock()

def work(h):
    try:
        p = None
        for home in ('https://' + h + '/', 'https://www.' + h + '/', 'http://' + h + '/'):
            p = web.site_profile(home, max_pages=4)
            if p: break
        if not p: return h, {'st': 'sem acesso'}
        hd = web.fetch(p['final'])
        txt = fix(web.text_of(hd['html']))[:20000] if hd else ''
        if PARKED.search(txt[:3000]) and not p['ctx']: return h, {'st': 'estacionado'}
        if not LEGAL.search(p['title'] + ' ' + txt[:6000]): return h, {'st': 'nao juridico', 'title': p['title']}
        picked = J.pick(p)
        if not picked: return h, {'st': 'sem email', 'title': p['title']}
        return h, {'st': 'ok', 'site': p['final'], 'title': fix(p['title']), 'cat': 'retry',
                   'picked': [(e, t, u, fix(c)) for e, t, u, c in picked], 'perfil': PF.perfil(p['final'])}
    except Exception as ex:
        return h, {'st': 'erro', 'err': str(ex)[:120]}

def save():
    with lock:
        for path, obj in ((DONE_P, done), (CAND_P, cands)):
            with open(path + '.tmp', 'w') as fh: json.dump(obj, fh, ensure_ascii=False)
            os.replace(path + '.tmp', path)

with ThreadPoolExecutor(int(os.environ.get('THREADS', '60'))) as ex:
    for n, (h, r) in enumerate(ex.map(work, T), 1):
        with lock:
            done[h] = r['st']
            if r['st'] == 'ok': cands[h] = r
        if n % 100 == 0:
            save(); print(n, '|', len(cands), 'com e-mail |', dict(Counter(done.values())), flush=True)
save(); print('FIM', len(cands), 'com e-mail', flush=True)
