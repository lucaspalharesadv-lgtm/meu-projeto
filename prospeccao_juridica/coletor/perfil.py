# -*- coding: utf-8 -*-
"""Perfil de personalizacao extraido LITERALMENTE do site oficial (paginas ja visitadas / cache).
Nada e inventado: areas = termos que aparecem no site; frase = meta description ou texto do proprio site."""
import re, sys, os, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web
from fixenc import fix
import json as _json
_MUN = {}
try:
    for _m in _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ibge_mun.json'))):
        _uf = ((_m.get('microrregiao') or {}).get('mesorregiao') or {}).get('UF', {}).get('sigla') or ((_m.get('regiao-imediata') or {}).get('regiao-intermediaria') or {}).get('UF', {}).get('sigla')
        _MUN.setdefault(_m['nome'].lower(), set()).add(_uf)
except Exception:
    pass
from bs4 import BeautifulSoup

AREAS = [
 ('Previdenciario', r'previdenci|inss|aposentadori|bpc|loas|aux[ií]lio[- ]doen|benef[ií]cio por incapacidade'),
 ('Trabalhista', r'trabalhist|direito do trabalho|reclama[cç][aã]o trabalhista'),
 ('Bancario', r'banc[aá]ri|revisional|superendivid|juros abusivos|consignado'),
 ('Consumidor', r'consumidor|consumerista|\bcdc\b'),
 ('Saude / planos de saude', r'plano de sa[uú]de|planos de sa[uú]de|direito [àa] sa[uú]de|direito m[eé]dico|sa[uú]de suplementar|erro m[eé]dico|medicamento'),
 ('Civel', r'\bc[ií]vel\b|direito civil|contratos|responsabilidade civil'),
 ('Familia e sucessoes', r'fam[ií]lia|div[oó]rcio|invent[aá]rio|sucess[oõ]es|pens[aã]o aliment'),
 ('Imobiliario', r'imobili[aá]ri|usucapi[aã]o|loteamento|regulariza[cç][aã]o fundi'),
 ('Tributario', r'tribut[aá]ri|execu[cç][aã]o fiscal|recupera[cç][aã]o de tributos|fiscal'),
 ('Empresarial / societario', r'empresarial|societ[aá]ri|contratos empresariais|compliance'),
 ('Recuperacao judicial / credito', r'recupera[cç][aã]o judicial|fal[eê]ncia|recupera[cç][aã]o de cr[eé]dito|cobran[cç]a'),
 ('Agronegocio', r'agroneg[oó]cio|direito agr[aá]rio|rural'),
 ('Servidor publico / administrativo', r'servidor(es)? p[uú]blico|direito administrativo|licita[cç]|concurso'),
 ('Criminal', r'criminal|penal\b|direito penal'),
 ('Ambiental', r'ambiental'),
 ('Digital / LGPD', r'\blgpd\b|direito digital|prote[cç][aã]o de dados'),
 ('Transito / multas', r'tr[aâ]nsito|multas|cnh'),
 ('Militar', r'militar(es)?\b'),
]
CAREER = re.compile(r'trabalhe conosco|trabalhe-conosco|carreiras?\b|vagas\b|banco de talentos|envie (seu )?curr[ií]culo|fa[cç]a parte (do|da) (nosso|nossa) (time|equipe)', re.I)
PARTNER = re.compile(r'correspondentes?\b|correspond[eê]ncia jur[ií]dica|advogad[oa]s? parceir[oa]s?|seja (um |uma )?(advogad[oa] )?parceir[oa]|rede de (advogados|parceiros|correspondentes)|credenciamento de advogad', re.I)
VOLUME = re.compile(r'contencioso de massa|massificad|carteira de processos|mais de [\d\.]+ (mil )?processos', re.I)
NACIONAL = re.compile(r'atua[cç][aã]o em todo (o )?(territ[oó]rio nacional|brasil|pa[ií]s)|em todo o (territ[oó]rio nacional|brasil)|todos os estados', re.I)
YEAR = re.compile(r'(?:desde|fundad[oa] em|criad[oa] em|funda[cç][aã]o em)\s+(19[5-9]\d|20[0-2]\d)\b', re.I)
UFN = {'Acre':'AC','Alagoas':'AL','Amapá':'AP','Amazonas':'AM','Bahia':'BA','Ceará':'CE','Distrito Federal':'DF','Espírito Santo':'ES','Goiás':'GO','Maranhão':'MA','Mato Grosso do Sul':'MS','Mato Grosso':'MT','Minas Gerais':'MG','Pará':'PA','Paraíba':'PB','Paraná':'PR','Pernambuco':'PE','Piauí':'PI','Rio de Janeiro':'RJ','Rio Grande do Norte':'RN','Rio Grande do Sul':'RS','Rondônia':'RO','Roraima':'RR','Santa Catarina':'SC','São Paulo':'SP','Sergipe':'SE','Tocantins':'TO'}
CITYUF = re.compile(r'\b([A-ZÀ-Ú][a-zà-ú]+(?:\s(?:d[aeo]s?|[A-ZÀ-Ú][a-zà-ú]+)){0,3})\s?[-/–,]\s?(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)\b')
UFNAMES = '|'.join(sorted(UFN, key=len, reverse=True))
CITYUFN = re.compile(r'\b([A-ZÀ-Ú][a-zà-ú]+(?:\s(?:d[aeo]s?|[A-ZÀ-Ú][a-zà-ú]+)){0,3})\s?[-/–,]\s?(' + UFNAMES + r')\b')
BADCITY = re.compile(r'^(Rua|Av|Avenida|Sala|Centro|Bairro|Edif|Cep|Conj|Andar|Loja|Quadra|Lote|Setor|Jardim|Vila|Torre|Bloco|Fone|Tel|Copyright|Todos)', re.I)

