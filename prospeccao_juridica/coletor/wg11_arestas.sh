#!/bin/bash
# Lote 10, parte 2: fonte nova = ARESTAS do grafo de links do Common Crawl, nao o nome do dominio.
# Varre em stream o arquivo de arestas da edicao (7,6 GB .gz, nada e gravado em disco) e guarda
# so as arestas que apontam para um hub juridico brasileiro. Os ids vem do arquivo de vertices
# (wg10_cc-main-2026-aug-sep-oct_br.tsv): conjur, escavador, jusbrasil, jusdecisum, migalhas, cnj, oab.
# As arestas vem ordenadas por dominio de origem, e a faixa .br termina no id 6.244.778: quando a
# origem passa disso, todo o Brasil ja foi varrido e o download pode ser interrompido.
set -euo pipefail
ED=${ED:-cc-main-2026-aug-sep-oct}
IDS=${IDS:-"5194562 5320105 5545184 5545233 5665317 6180304 6224202"}
cd "$(dirname "$0")"
curl -sS --cacert /root/.ccr/ca-bundle.crt --max-time 5400 \
  "https://data.commoncrawl.org/projects/hyperlinkgraph/$ED/domain/$ED-domain-edges.txt.gz" \
| gzip -dc \
| awk -F'\t' -v ids="$IDS" 'BEGIN{n=split(ids,a," "); for(i=1;i<=n;i++) t[a[i]]=1} ($2 in t){print $1"\t"$2}' \
> ccidx/edges_legal.tsv
wc -l ccidx/edges_legal.tsv
