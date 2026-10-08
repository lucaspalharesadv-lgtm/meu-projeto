# -*- coding: utf-8 -*-
"""Radar de vagas juridicas no portal publico da Gupy (portal.gupy.io, robots.txt libera tudo).
Le a lista de vagas embutida na pagina de busca (sem login, sem API privada), filtra vagas juridicas
remotas ou em Rondonia e mostra so as que ainda nao foram vistas. Nao envia nada, nao se candidata.
Uso: python3 rotina/vagas_gupy.py [--all]   (--all ignora o historico de vistas)"""
import os, re, sys, json, time, html, requests
D = os.path.dirname(os.path.abspath(__file__))
SEEN = os.path.join(D, 'gupy_vistas.json')
OUT = os.path.join(D, 'vagas_gupy.json')
CA = os.environ.get('REQUESTS_CA_BUNDLE') or ('/root/.ccr/ca-bundle.crt' if os.path.exists('/root/.ccr/ca-bundle.crt') else True)
TERMS = ['advogado', 'advogada', 'jurídico']
PAGES = 4
JUR = re.compile(r'advoga|jur[ií]dic|legal|direito|contencioso|previdenci|trabalhista|tribut', re.I)
NEG = re.compile(r'est[aá]gi|estagi[aá]rio|jovem aprendiz|aprendiz|assistente|auxiliar|recepcion|sdr|comercial|vendas|closer|secret[aá]ri', re.I)
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (compatible; RadarVagasLP/1.0)'

def page(term, p):
    u = f'https://portal.gupy.io/job-search/term={requests.utils.quote(term)}&page={p}'
    r = S.get(u, timeout=60, verify=CA)
    h = r.text; i = h.find('[{"id":')
    if i < 0: return []
    try:
        arr, _ = json.JSONDecoder().raw_decode(h[i:])
    except Exception:
        return []
    return arr

def main():
    allf = '--all' in sys.argv
    seen = set(json.load(open(SEEN))) if os.path.exists(SEEN) and not allf else set()
    jobs = {}
    for t in TERMS:
        for p in range(1, PAGES + 1):
            try:
                arr = page(t, p)
            except Exception as e:
                print('erro', t, p, str(e)[:80], file=sys.stderr); break
            if not arr: break
            for j in arr: jobs[j['id']] = j
            time.sleep(1.5)
    novas = []
    for j in jobs.values():
        name = j.get('name', '') or ''
        if not JUR.search(name) or NEG.search(name): continue
        wt = j.get('workplaceType', ''); st = (j.get('state') or '')
        if not (wt == 'remote' or st == 'Rondônia'): continue
        if j['id'] in seen: continue
        desc = html.unescape(re.sub(r'<[^>]+>', ' ', j.get('description', '') or ''))
        emails = sorted(set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', desc)))
        novas.append({'id': j['id'], 'titulo': name.strip(), 'empresa': (j.get('careerPageName') or '').strip(), 'modalidade': wt,
                      'cidade': j.get('city') or '', 'uf': st, 'tipo': j.get('type', ''), 'publicada': (j.get('publishedDate') or '')[:10],
                      'prazo': (j.get('applicationDeadline') or '')[:10], 'link': (j.get('jobUrl') or '').split('?')[0], 'emails': emails,
                      'resumo': re.sub(r'\s+', ' ', desc)[:400]})
    novas.sort(key=lambda x: x['publicada'], reverse=True)
    json.dump(novas, open(OUT, 'w'), ensure_ascii=False, indent=1)
    if not allf:
        json.dump(sorted(seen | {n['id'] for n in novas}), open(SEEN, 'w'))
    print(f'{len(jobs)} vagas lidas | {len(novas)} juridicas remotas/RO novas')
    for n in novas:
        print(f"- [{n['titulo']}]({n['link']}) — {n['empresa']} — {n['modalidade']}{(' ' + n['cidade'] + '/' + n['uf']) if n['cidade'] else ''} — publicada {n['publicada']}" + (f" — e-mail no anúncio: {', '.join(n['emails'])}" if n['emails'] else ''))

if __name__ == '__main__':
    main()
