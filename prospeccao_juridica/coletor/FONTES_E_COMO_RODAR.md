# Coletor: fontes já usadas e como rodar

## Fontes ESGOTADAS (não varrer de novo)
- Índice do Common Crawl (`cc_scan.py`): `.adv.br` nas edições 2026-17/21/25/30/34; `.com.br` com nome jurídico nas 30/34/39; `.com` com nome jurídico na 39.
- **Lote 7: grafo de links do Common Crawl (domínios)**, 19 edições de 2023 a 2026 (cc-main-2023-may-sep-nov até cc-main-2026-jul-aug-sep; a cc-main-2023-oct-nov-dec não foi encontrada com esse nome). Foram visitados 74.493 domínios novos: todos os `.adv.br`; `.com.br` com nome jurídico (padrão antigo e "adv" colado, juris, lex, aposentadoria, inss); outros `.br` (net, blog, app...); e `.com` com palavra jurídica em português. Resultado de cada domínio: `estado/cc7_done_lote7.json`.
- **Lote 8 (10/10/2026):** `.com` com palavra jurídica em português nas outras 17 edições do grafo (10.213 domínios) e **grafo de hosts** `.br` (subdomínio com palavra jurídica, 1.770 hosts: Jusfy, site.adv.br, jur.adv.br, jud.adv.br, blogspot.com.br, webnode etc.). Resultado: `estado/cc7_done_lote8.json`. Lista montada por `wg8_universo.py`. Rendeu 362 e-mails: os sites do Jusfy não publicam e-mail no HTML, e o site.adv.br estava fora do ar.
- Bloqueadas ou inúteis: LinkedIn, BNE, Catho, Jooble, InfoJobs, Vagas.com, Juris Vagas e o portal do DJEN (bloqueia acesso de fora do Brasil).

## Fonte do Lote 10 (parte 2): as ARESTAS do grafo, não o nome do domínio

O filtro por nome só acha quem põe "adv", "advocacia" ou "juridico" no domínio, e ainda traz lixo
("flex", "complex", "alex", "oab" dentro de outra palavra: colégio, engenharia, motoboy). A parte 2
do Lote 10 troca o sinal: vale quem **linka** para um hub jurídico brasileiro.

1. `bash wg11_arestas.sh` — lê em stream o arquivo de arestas da edição (7,6 GB .gz, nada gravado em
   disco) e guarda só as arestas que apontam para conjur, escavador, jusbrasil, jusdecisum, migalhas,
   cnj ou oab (ids tirados do arquivo de vértices). As arestas vêm ordenadas pelo domínio de origem e
   a faixa `.br` termina no id 6.244.778: quando a origem passa disso, o Brasil inteiro já foi lido e
   dá para interromper o download (foram ~12 minutos, não as horas que o arquivo inteiro levaria).
2. `python3 wg11_universo.py` — mapeia id para domínio, tira órgão público, universidade, imprensa,
   portal de vagas, hospedagem gratuita, os próprios hubs e tudo que já está em `hosts_ja_vistos.json`.
   Resultado: 13.094 domínios `.br` ligados a hub jurídico, 9.390 nunca visitados.
3. `WG=wg11_novos.json TAG=gK SHARD=k/6 python3 cc7_process.py HUB 0` — visita.
4. `CANDS=... DRY=1 ORIGEM="site linkado ao portal da OAB ou a portais juridicos no grafo de links" python3 final_add10.py`

Rendimento: **32% dos sites com e-mail, contra 13% do filtro por nome**, e os escritórios são de outro
tipo — os que têm só o nome dos sócios no domínio (Arruda Alvim Aragão & Lins, Souto Correa, Finocchio
& Ustra, Araújo Policastro), que o filtro por nome nunca via.

## Ideias que ainda não foram tentadas
- Hosts `.com` em plataformas (`*.wixsite.com`, `*.blogspot.com`, `*.wordpress.com`) com nome jurídico em português: ficam nas partes `com.*` dos vértices de host (arquivos grandes). Rendimento provável baixo, porque blogs raramente são escritórios.
- Domínios que deram "sem acesso" (63 mil nos Lotes 7 e 8) podem voltar a responder em alguns meses. Rendimento baixo.
- Mesma varredura por arestas com outros alvos: quem linka para tribunais (tjsp, trf1, trt), para o PJe ou para a Receita.
- Daqui para a frente, o Common Crawl só traz novidade a cada nova edição do grafo (a cada ~3 meses): basta repetir o passo a passo só com a edição nova.

## Como rodar uma rodada nova (exemplo do Lote 7)
1. Baixar a parte `.br` dos vértices de domínio do grafo: o arquivo é ordenado, então basta ler até sair do bloco `br.` (cerca de 6 s por edição).
2. Filtrar os nomes e tirar o que já está em `estado/hosts_ja_vistos.json`: gera `ccidx/wg_novos.json`.
3. `TAG=X SHARD=k/n THREADS=80 python3 cc7_process.py A,B,...`: visita os sites respeitando o robots.txt.
4. `python3 cc7_merge.py`: junta os resultados e atualiza `hosts_ja_vistos.json`.
5. `CANDS=cc7_cands_all.json DRY=1 OUTROWS=... python3 final_add7.py`: aplica os filtros, sem gravar nada.
6. Revisão das linhas duvidosas (nome sem palavra de escritório, ou e-mail em domínio diferente do site).
7. `LOTE=N python3 add7.py linhas.json retirados.json`: valida o MX por DNS sobre HTTPS e grava na base. Em seguida, `python3 build_xlsx_500.py`. Antes, troque `LOTE = N` no topo do `build_xlsx_500.py` (e o texto do LEIA-ME) e a ordem dos lotes em `rotina/proximos.py`.

Sites-modelo (tema de demonstração com "Rua Nome da Rua", "(11) 98765-4321", "Lorem ipsum" e e-mail de outro domínio) aparecem nos `.com` e nos subdomínios: a revisão por agentes pegou esses casos no Lote 8.

MX que aponta para `0.0.0.0` ou `localhost` (caso do domínio `adv.com`) agora conta como "sem MX": o domínio não recebe e-mail.

O DNS local deste ambiente não responde a consultas de MX. Por isso `pros2.mx()` usa DNS sobre HTTPS (dns.google, com cloudflare de reserva), sem enviar nada ao domínio. Para usar o DNS local, defina `MX_DOH=0`.
