# -*- coding: utf-8 -*-
"""Varre o Jobijoba (agregador que publica o texto completo do anuncio) atras de vagas juridicas
com e-mail de candidatura. Guarda em vagas_jobijoba.json e marca as ja vistas em vagas_vistas.json."""
import sys, os, re, json, urllib.parse
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(B, 'lib'))
import web
from bs4 import BeautifulSoup
SEEN = os.path.join(B, 'vagas_vistas.json'); OUT = os.path.join(B, 'vagas_jobijoba.json')
vistas = json.load(open(SEEN)) if os.path.exists(SEEN) else {}
BAD = re.compile(r'jobijoba|hellowork|sentry|example|wixpress|gov\.br|jus\.br', re.I)
BLOQ = re.compile(r'\bmbt\b|mbtadvoca|ernesto ?borges|ernestoborges|pessoa ?(&|e) ?pessoa|pessoaepessoa', re.I)
UFS = ['parana', 'sao-paulo', 'minas-gerais', 'rondonia', 'mato-grosso', 'goias', 'rio-de-janeiro', 'santa-catarina', 'rio-grande-do-sul', 'bahia', 'pernambuco', 'amazonas', 'para', 'distrito-federal', 'mato-grosso-do-sul', 'espirito-santo', 'ceara', 'acre', 'tocantins', 'maranhao', 'paraiba', 'rio-grande-do-norte', 'sergipe', 'alagoas', 'piaui']
ROLES = ['advogado', 'analista-juridico', 'assistente-juridico', 'advogado-junior', 'advogado-pleno', 'advogado-trabalhista', 'advogado-previdenciario', 'advogado-civel', 'controladoria-juridica', 'auxiliar-juridico', 'consultor-juridico', 'correspondente-juridico']
pages = [f'https://www.jobijoba.com.br/vagas-emprego/{r}' for r in ROLES] + [f'https://www.jobijoba.com.br/vagas-emprego/advogado/estado-{u}' for u in UFS] + [f'https://www.jobijoba.com.br/vagas-emprego/analista-juridico/estado-{u}' for u in UFS[:8]]
det = []
for u in pages:
    d = web.fetch(u, use_cache=False)
    if not d: continue
    s = BeautifulSoup(d['html'], 'lxml')
    for a in s.find_all('a', href=True):
        h = urllib.parse.urljoin(d['final'], a['href']).split('?')[0]
        if '/detail/' in h and h not in det and h not in vistas: det.append(h)
print('anuncios novos a abrir', len(det), flush=True)
novas = {}
for i, h in enumerate(det, 1):
    d = web.fetch(h)
    vistas[h] = 1
    if not d: continue
    em = [e for e in web.emails_in(d['html']) if not BAD.search(e)]
    tx = re.sub(r'\s+', ' ', web.text_of(d['html']))
    if em and not BLOQ.search(tx):
        novas[h] = dict(title=web.title_of(d['html']), emails=em, texto=tx[:3500])
    if i % 50 == 0:
        json.dump(vistas, open(SEEN, 'w')); print(i, 'abertos |', len(novas), 'com e-mail', flush=True)
json.dump(vistas, open(SEEN, 'w')); json.dump(novas, open(OUT, 'w'), ensure_ascii=False)
print('FIM: vagas novas com e-mail:', len(novas))
for h, v in novas.items(): print('-', v['title'][:90], '|', v['emails'][:2])
