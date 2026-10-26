# -*- coding: utf-8 -*-
"""Baixa a parte .br dos vertices de dominio do grafo de links (edicao nova) ate sair do bloco 'br.'.
Uso: python3 wg10_fetch.py cc-main-2026-aug-sep-oct"""
import sys, os, gzip, requests
ED = sys.argv[1]
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'ccidx'); os.makedirs(D, exist_ok=True)
CA = '/root/.ccr/ca-bundle.crt'
PATHS = os.environ.get('VP', f'projects/hyperlinkgraph/{ED}/domain/{ED}-domain-vertices.txt.gz')
url = 'https://data.commoncrawl.org/' + PATHS
out = os.path.join(D, f'wg10_{ED}_br.tsv')
S = requests.Session(); S.headers['User-Agent'] = 'PesquisaJuridicaBot/1.0 (pesquisa de contatos profissionais publicos)'
n = 0; kept = 0; started = False
with S.get(url, stream=True, timeout=600, verify=CA) as r:
    r.raise_for_status()
    gz = gzip.GzipFile(fileobj=r.raw)
    with open(out, 'w') as fh:
        for line in gz:
            n += 1
            try: s = line.decode('utf-8', 'replace')
            except Exception: continue
            p = s.rstrip('\n').split('\t')
            if len(p) < 2: continue
            rev = p[1]
            if rev.startswith('br.'):
                started = True; fh.write(s); kept += 1
            elif started:
                break
            if n % 5_000_000 == 0: print(n, 'linhas |', kept, 'br', flush=True)
print('FIM linhas', n, '| dominios .br', kept, '->', out, flush=True)
