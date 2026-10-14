# -*- coding: utf-8 -*-
"""Segunda passada nos escritorios que ficaram 'sem email': procura o e-mail nas paginas de
politica de privacidade / LGPD / termos / equipe / socios, e no sitemap.xml.
Respeita robots.txt (web.fetch). Nao envia nada.
Uso: THREADS=40 SHARD=k/n python3 lgpd_pass.py [limite]
Saida: estado/lgpd_done_<TAG>.json e lgpd_cands_<TAG>.json (formato de cc_cands.json)."""
import sys, os, re, json, threading, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web, perfil as PF, jv_process as J
from fixenc import fix
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); EST = os.path.join(HERE, 'estado')
TAG = os.environ.get('TAG', 'x')
DONE_P = os.path.join(EST, f'lgpd_done_{TAG}.json'); CAND_P = os.path.join(HERE, f'lgpd_cands_{TAG}.json')
LEGAL = re.compile(r'advog|advocacia|jur[ií]dic|direito|escrit[oó]rio|oab', re.I)
# paginas onde o e-mail costuma aparecer mesmo quando a home nao mostra
KEY2 = re.compile(r'privacidad|privacy|lgpd|prote[cç][aã]o.?de.?dados|termo|cookie|equipe|socio|s[oó]cios|advogados|time|quem.?somos|sobre|institucional|atendimento|ouvidoria|contato|fale', re.I)
hosts = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(EST, 'sem_email_hosts.json')))
done = json.load(open(DONE_P)) if os.path.exists(DONE_P) else {}
cands = json.load(open(CAND_P)) if os.path.exists(CAND_P) else {}
T = [h for h in hosts if h not in done]
if os.environ.get('SHARD'):
    k, n = map(int, os.environ['SHARD'].split('/')); T = T[k::n]
if len(sys.argv) > 1 and sys.argv[1] != '0': T = T[:int(sys.argv[1])]
print('hosts a revisitar', len(T), flush=True)
lock = threading.Lock()

def pages_from_sitemap(base):
    out = []
    for sm in ('sitemap.xml', 'sitemap_index.xml', 'wp-sitemap.xml'):
        d = web.fetch(urllib.parse.urljoin(base, '/' + sm))
        if not d: continue
        locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', d['html'])[:300]
        out += [u for u in locs if KEY2.search(u)]
        if out: break
    return out[:8]

def work(h):
    try:
        base = None
        for home in ('https://' + h + '/', 'http://' + h + '/'):
            d = web.fetch(home)
            if d: base = d['final']; break
        if not base: return h, {'st': 'sem acesso'}
        d0 = web.fetch(base)
        html0 = d0['html'] if d0 else ''
        host0 = urllib.parse.urlsplit(base).netloc.lower().replace('www.', '')
        # links internos com as palavras-chave da segunda passada
        links = []
        for href, atxt in web.anchors_of(html0):
            u = urllib.parse.urljoin(base, href.split('#')[0])
            p = urllib.parse.urlsplit(u)
            if p.scheme not in ('http', 'https'): continue
            if p.netloc.lower().replace('www.', '') != host0: continue
            if KEY2.search(p.path) or KEY2.search(atxt):
                if u not in links and u.rstrip('/') != base.rstrip('/'): links.append(u)
        if len(links) < 3:
            links += [u for u in pages_from_sitemap(base) if u not in links]
        if not links:
            for g in ('/politica-de-privacidade/', '/politica-de-privacidade', '/privacidade/', '/lgpd/', '/termos-de-uso/', '/equipe/', '/contato/'):
                links.append(urllib.parse.urljoin(base, g))
        ctx = {}; pgs = []
        txtall = fix(web.text_of(html0))[:8000]
        for u in links[:8]:
            dd = web.fetch(u)
            if not dd: continue
            em = web.emails_in(dd['html'])
            pgs.append((u, web.title_of(dd['html'])[:70], em))
            txtall += ' ' + fix(web.text_of(dd['html']))[:4000]
            for e, c in web.contexts(dd['html'], em).items():
                ctx.setdefault(e, (u, c))
        if not LEGAL.search((web.title_of(html0) or '') + ' ' + txtall[:8000]):
            return h, {'st': 'nao juridico'}
        if not ctx: return h, {'st': 'sem email'}
        prof = {'home': base, 'final': base, 'title': web.title_of(html0), 'pages': pgs, 'ctx': ctx}
        picked = J.pick(prof)
        if not picked: return h, {'st': 'sem email'}
        return h, {'st': 'ok', 'site': base, 'title': fix(web.title_of(html0) or ''), 'cat': 'lgpd',
                   'picked': [(e, t, u, fix(c)) for e, t, u, c in picked], 'perfil': PF.perfil(base)}
    except Exception as ex:
        return h, {'st': 'erro', 'err': str(ex)[:120]}

def save():
    with lock:
        for path, obj in ((DONE_P, done), (CAND_P, cands)):
            with open(path + '.tmp', 'w') as fh: json.dump(obj, fh, ensure_ascii=False)
            os.replace(path + '.tmp', path)

from collections import Counter
with ThreadPoolExecutor(int(os.environ.get('THREADS', '40'))) as ex:
    for n, (h, r) in enumerate(ex.map(work, T), 1):
        with lock:
            done[h] = r['st']
            if r['st'] == 'ok': cands[h] = r
        if n % 50 == 0:
            save(); print(n, 'revisitados |', len(cands), 'com e-mail |', dict(Counter(list(done.values())[-n:])), flush=True)
save(); print('FIM', len(cands), 'com e-mail', flush=True)
