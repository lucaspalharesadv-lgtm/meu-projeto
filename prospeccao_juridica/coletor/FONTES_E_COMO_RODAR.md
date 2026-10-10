# Coletor: fontes já usadas e como rodar

## Fontes ESGOTADAS (não varrer de novo)
- Índice do Common Crawl (`cc_scan.py`): `.adv.br` nas edições 2026-17/21/25/30/34; `.com.br` com nome jurídico nas 30/34/39; `.com` com nome jurídico na 39.
- **Lote 7: grafo de links do Common Crawl (domínios)**, 19 edições de 2023 a 2026 (cc-main-2023-may-sep-nov até cc-main-2026-jul-aug-sep; a cc-main-2023-oct-nov-dec não foi encontrada com esse nome). Foram visitados 74.493 domínios novos: todos os `.adv.br`; `.com.br` com nome jurídico (padrão antigo e "adv" colado, juris, lex, aposentadoria, inss); outros `.br` (net, blog, app...); e `.com` com palavra jurídica em português. Resultado de cada domínio: `estado/cc7_done_lote7.json`.
- Bloqueadas ou inúteis: LinkedIn, BNE, Catho, Jooble, InfoJobs, Vagas.com, Juris Vagas e o portal do DJEN (bloqueia acesso de fora do Brasil).

## Ideias que ainda não foram tentadas
- Grafo de **hosts** (não só domínios): subdomínios do tipo `fulano.advocacia.blog.br` ou `escritorio.cidade.br`.
- `.com` com palavras jurídicas em português nas outras 17 edições do grafo (no Lote 7 só entraram 2 edições para `.com`): devem render algumas centenas.
- Domínios que deram "sem acesso" (55 mil) podem voltar a responder em alguns meses. Rendimento baixo.

## Como rodar uma rodada nova (exemplo do Lote 7)
1. Baixar a parte `.br` dos vértices de domínio do grafo: o arquivo é ordenado, então basta ler até sair do bloco `br.` (cerca de 6 s por edição).
2. Filtrar os nomes e tirar o que já está em `estado/hosts_ja_vistos.json`: gera `ccidx/wg_novos.json`.
3. `TAG=X SHARD=k/n THREADS=80 python3 cc7_process.py A,B,...`: visita os sites respeitando o robots.txt.
4. `python3 cc7_merge.py`: junta os resultados e atualiza `hosts_ja_vistos.json`.
5. `CANDS=cc7_cands_all.json DRY=1 OUTROWS=... python3 final_add7.py`: aplica os filtros, sem gravar nada.
6. Revisão das linhas duvidosas (nome sem palavra de escritório, ou e-mail em domínio diferente do site).
7. `python3 add7.py linhas.json retirados.json`: valida o MX por DNS sobre HTTPS e grava na base. Em seguida, `python3 build_xlsx_500.py`. Antes de rodar, ajuste o número do lote nos dois scripts e em `rotina/proximos.py`.

O DNS local deste ambiente não responde a consultas de MX. Por isso `pros2.mx()` usa DNS sobre HTTPS (dns.google, com cloudflare de reserva), sem enviar nada ao domínio. Para usar o DNS local, defina `MX_DOH=0`.
