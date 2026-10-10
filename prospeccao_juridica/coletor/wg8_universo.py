# -*- coding: utf-8 -*-
"""Lote 8: monta ccidx/wg8_novos.json com duas fontes novas do grafo de links do Common Crawl.
F = dominios .com com palavra juridica em portugues (as 17 edicoes que o Lote 7 nao usou para .com);
G = hosts .br cujo SUBDOMINIO tem palavra juridica (sites de advogados em plataformas como Jusfy e jur.adv.br),
    sem orgao publico, universidade, OAB, Jusbrasil, portais de vagas etc.
Tudo que ja esta em estado/hosts_ja_vistos.json fica de fora."""
import json, re, glob, os, collections
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'ccidx')
vis = {h.replace('www.', '') for h in json.load(open(os.path.join(H, 'estado', 'hosts_ja_vistos.json')))}
# --- F: .com ---
PT = re.compile(r'advogad|advocacia|juridic|previdenci|trabalhist|tributari|associados|escritoriodeadv|direitod[oa]|sociedadedeadv', re.I)
ES = re.compile(r'asesor|estudio|abogad|despacho|avvocat|juridicos?legal|consultorio|bufete|notari|inmobil|corporacion|studiolegal|legale|juridicos[a-z]', re.I)
F = collections.Counter()
for f in glob.glob(os.path.join(D, 'wgcom_*.tsv')):
    for l in open(f):
        p = l.rstrip('\n').split('\t')
        if len(p) < 2: continue
        d = '.'.join(reversed(p[1].split('.')))
        if PT.search(d[:-4]) and not ES.search(d): F[d] += 1
Fn = sorted([(d, n) for d, n in F.items() if d not in vis], key=lambda x: -x[1])
# --- G: hosts .br ---
SLD = {'com', 'adv', 'net', 'org', 'blog', 'eco', 'srv', 'tec', 'ind', 'emp', 'app', 'log', 'art', 'pro', 'eti', 'gov', 'edu', 'jus',
       'leg', 'mp', 'def', 'med', 'eng', 'arq', 'tur', 'inf', 'nom', 'psi', 'jor', 'cnt', 'adm', 'odo', 'vet', 'fot', 'ato', 'bio', 'far',
       'fnd', 'esp', 'etc', 'rec', 'tmp', 'tv', 'wiki', 'agr', 'am', 'coop', 'g12', 'ggf', 'imb', 'lel', 'mat', 'mil', 'mus', 'not', 'ntr',
       'qsl', 'radio', 'slg', 'taxi', 'teo', 'trd', 'vlog', 'zlg', 'b', 'seg', 'bet', 'dev', 'sp', 'rj', 'mg', 'rs', 'pr', 'sc', 'ba', 'df',
       'go', 'pe', 'ce', 'es', 'pa', 'am', 'mt', 'ms', 'ma', 'pb', 'rn', 'al', 'pi', 'se', 'ro', 'to', 'ac', 'ap', 'rr', 'jur', 'jud'}
LEG = re.compile(r'advoc|advog|juridic|previdenci|trabalhist|tributari|associados|adv($|s$|-)|^adv[^aeiou]|-adv|juris|lawyers?|aposentad', re.I)
# institucional, publico, ensino, vagas, diretorios e portais (nao sao escritorios)
INST = re.compile(r'\.(gov|edu|org|mil|jus|leg|mp|def|mus|g12)\.br$|^[^.]*\.?(uf[a-z]{1,4}|unb|usp|unicamp|unesp|fgv|puc[a-z]*|uerj|ufrgs|unifesp|uem|uel|unioeste|ifsp|if[a-z]{1,3})\.br$'
                  r'|jusbrasil|infojobs|softonic|eventize|emnuvens|solides|efpc\.com|aspec\.com|oab[a-z]{0,3}\.org|catho|vagas\.com|linkedin|bne\.com|gupy|kenoby|pandape|'
                  r'jooble|indeed|musicas\.mus|hpg\.(ig\.)?com\.br|blig\.ig|tripod|geocities|sites\.uol|ucoz|webcindario|ning\.com|'
                  r'decisoes\.com\.br|comexdata|lyrics\.com|itau\.com|permutalivre|k6\.com|bradial|ibooked|infoisinfo|guiataubate|formulamaster|'
                  r'jus\.com\.br|projuris|jusdecisum|escavador|juristas\.com', re.I)
G = collections.Counter(); por_dom = collections.defaultdict(set); dom_of = {}
for f in glob.glob(os.path.join(D, 'hv_*_br.txt')):
    for l in open(f):
        r = l.strip(); labs = r.split('.')
        if len(labs) < 3: continue
        k = 3 if labs[1] in SLD else 2
        dom = '.'.join(reversed(labs[:k])); sub = [s for s in labs[k:] if s != 'www']
        if not sub: continue
        host = '.'.join(reversed(labs)).replace('www.', '')
        if INST.search(host): continue
        if not LEG.search('.'.join(sub)): continue
        G[host] += 1; por_dom[dom].add(host); dom_of[host] = dom
# subdominio de um escritorio ja visitado (ex.: blog.silvaadvogados.com.br) = mesmo escritorio: fica de fora;
# plataforma (5+ subdominios juridicos distintos, ex.: jusfy.com.br) = cada subdominio e um advogado diferente
plataforma = {d for d, hs in por_dom.items() if len(hs) >= 5}
Gn = []
for h, n in G.items():
    if h in vis: continue
    dom = dom_of[h]
    if dom in vis and dom not in plataforma: continue
    Gn.append((h, n))
Gn.sort(key=lambda x: -x[1])
json.dump({'F com (17 edicoes novas do grafo)': Fn, 'G hosts .br com subdominio juridico': Gn}, open(os.path.join(D, 'wg8_novos.json'), 'w'))
print('F .com novos', len(Fn), '| G hosts .br novos', len(Gn))
print('plataformas', sorted(((d, len(por_dom[d])) for d in plataforma), key=lambda x: -x[1])[:25])
