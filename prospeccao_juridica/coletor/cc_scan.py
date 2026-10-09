# -*- coding: utf-8 -*-
"""Varredura generica do indice Common Crawl (cluster.idx + blocos cdx via Range) por faixa SURT e regex de host.
Uso: python3 cc_scan.py EDICAO PREFIXO REGEX_NOME SAIDA THREADS
Saida: ccidx/<SAIDA>_hosts.json {host: {ok, paths}} ; ccidx/<SAIDA>_done.json ; ccidx/<SAIDA>.done ao terminar."""
import sys, os, re, json, gzip, time, bisect, threading, requests
from concurrent.futures import ThreadPoolExecutor
CA = '/root/.ccr/ca-bundle.crt'
ED, PREF, RXN, OUTN, TH = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ccidx'); os.makedirs(D, exist_ok=True)
BASE = f'https://data.commoncrawl.org/cc-index/collections/{ED}/indexes/'
RX = {
 'OLD': r'advoc|advog|juridic|jurídic|(^|[.-])adv($|[.-])|escritorio|lawyer|law($|[.-])',
 'NEW': r'direito|previdenci|trabalhist|tributari|associados|consultoriajur|defesad|(^|[.-])causas?($|[.-])',
 'COM': r'advocacia|advogad|juridic|previdenciari|trabalhista|escritoriodeadv',
}
if RXN == 'OLDNEW': HOSTRE = re.compile(RX['OLD'] + '|' + RX['NEW'], re.I)
else: HOSTRE = re.compile(RX[RXN], re.I)
S = requests.Session(); S.headers['User-Agent'] = 'PesquisaJuridicaBot/1.0 (pesquisa de contatos profissionais publicos)'
S.mount('https://', requests.adapters.HTTPAdapter(pool_connections=TH + 4, pool_maxsize=TH + 4))
idx = os.path.join(D, f'cluster_{ED}.idx')
if ED == 'CC-MAIN-2026-30' and not os.path.exists(idx) and os.path.exists(os.path.join(D, 'cluster.idx')):
    os.link(os.path.join(D, 'cluster.idx'), idx)
for t in range(6):
    if os.path.exists(idx) and os.path.getsize(idx) > 50_000_000: break
    try:
        r = S.get(BASE + 'cluster.idx', timeout=600, verify=CA, stream=True)
        with open(idx + '.part', 'wb') as fh:
            for ch in r.iter_content(1 << 20): fh.write(ch)
        os.replace(idx + '.part', idx)
    except Exception as e:
        print('erro baixando cluster.idx', e, flush=True); time.sleep(30 * (t + 1))
lines = open(idx, encoding='utf-8', errors='replace').read().splitlines()
keys = [l.split('\t')[0].split(' ')[0] for l in lines]
lo = bisect.bisect_left(keys, PREF); hi = bisect.bisect_left(keys, PREF + '\xff')
blocks = [l.split('\t') for l in lines[max(lo - 1, 0):hi]]
del lines, keys
OUT = os.path.join(D, OUTN + '_hosts.json'); DONE = os.path.join(D, OUTN + '_done.json')
hosts = json.load(open(OUT)) if os.path.exists(OUT) else {}
done = set(json.load(open(DONE))) if os.path.exists(DONE) else set()
lock = threading.Lock()
print(ED, PREF, RXN, 'blocos', len(blocks), 'ja feitos', len(done), flush=True)

def work(b):
    fname, off, ln, bid = b[1], int(b[2]), int(b[3]), b[4]
    if bid in done: return 0
    data = None
    for t in range(8):
        try:
            r = S.get(BASE + fname, headers={'Range': f'bytes={off}-{off+ln-1}'}, timeout=120, verify=CA)
            if r.status_code in (200, 206) and len(r.content) == ln: data = r.content; break
            time.sleep(4 * (t + 1))
        except Exception:
            time.sleep(4 * (t + 1))
    if data is None: return -1
    try: txt = gzip.decompress(data).decode('utf-8', 'replace')
    except Exception: return -1
    found = {}
    for line in txt.splitlines():
        sp = line.split(' ', 2)
        if len(sp) < 3 or not sp[0].startswith(PREF): continue
        h = '.'.join(reversed(sp[0].split(')')[0].split(',')))
        if not HOSTRE.search(h): continue
        st = '"status": "200"' in sp[2]
        d = found.setdefault(h, {'ok': 0, 'paths': []})
        if st:
            d['ok'] += 1
            p = sp[0].split(')', 1)[1] if ')' in sp[0] else '/'
            if len(d['paths']) < 10: d['paths'].append(p)
    with lock:
        for h, d in found.items():
            e = hosts.setdefault(h, {'ok': 0, 'paths': []}); e['ok'] += d['ok']; e['paths'] = (e['paths'] + d['paths'])[:20]
        done.add(bid)
    return 1

for passe in (1, 2, 3):
    t0 = time.time(); nb = fail = 0
    with ThreadPoolExecutor(TH) as ex:
        for res in ex.map(work, blocks):
            nb += 1; fail += (res == -1)
            if nb % 500 == 0:
                with lock: json.dump(hosts, open(OUT, 'w')); json.dump(sorted(done), open(DONE, 'w'))
                print(f'passe {passe} {nb}/{len(blocks)} | hosts {len(hosts)} | falhas {fail} | {time.time()-t0:.0f}s', flush=True)
    with lock: json.dump(hosts, open(OUT, 'w')); json.dump(sorted(done), open(DONE, 'w'))
    print(f'FIM passe {passe}: hosts {len(hosts)} | falhas {fail}', flush=True)
    if fail == 0: break
open(os.path.join(D, OUTN + '.done'), 'w').write('ok')