def _meta(htm):
    s = BeautifulSoup(htm, 'lxml')
    for k in ({'name': 'description'}, {'property': 'og:description'}):
        m = s.find('meta', attrs=k)
        if m and m.get('content') and len(m['content'].strip()) > 40:
            return re.sub(r'\s+', ' ', m['content']).strip()
    for tag in s.find_all(['h1', 'h2', 'p']):
        t = re.sub(r'\s+', ' ', tag.get_text(' ')).strip()
        if 60 < len(t) < 400 and not re.search(r'cookie|copyright|todos os direitos', t, re.I):
            return t
    return ''

def perfil(site, extra_pages=()):
    d = web.fetch(site)
    if not d:
        return None
    pages = [d] + [x for x in (web.fetch(u) for u in extra_pages) if x]
    # paginas internas ja visitadas (cache) de sobre/areas/contato
    s = BeautifulSoup(d['html'], 'lxml'); base = urllib.parse.urlsplit(d['final']).netloc.replace('www.', '')
    more = []
    for a in s.find_all('a', href=True):
        h = urllib.parse.urljoin(d['final'], a['href'].split('#')[0])
        if urllib.parse.urlsplit(h).netloc.replace('www.', '') == base and re.search(r'sobre|quem-somos|escritorio|areas|atuacao|servicos|contato|trabalhe|carreira', h, re.I):
            more.append(h)
    for u in list(dict.fromkeys(more))[:4]:
        x = web.fetch(u)
        if x: pages.append(x)
    txt = fix('\n'.join(web.text_of(p['html']) for p in pages))
    low = txt.lower()
    areas = [n for n, rx in AREAS if len(re.findall(rx, low)) >= 1]
    # ordena por frequencia
    areas.sort(key=lambda n: -len(re.findall(dict(AREAS)[n], low)))
    cities = []
    for m in CITYUF.finditer(txt):
        c = m.group(1).strip()
        if BADCITY.search(c) or len(c) < 4: continue
        if _MUN and m.group(2) not in _MUN.get(c.lower(), ()): continue
        cu = f'{c}/{m.group(2)}'
        if cu not in cities: cities.append(cu)
    for m in CITYUFN.finditer(txt):
        c = m.group(1).strip(); uf = UFN[m.group(2)]
        if BADCITY.search(c) or len(c) < 4: continue
        if _MUN and uf not in _MUN.get(c.lower(), ()): continue
        cu = f'{c}/{uf}'
        if cu not in cities: cities.append(cu)
    y = YEAR.search(txt)
    return {
        'frase': fix(_meta(d['html']))[:260],
        'areas': areas[:6],
        'cidades': cities[:5],
        'carreiras': bool(CAREER.search(txt)),
        'parceria': bool(PARTNER.search(txt)),
        'volume': bool(VOLUME.search(txt)),
        'nacional': bool(NACIONAL.search(txt)),
        'desde': y.group(1) if y else '',
        'n_paginas': len(pages),
    }

def gancho(p, vaga=''):
    """Texto curto, so com fatos do site/vaga, para o redator usar."""
    if not p: return ''
    partes = []
    if p['areas']: partes.append('Areas destacadas no site: ' + ', '.join(p['areas'][:4]))
    if p['cidades']: partes.append('Enderecos/cidades citados: ' + ', '.join(p['cidades'][:3]))
    if p['desde']: partes.append(f"Site menciona atuacao desde {p['desde']}")
    if p['volume']: partes.append('Site fala em contencioso de massa/volume de processos')
    if p.get('nacional'): partes.append('Site diz atuar em todo o Brasil')
    if p['carreiras']: partes.append("Site tem area 'trabalhe conosco'/carreiras")
    if p['parceria']: partes.append('Site menciona correspondentes/advogados parceiros')
    if vaga: partes.append('Vaga anunciada: ' + vaga)
    return '. '.join(partes) + '.' if partes else ''

def abordagem(p, modelo='', oport=''):
    t = (modelo + ' ' + oport).lower()
    if re.search(r'recrut|vaga|associad|pj|remot', t): return 'A - candidato (vaga/associado)'
    if re.search(r'correspond|plataforma', t) or (p and p['volume']): return 'B - fornecedor (correspondencia)'
    if p and p['carreiras']: return 'A - candidato (banco de talentos)'
    return 'C - parceria (divisao de honorarios)'

if __name__ == '__main__':
    import json
    for u in sys.argv[1:]:
        p = perfil(u); print(json.dumps(p, ensure_ascii=False)); print(gancho(p)); print(abordagem(p))
