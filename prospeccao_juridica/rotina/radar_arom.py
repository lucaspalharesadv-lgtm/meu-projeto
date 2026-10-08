# -*- coding: utf-8 -*-
"""Radar de dinheiro publico: varre o Diario Oficial dos Municipios de Rondonia (AROM, diariomunicipal.com.br/arom,
robots.txt libera tudo) atras de credenciamento/contratacao de advogados e assessoria juridica.
Uso: python3 rotina/radar_arom.py [dias=8] [--all]"""
import os, re, sys, json, time, html, datetime, requests
D = os.path.dirname(os.path.abspath(__file__))
SEEN = os.path.join(D, 'arom_vistos.json'); OUT = os.path.join(D, 'arom_hits.json')
CA = os.environ.get('REQUESTS_CA_BUNDLE') or ('/root/.ccr/ca-bundle.crt' if os.path.exists('/root/.ccr/ca-bundle.crt') else True)
TERMOS = ['credenciamento advogados', 'serviços advocatícios', 'assessoria jurídica contratação', 'inexigibilidade advocacia',
          'sociedade de advogados contrato', 'honorários advocatícios contrato', 'advogado dativo', 'chamamento público advogados',
          'assessoria jurídica câmara', 'consultoria jurídica contratação']
POS = re.compile(r'credenciamento|inexigibilidade|dispensa|chamamento|contrata[çc][ãa]o|licita|preg[ãa]o|termo de refer[êe]ncia|contrato|extrato|aviso|edital|dativo', re.I)
ADV = re.compile(r'advocat[íi]cio|advoga[dc]|assessoria jur[íi]dica|servi[çc]os jur[íi]dicos|sociedade de advogados|consultoria jur[íi]dica|dativo', re.I)
NEG = re.compile(r'concurso p[úu]blico|processo seletivo|nomea[çc][ãa]o|exonera|homologa[çc][ãa]o do resultado|gabarito|convoca[çc][ãa]o de candidato|di[áa]rias?\b|f[ée]rias|ata da|reuni[ãa]o', re.I)
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (compatible; RadarJuridicoLP/1.0; pesquisa de editais publicos)'
cl = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x or ''))).strip()

def busca(texto, ini, fim, pagina=1):
    r = S.get('https://www.diariomunicipal.com.br/arom/pesquisar', timeout=60, verify=CA,
              params={'busca_avancada[texto]': texto, 'busca_avancada[dataInicio]': ini, 'busca_avancada[dataFim]': fim, 'busca_avancada[pagina]': pagina})
    h = r.text; out = []
    for c in re.findall(r'<li class="materia-card">(.*?)</li>', h, re.S):
        t = re.search(r'materia-card__titulo">\s*<a href="([^"]+)"[^>]*>(.*?)</a>', c, re.S)
        if not t: continue
        g = lambda rx: (lambda m: cl(m.group(1)) if m else '')(re.search(rx, c, re.S))
        out.append({'url': 'https://www.diariomunicipal.com.br' + t.group(1), 'titulo': cl(t.group(2)), 'entidade': g(r'materia-card__entidade">(.*?)</span>'),
                    'orgao': g(r'materia-card__orgao">(.*?)</span>'), 'trecho': g(r'materia-card__trecho">(.*?)</p>'), 'data': g(r'<dt>Circulação</dt>\s*<dd>(.*?)</dd>')})
    tot = re.search(r'de <strong>([\d.]+)</strong> mat', h)
    return out, int(tot.group(1).replace('.', '')) if tot else len(out)

def main():
    dias = next((int(a) for a in sys.argv[1:] if a.isdigit()), 8); allf = '--all' in sys.argv
    fim = datetime.date.today(); ini = fim - datetime.timedelta(days=dias)
    seen = set(json.load(open(SEEN))) if os.path.exists(SEEN) and not allf else set()
    mats = {}
    for t in TERMOS:
        p = 1
        while p <= 5:
            try: out, tot = busca(t, ini.isoformat(), fim.isoformat(), p)
            except Exception as e: print('erro', t, p, str(e)[:80], file=sys.stderr); break
            for o in out: mats.setdefault(o['url'], o)
            if len(out) < 10 or p * 10 >= tot: break
            p += 1; time.sleep(2)
        time.sleep(2)
    STRICT = re.compile(r'servi[çc]os (t[ée]cnicos )?(especializados )?(de )?(advocac|advocat|jur[íi]dic)|assessoria jur[íi]dica|consultoria jur[íi]dica|sociedade de advogados|escrit[óo]rio de advocacia|advogados? dativos?|credenciamento de advogad', re.I)
    def ok(o):
        t, tr = o['titulo'], o['trecho']
        if NEG.search(t) or o['url'] in seen: return False
        if ADV.search(t) and POS.search(t + ' ' + tr): return True          # advocacia no proprio titulo
        return bool(STRICT.search(tr) and POS.search(t))                     # objeto juridico no trecho + ato de contratacao no titulo
    hits = [o for o in mats.values() if ok(o)]
    hits.sort(key=lambda o: o['data'][6:] + o['data'][3:5] + o['data'][:2], reverse=True)
    json.dump(hits, open(OUT, 'w'), ensure_ascii=False, indent=1)
    if not allf: json.dump(sorted(seen | {o['url'] for o in hits}), open(SEEN, 'w'))
    print(f'{len(mats)} matérias lidas ({ini} a {fim}) | {len(hits)} com indício de contratação de advogado/assessoria jurídica')
    for o in hits:
        print(f"- {o['data']} — {o['entidade']} / {o['orgao']} — [{o['titulo'][:110]}]({o['url']}) — {o['trecho'][:160]}")

if __name__ == '__main__':
    main()
