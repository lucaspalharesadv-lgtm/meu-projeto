# -*- coding: utf-8 -*-
"""Terceira passada: tenta enderecos de pagina comuns que nao estavam no menu do site
(politica de privacidade, LGPD, equipe, socios, contato). Respeita robots.txt.
Uso: TAG=g0 THREADS=50 SHARD=k/n python3 lgpd_pass2.py [limite]"""
import sys, os, re, json, threading, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web, perfil as PF, jv_process as J
from fixenc import fix
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); EST = os.path.join(HERE, 'estado')
TAG = os.environ.get('TAG', 'g')
DONE_P = os.path.join(EST, f'lgpd2_done_{TAG}.json'); CAND_P = os.path.join(HERE, f'lgpd2_cands_{TAG}.json')
LEGAL = re.compile(r'advog|advocacia|jur[ií]dic|direito|escrit[oó]rio|oab', re.I)
PATHS = ['/politica-de-privacidade/', '/politica-de-privacidade', '/privacidade/', '/politica-privacidade/',
         '/lgpd/', '/termos-de-uso/', '/termos/', '/equipe/', '/nossa-equipe/', '/socios/', '/advogados/',
         '/contato/', '/contatos/', '/fale-conosco/', '/atendimento/', '/quem-somos/', '/sobre-nos/', '/sobre/']
hosts = json.load(open(os.path.join(EST, 'sem_email2.json')))
done = json.load(open(DONE_P)) if os.path.exists(DONE_P) else {}
cands = json.load(open(CAND_P)) if os.path.exists(CAND_P) else {}
T = [h for h in hosts if h not in done]
if os.environ.get('SHARD'):
    k, n = map(int, os.environ['SHARD'].split('/')); T = T[k::n]
if len(sys.argv) > 1 and sys.argv[1] != '0': T = T[:int(sys.argv[1])]
print('hosts', len(T), flush=True)
lock = threading.Lock()

def work(h):
    try:
        base = None
        for home in ('https://' + h + '/', 'http://' + h + '/'):
            d = web.fetch(home)
            if d: base = d['final']; break
        if not base: return h, {'st': 'sem acesso'}
        d0 = web.fetch(base); html0 = d0['html'] if d0 else ''
        ctx = {}; pgs = []; txt = fix(web.text_of(html0))[:8000]
        for p in PATHS:
            u = urllib.parse.urljoin(base, p)
            dd = web.fetch(u)
            if not dd or dd.get('status') != 200: continue
            em = web.emails_in(dd['html'])
            if em:
                pgs.append((u, web.title_of(dd['html'])[:70], em))
                txt += ' ' + fix(web.text_of(dd['html']))[:3000]
                for e, c in web.contexts(dd['html'], em).items(): ctx.setdefault(e, (u, c))
            if len(ctx) >= 2: break
        if not ctx: return h, {'st': 'sem email'}
        if not LEGAL.search((web.title_of(html0) or '') + ' ' + txt[:8000]): return h, {'st': 'nao juridico'}
        prof = {'home': base, 'final': base, 'title': web.title_of(html0), 'pages': pgs, 'ctx': ctx}
        picked = J.pick(prof)
        if not picked: return h, {'st': 'sem email'}
        return h, {'st': 'ok', 'site': base, 'title': fix(web.title_of(html0) or ''), 'cat': 'lgpd2',
                   'picked': [(e, t, u, fix(c)) for e, t, u, c in picked], 'perfil': PF.perfil(base)}
    except Exception as ex:
        return h, {'st': 'erro', 'err': str(ex)[:120]}

def save():
    with lock:
        for path, obj in ((DONE_P, done), (CAND_P, cands)):
            with open(path + '.tmp', 'w') as fh: json.dump(obj, fh, ensure_ascii=False)
            os.replace(path + '.tmp', path)

with ThreadPoolExecutor(int(os.environ.get('THREADS', '50'))) as ex:
    for n, (h, r) in enumerate(ex.map(work, T), 1):
        with lock:
            done[h] = r['st']
            if r['st'] == 'ok': cands[h] = r
        if n % 100 == 0: save(); print(n, '|', len(cands), 'com e-mail |', dict(Counter(done.values())), flush=True)
save(); print('FIM', len(cands), 'com e-mail', flush=True)
