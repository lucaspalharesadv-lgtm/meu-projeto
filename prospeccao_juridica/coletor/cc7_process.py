# -*- coding: utf-8 -*-
"""Lote 7: dominios do grafo de links do Common Crawl (wg_novos.json) -> site oficial -> e-mails + perfil.
Pula tudo que ja esta em estado/hosts_ja_vistos.json e em estado/cc7_done_*.json (TAG=nome do processo).
Uso: python3 cc7_process.py CATEGORIA1[,CATEGORIA2] [LIMITE] [SEMENTE_AMOSTRA]
Saida: estado/cc7_done_<TAG>.json {dominio: status} e cc7_cands_<TAG>.json {dominio: candidato} (mesmo formato de cc_cands.json)."""
import sys, os, re, json, random, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web, perfil as PF, jv_process as J
from fixenc import fix
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(HERE, 'estado')
LEGAL = re.compile(r'advog|advocacia|jur[ií]dic|direito|escrit[oó]rio|oab', re.I)
PARKED = re.compile(r'dom[ií]nio (est[aá] )?(registrado|[àa] venda)|this domain|parked|em constru[cç][aã]o|coming soon|site em manuten|hostgator|locaweb.*(default|padr[aã]o)|index of /|domain (is )?for sale|comprar este dom[ií]nio', re.I)

cats = sys.argv[1].split(',')
limit = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != '0' else None
seed = int(sys.argv[3]) if len(sys.argv) > 3 else None
W = json.load(open(os.path.join(HERE, 'ccidx', 'wg_novos.json')))
VIS_P = os.path.join(EST, 'hosts_ja_vistos.json')
TAG = os.environ.get('TAG', 'x')
DONE_P = os.path.join(EST, f'cc7_done_{TAG}.json')
CAND_P = os.path.join(HERE, f'cc7_cands_{TAG}.json')
vis = json.load(open(VIS_P))
import glob
for f in glob.glob(os.path.join(EST, 'cc7_done_*.json')):   # outros processos paralelos / rodadas anteriores
    vis += list(json.load(open(f)))
visn = {h.replace('www.', '') for h in vis}
done = json.load(open(DONE_P)) if os.path.exists(DONE_P) else {}
cands = json.load(open(CAND_P)) if os.path.exists(CAND_P) else {}

T = []
for c in cats:
    k = [x for x in W if x.startswith(c + ' ')][0]
    # mais edicoes do grafo = dominio mais estavel/vivo: visita primeiro
    lst = sorted(W[k], key=lambda x: -x[1])
    T += [(d, k) for d, n in lst if d not in visn and d not in done]
if os.environ.get('SHARD'):      # SHARD=k/n: este processo pega so 1 de cada n dominios (processos paralelos sem repeticao)
    k, nsh = map(int, os.environ['SHARD'].split('/'))
    T = T[k::nsh]
if seed is not None:
    random.Random(seed).shuffle(T)
if limit:
    T = T[:limit]
print('dominios a visitar', len(T), flush=True)
lock = threading.Lock()


def work(item):
    d, k = item
    try:
        p = None
        for home in ('https://' + d + '/', 'https://www.' + d + '/', 'http://www.' + d + '/'):
            p = web.site_profile(home, max_pages=4)
            if p:
                break
        if not p:
            return d, {'st': 'sem acesso'}
        hd = web.fetch(p['final'])
        txt = fix(web.text_of(hd['html']))[:20000] if hd else ''
        if PARKED.search(txt[:3000]) and not p['ctx']:
            return d, {'st': 'estacionado'}
        if not LEGAL.search(p['title'] + ' ' + txt[:6000]):
            return d, {'st': 'nao juridico', 'title': p['title']}
        picked = J.pick(p)
        if not picked:
            return d, {'st': 'sem email', 'title': p['title']}
        pr = PF.perfil(p['final'])
        return d, {'st': 'ok', 'site': p['final'], 'title': fix(p['title']), 'cat': k,
                   'picked': [(e, t, u, fix(c)) for e, t, u, c in picked], 'perfil': pr}
    except Exception as ex:
        return d, {'st': 'erro', 'err': str(ex)[:120]}


def save():
    with lock:
        for path, obj in ((DONE_P, done), (CAND_P, cands)):   # hosts_ja_vistos e atualizado no fim (cc7_merge)
            with open(path + '.tmp', 'w') as fh:
                json.dump(obj, fh, ensure_ascii=False)
            os.replace(path + '.tmp', path)


with ThreadPoolExecutor(int(os.environ.get('THREADS', '48'))) as ex:
    for n, (d, r) in enumerate(ex.map(work, T), 1):
        with lock:
            done[d] = r['st']
            if r['st'] == 'ok':
                cands[d] = r
        if n % 50 == 0:
            save()
            from collections import Counter
            print(n, 'visitados |', len(cands), 'com e-mail |', dict(Counter(done[x[0]] for x in T[:n])), flush=True)
save()
print('FIM', len(cands), 'com e-mail', flush=True)
