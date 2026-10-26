# -*- coding: utf-8 -*-
"""Lote 10, parte 2: monta ccidx/wg11_novos.json a partir das arestas do grafo (wg11_arestas.sh).
H = dominios .br que linkam para pelo menos um hub juridico (OAB, Jusbrasil, Conjur, Migalhas, CNJ,
Escavador, JusDecisum). O sinal e a aresta, nao o nome: pega escritorio cujo dominio e so o nome dos
socios, que o filtro por palavra juridica no nome (Lotes 7, 8 e 10 parte 1) nao via.
Fora: orgao publico, universidade, os proprios hubs, portais de vagas, grande imprensa, hospedagem
gratuita, entidades de classe, e tudo que ja esta em estado/hosts_ja_vistos.json."""
import json, re, os, collections
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'ccidx')
ED = os.environ.get('ED', 'cc-main-2026-aug-sep-oct')
HUB = {'5194562': 'conjur', '5320105': 'escavador', '5545184': 'jusbrasil', '5545233': 'jusdecisum',
       '5665317': 'migalhas', '6180304': 'cnj', '6224202': 'oab'}
INST = re.compile(r'\.(gov|edu|mil|jus|leg|mp|def|g12|org)\.br$|jusbrasil|oab[a-z]{0,4}\.org|conjur|migalhas|escavador|jusdecisum|'
                  r'uf[a-z]{1,4}\.br|unb\.br|usp\.br|unicamp|unesp|fgv\.br|puc[a-z]*\.br|sebrae|senac|senai|fiesp|'
                  r'catho|vagas\.com|linkedin|infojobs|gupy|solides|indeed|jooble|bne\.com|empregos|'
                  r'globo|uol|terra\.com|band\.com|folha|estadao|ig\.com\.br|record|sbt|metropoles|'
                  r'wordpress|blogspot|wixsite|webnode|hpg\.|blig\.|tripod|ucoz|'
                  r'projuris|jus\.com\.br|juristas\.com|aasp|iasp|anoreg|cnb', re.I)
ids = {}
for l in open(os.path.join(D, f'wg10_{ED}_br.tsv')):
    p = l.rstrip('\n').split('\t')
    if len(p) >= 2: ids[int(p[0])] = p[1]
por = collections.defaultdict(set)
for l in open(os.path.join(D, 'edges_legal.tsv')):
    p = l.split()
    if len(p) < 2: continue
    i = int(p[0])
    if i in ids: por[i].add(HUB[p[1]])
hub = {'.'.join(reversed(ids[i].split('.'))): sorted(v) for i, v in por.items()}
json.dump(hub, open(os.path.join(D, 'wg11_hub_dominios.json'), 'w'))
vis = {h.replace('www.', '') for h in json.load(open(os.path.join(H, 'estado', 'hosts_ja_vistos.json')))}
novos = [(d, len(v)) for d, v in hub.items() if d not in vis and ('www.' + d) not in vis and not INST.search(d)]
novos.sort(key=lambda x: -x[1])
json.dump({f'HUB dominios .br que linkam para OAB/Jusbrasil/Conjur/Migalhas/CNJ (grafo {ED})': novos},
          open(os.path.join(D, 'wg11_novos.json'), 'w'))
print('dominios .br que linkam para hub juridico', len(hub), '| novos e nao institucionais', len(novos))
