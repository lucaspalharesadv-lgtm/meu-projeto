# M3BS — DADOS CORPORATIVOS E REGISTRAIS (key = dados-corporativos)
Coletado em 2026-10-13. Arquivos brutos (JSON/HTML/renders) em findings/dc_raw/. Script Playwright usado para OAB em dc_scripts/oab.js.
OBS: o orçamento de WebSearch desta rodada estava esgotado (limite compartilhado); tudo abaixo veio de curl/WebFetch/Playwright em URLs diretas e da varredura dos arquivos locais já baixados por outros finders.

## 1. RECEITA FEDERAL — MATRIZ 07.848.463/0001-57  [CONFIRMADO — 3 APIs independentes concordantes + Casa dos Dados + ReceitaWS + CNPJá]
Fontes (lidas 2026-10-13):
- https://brasilapi.com.br/api/cnpj/v1/07848463000157 (dc_raw/brasilapi_com_br_api_cnpj_v1_07848463000157.json)
- https://minhareceita.org/07848463000157 (dc_raw/minhareceita_org_07848463000157.json)
- https://publica.cnpj.ws/cnpj/07848463000157 ("atualizado_em": "2026-09-12") (dc_raw/publica_cnpj_ws_cnpj_07848463000157.json)
- https://receitaws.com.br/v1/cnpj/07848463000157 ("ultima_atualizacao": "2026-10-08")
- https://open.cnpja.com/office/07848463000157 ("updated": "2026-09-12")
- https://casadosdados.com.br/solucao/cnpj/miglioli-bianchi-borrozzino-bellinatti-e-scarabel-advogados-07848463000157 (render Playwright; "Ultima Atualização: 13/09/2026 21:00")

Campos (literais):
- razao_social: "MIGLIOLI, BIANCHI, BORROZZINO, BELLINATTI E SCARABEL ADVOGADOS"
- nome_fantasia: "" (vazio / "-") — não há nome fantasia "M3BS" registrado na RFB.
- cnpj: 07.848.463/0001-57 — identificador_matriz_filial: MATRIZ
- data_inicio_atividade / "Data de Abertura": 2005-09-01 (01/09/2005)  <<< ATENÇÃO: a tarefa diz "em atividade desde 2009"; o CNPJ foi aberto em 01/09/2005. O LinkedIn diz "constituído em 2009". Ver seção 6.
- situacao_cadastral: 2 = "ATIVA"; data_situacao_cadastral: 2005-09-01; motivo: "SEM MOTIVO"; situacao_especial: vazio
- natureza_juridica: 223-2 "Sociedade Simples Pura"
- cnae_fiscal: 6911-7/01 "Serviços advocatícios" (seção M, divisão 69). cnaes_secundarios: [] (nenhum)
- capital_social: 150000 (R$ 150.000,00)
- porte: código 05 "DEMAIS" (ou seja, NÃO é ME nem EPP → enquadramento acima de R$ 4,8 mi/ano de receita bruta)
- qualificacao_do_responsavel: 49 "Sócio-Administrador"
- endereço: tipo AVENIDA, logradouro "PAULISTA", numero "854", complemento "ANDAR 3", bairro "BELA VISTA", cep 01310-913, SAO PAULO/SP (IBGE 3550308)
- ddd_telefone_1: "1131152282" → (11) 3115-2282 ; ddd_telefone_2: vazio ; ddd_fax: 1131152282 (mesmo número)
- email (cadastral RFB, via publica.cnpj.ws, receitaws, cnpja, Casa dos Dados): "contato@miglioli.com.br"  <<< e-mail cadastral ainda no DOMÍNIO ANTIGO miglioli.com.br (BrasilAPI/minhareceita retornam email: null)
- opcao_pelo_simples: false; data_opcao_pelo_simples: 2015-01-01; data_exclusao_do_simples: 2022-10-31. CNPJá: "history": [{"from": "2015-01-01", "until": "2022-10-31", "text": "Excluída por Comunicação Obrigatória do Contribuinte"}]. MEI: não.
- regime_tributario (BrasilAPI): ano 2022 "LUCRO PRESUMIDO" (1 escrituração); 2023 "LUCRO PRESUMIDO"; 2024 "LUCRO PRESUMIDO".
- inscricoes_estaduais: [] ; suframa: [] ; ente_federativo_responsavel: vazio
- pais: Brasil

QSA — QUADRO SOCIETÁRIO (5 sócios pessoa física; idêntico nas 3 APIs; Casa dos Dados confirma):
| Sócio (nome na RFB) | Qualificação | Data de entrada na sociedade | Faixa etária (RFB) | CPF mascarado |
|---|---|---|---|---|
| LUCAS AUGUSTUS ALVES MIGLIOLI | 49 — Sócio-Administrador | 2005-09-01 (01/09/2005) | 41 a 50 anos | ***473358** |
| FERNANDO MACHADO BIANCHI | 49 — Sócio-Administrador | 2010-05-10 (10/05/2010) | 41 a 50 anos | ***749718** |
| LUIS HENRIQUE BORROZZINO | 52 — Sócio com Capital | 2010-05-10 (10/05/2010) | 41 a 50 anos | ***677598** |
| GIULIANO PRETINI BELLINATTI | 52 — Sócio com Capital | 2014-01-31 (31/01/2014) | 41 a 50 anos | ***588748** |
| ROGERIO SCARABEL BARBOSA | 52 — Sócio com Capital | 2022-03-21 (21/03/2022) | 51 a 60 anos | ***649748** |
=> Só Miglioli e Bianchi são SÓCIOS-ADMINISTRADORES (representam a sociedade). Borrozzino, Bellinatti e Scarabel são "sócio com capital".
=> Miglioli é o único sócio desde a abertura (2005). Bianchi e Borrozzino entraram juntos em 10/05/2010. Bellinatti em 31/01/2014. Scarabel em 21/03/2022 (coerente com sua saída da ANS em ago/2021 e com o ConJur de 03/03/2022 que já o chama de "mais novo sócio").
Observação de outro finder (socios-miglioli-bianchi.md): MonitorCNPJ mostrava a mesma estrutura de QSA (datas 01/09/2005, 10/05/2010, 10/05/2010, 31/01/2014, 21/03/2022) com nomes ocultos; agora CONFIRMADO com nomes.

## 2. FILIAIS — RAIZ 07.848.463  [CONFIRMADO]
- Casa dos Dados "Filiais" (https://casadosdados.com.br/solucao/cnpj/filiais/miglioli-bianchi-borrozzino-bellinatti-e-scarabel-advogados-07848463000157, render Playwright 2026-10-13): "Encontrado 2 empresas para a matriz: 07.848.463" → "07.848.463/0001-57 - Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados Ativa" ; "07.848.463/0002-38 - Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados Baixada".
- Teste direto: CNPJs 07.848.463/0003-19, /0004-08, /0005-80, /0006-61, /0007-42, /0008-23 (dígitos calculados) → 404 "não encontrado" na BrasilAPI e na minhareceita. => NÃO EXISTE filial registrada na RFB além da 0002 (Taubaté).
### FILIAL 0002-38 — TAUBATÉ/SP (BAIXADA)
Fontes: https://brasilapi.com.br/api/cnpj/v1/07848463000238 ; https://minhareceita.org/07848463000238 ; https://publica.cnpj.ws/cnpj/07848463000238 (Serasa: https://empresas.serasaexperian.com.br/consulta-gratis/MIGLIOLI-BIANCHI-BORROZZINO-BELLINATTI-E-SCARABEL-ADVOGADOS-07848463000238 abre, mas só mostra texto genérico "Cadastre o seu CNPJ..." sem dados).
- identificador: FILIAL; razão social idêntica; situacao_cadastral 8 = "BAIXADA"; data_situacao_cadastral: 2008-03-25 (25/03/2008); motivo 1 = "EXTINCAO POR ENCERRAMENTO LIQUIDACAO VOLUNTARIA"
- data_inicio_atividade: 2005-09-01 (mesma da matriz — herdada)
- endereço: AVENIDA FRANCISCO BARRETO LEME, 976, bairro JARDIM CALIFORNIA, CEP 12062-001, TAUBATE/SP (IBGE 3554102)
- telefone/fax: ddd 11 + 31043875 → (11) 3104-3875 (DDD 11 cadastrado para filial em Taubaté, cujo DDD é 12 — provável telefone de SP)
- email: null ; CNAE 6911-7/01 ; capital social 150.000 (da raiz)
- Contexto (outro finder, clientes-casos.md): há inventário/sucessão da "família Miglioli, Taubaté" no e-SAJ → Taubaté é cidade de origem/ligação familiar de Lucas Miglioli (PROVÁVEL). A filial de Taubaté existiu entre 2005 e 2008 (fase pré-Bianchi).
### "FILIAL" DE FORTALEZA/CE — NÃO CONSTA NA RECEITA
- ConJur 03/03/2022 12h38, "Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel chega ao Ceará", Redação ConJur, https://www.conjur.com.br/2022-mar-03/miglioli-bianchi-borrozzino-bellinatti-scarabel-chega-ceara/ (curl 2026-10-13; meta article:published_time 2022-03-03T15:38:00+00:00). TEXTO LITERAL:
  > "O escritório Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados (M3BS), com sede em São Paulo, acaba de inaugurar sua primeira filial em Fortaleza."
  > "'O objetivo é nos aproximarmos ainda mais das empresas de saúde privada — clientes e prospects — nas regiões Norte e Nordeste', afirma Fernando Bianchi, sócio do M3BS ao lado de Giuliano Bellinatti, Lucas Miglioli, Luis Henrique Borrozzino e do mais novo sócio, Rogério Scarabel, ex-presidente substituto da Agência Nacional de Saúde Suplementar."
  > "Hoje, o M3BS soma mais de 450 clientes espalhados em todo o país e no exterior, que contam com atendimento preventivo e contencioso de demandas jurídicas nas áreas de Direito Médico, Direito de Saúde Suplementar e Regulatório, Direito Administrativo, Negócios Públicos, Direito Empresarial e Penal Empresarial."
  Legenda da foto: "Banca Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel inaugura filial no CE". Tags: Advocacia, Empresarial, Escritórios, Mercado Jurídico. NÃO informa endereço da filial nem quem a lidera.
- The Latin American Lawyer https://thelatinamericanlawyer.com/m3bs-opens-branch-in-fortaleza/ → HTTP 403 Cloudflare (curl, WebFetch, Playwright headless com "Executando verificação de segurança", wp-json e feed RSS também 403). NÃO LIDO.
- Receita: nenhum estabelecimento no CE (ver acima). Site 2026: página /o-escritorio/ lista apenas "Sede (São Paulo/SP)"; outro finder (site-news-institucional.md) anotou "O M3BS conta com correspondentes em todos os Estados brasileiros". Posts do site mencionam Fortaleza só como local de cliente/eventos (Hapvida NotreDame Intermédica Fortaleza 30/11/2023 e 03/04/2024; ABEA 10/09/2024; SINNAD 28/08/2026). Post 03/04/2024 (https://m3bs.com.br/academia-m3bs-na-hapvida-saude-fortaleza/): "Em parceria com Hapvida NotreDame Intermédica de Fortaleza, o encontro contou com a participação da equipe do Contencioso Regulatório da unidade de Fortaleza" — ambíguo (unidade da Hapvida ou do M3BS).
- HIPÓTESE (INCERTO): a "filial" de Fortaleza anunciada em mar/2022 funciona(va) sem CNPJ de filial próprio — provavelmente como escritório associado/correspondente ou equipe alocada em cliente (Hapvida é de Fortaleza; Scarabel tem formação na UFC/Unifor e presença frequente em Fortaleza). Não há evidência de que ainda exista em 2026.

## 3. DOMÍNIOS / WHOIS (RDAP registro.br)  [CONFIRMADO]
### m3bs.com.br — https://rdap.registro.br/domain/m3bs.com.br (2026-10-13)
- Registro do domínio: 2021-09-21T16:11:36Z ; última alteração 2024-08-29 ; expiração 2027-09-21 ; status active ; DNSSEC não ; ticket de arquivo 23452227.
- Registrante (entity handle 07848463000157): "fn": "Miglioli e Bianchi Advogados" ; publicIds cnpj "07.848.463/0001-57" ; "legalRepresentative": "Lucas Augustus Alves Miglioli" ; entidade registrada no registro.br em 2006-06-26, última alteração 2017-06-12.
- Contato administrativo e técnico: handle LAM725 "lucas augustus alves miglioli", e-mail "lucas@miglioli.com.br", lang pt; handle criado 2005-07-18, alterado 2021-09-21.
- Nameservers: ns1/ns2/ns3/ns4.bdm.microsoftonline.com (DNS gerenciado pelo Microsoft 365).
=> O domínio m3bs.com.br só foi registrado em set/2021 — a marca "M3BS" nasce entre set/2021 (domínio) e mar/2022 (entrada formal de Scarabel, o "S"). O registrante no registro.br AINDA está cadastrado com o nome antigo "Miglioli e Bianchi Advogados".
### miglioli.com.br — https://rdap.registro.br/domain/miglioli.com.br
- Registro 2004-06-29 ; última alteração 2025-06-14 ; expiração 2035-06-29 (renovado por longo prazo em 2025 → o escritório mantém o domínio antigo deliberadamente) ; mesmo registrante "Miglioli e Bianchi Advogados" / CNPJ 07848463000157 ; técnico LAM725 lucas@miglioli.com.br ; NS ns1-3.bdm.microsoftonline.com.
- O domínio antigo é ANTERIOR ao CNPJ (2004 vs 2005): Lucas Miglioli já atuava com a marca "Miglioli" antes de constituir a sociedade.
- DNS: miglioli.com.br e www.miglioli.com.br NÃO têm registro A (site antigo fora do ar; HTTP 502 via proxy), MAS têm MX "miglioli-com-br.mail.protection.outlook.com" e SPF "v=spf1 include:spf.protection.outlook.com -all" → o domínio continua recebendo e-mail no Microsoft 365 (PROVÁVEL que contato@miglioli.com.br e lucas@miglioli.com.br ainda funcionem; não testado).
- Glassdoor (outro finder): perfil "Miglioli e Bianchi Advogados" com site http://www.miglioli.com.br e porte "Micro empresa (até 19 funcionários)" (desatualizado).
### Outros domínios testados
- m3bslicita.com.br → RDAP 404 (não registrado) ; DNS NXDOMAIN. m3bs.adv.br → 404. m3bsadvogados.com.br → 404. licita.m3bs.com.br → sem A.
### Infra de e-mail/site m3bs.com.br (DNS via cloudflare-dns.com, 2026-10-13)
- MX: "0 m3bs-com-br.mail.protection.outlook.com." → Exchange Online / Microsoft 365.
- TXT: "v=spf1 include:spf.protection.outlook.com -all" ; "MS=ms49466817" (verificação Microsoft 365) ; "brevo-code:d31f11f5658b886628cc259a28430daa" (Brevo/ex-Sendinblue — plataforma de e-mail marketing usada para newsletter/clipping) ; "mscid=..." (Microsoft).
- autodiscover.m3bs.com.br → autodiscover.outlook.com.
- A m3bs.com.br = 102.165.25.7 (bloco AFRINIC — hospedagem/CDN; RDAP afrinic). Site: WordPress com tema próprio "theme-m3bs" + Elementor + plugin Shield Security (REST API anônima bloqueada).
=> Para e-mails de candidatura: o escritório usa Microsoft 365/Outlook; e-mails @m3bs.com.br chegam em caixas Exchange (filtros anti-spam padrão da Microsoft).

## 4. PADRÃO DE E-MAIL CORPORATIVO E E-MAILS PÚBLICOS @m3bs.com.br
(varredura de TODOS os arquivos locais: findings/*.md, ALL_SITE_POSTS.txt, inst_*, site/*.html; contagem de ocorrências)
Caixas institucionais:
- contato@m3bs.com.br — site /contato/ (site/contato.html: "contato@m3bs.com.br" + "Avenida Paulista, 854 – 3º andar", "CEP 01310-913", "Alameda Joaquim Eugênio de Lima, 424 (recepção)") [CONFIRMADO]
- m3bsresponde@m3bs.com.br — rodapé padrão dos posts 2023-2026 ("Contate-nos através do e-mail m3bsresponde@m3bs.com.br ou por telefone (11) 3115-2282") [CONFIRMADO]
- rh@m3bs.com.br — posts antigos de vaga no LinkedIn (Marcelo Alves, "Advogado(a) Jr III e Pleno", ~2021-2023; dado de outro finder) [PROVÁVEL]
- etica@m3bs.com.br — Código de Conduta ("canal de denúncia etica@m3bs.com.br") [CONFIRMADO]
- licita@m3bs.com.br — post 2023-08-07 https://m3bs.com.br/licitante-pega-essa-dica/ ("Quer saber mais? licita@m3bs.com.br ou (11) 3115-2282.") [CONFIRMADO]
- m3bsadvogados@m3bs.com.br — Política de privacidade/newsletter ("entrar em contato através do e-mail m3bsadvogados@m3bs.com.br para exercer seus direitos relacionados à proteção de dados pessoais") [CONFIRMADO]
- contato@miglioli.com.br — e-mail cadastral na RFB (domínio antigo) [CONFIRMADO na RFB; funcionamento INCERTO]
Sócios (mailto nos cards de https://m3bs.com.br/profissionais/ — site/profissionais.html) [CONFIRMADO]:
- lucas@m3bs.com.br (Lucas Miglioli) — também "cope_mail" no cadastro da Análise Advocacia 2026 (outro finder)
- fernando@m3bs.com.br (Fernando Bianchi)
- luis@m3bs.com.br (Luis Henrique Borrozzino) — também na Análise Advocacia (OAB/SP 262256)
- giuliano@m3bs.com.br (Giuliano Bellinatti) — também na Política de Privacidade como contato LGPD ("reportada ao M3BS, na pessoa do sócio Giuliano Bellinatti, através do telefone (11) 3115-2282 ou do e-mail (giuliano@m3bs.com.br)")
- scarabel@m3bs.com.br (Rogério Scarabel) — ÚNICA exceção: sobrenome em vez de primeiro nome
- lucas@miglioli.com.br (Lucas Miglioli, contato RDAP; domínio antigo)
Não-sócios:
- pamela.reis@m3bs.com.br — Pâmela (Reis) Sposito, coordenadora de Regulatório; posts 2022-11-14 (https://m3bs.com.br/justica-federal-determina-revogacao-da-resolucao-cfm-no-1-673-03/), 2023-02-10, 2023-03-07 ("Contate-nos através do e-mail pamela.reis@m3bs.com.br ou por telefone (11) 3115-2282"); grafias com erro: pamela.resi@m3bs.com.br (2023-03-14) e pamela@m3bs.com.br (2023-03-20) [CONFIRMADO — fonte primária do site]
PADRÃO INFERIDO: sócios = primeironome@m3bs.com.br (4 de 5; Scarabel = sobrenome); não-sócios = nome.sobrenome@m3bs.com.br (1 amostra confirmada: pamela.reis@) [PROVÁVEL]. Nenhum e-mail pessoal de RH/coordenador além de Pâmela foi encontrado no corpus.

## 5. ENDEREÇOS (ATUAL E ANTERIORES)
- ATUAL (RFB 09/2026, site, LinkedIn): Avenida Paulista, 854 – 3º andar, Bela Vista, São Paulo/SP, CEP 01310-913. Site /contato/: recepção pela "Alameda Joaquim Eugênio de Lima, 424 (recepção)" (entrada lateral do mesmo edifício). Vizinhos listados pela Casa dos Dados no mesmo endereço: "CONSORCIO ESTACIONAMENTO SHOPPING TOP CENTER", "EXP TOP CENTER REFEICOES LTDA" → o nº 854 da Paulista é o complexo Top Center (PROVÁVEL).
- ANTERIOR: Alameda Jaú, 1.754, Jardim Paulista, CEP 01420-002, São Paulo/SP — "8 e 11º andares" na Política de Privacidade do site ("inscrito no CNPJ/MF sob o nº 07.848.463/0001-57, com sede na Alameda Jaú, 1.754, 8 e 11º andares, Jardim Paulista, CEP 01420-002" — ainda não atualizada); "1º andar" no Sympla do Summit Academia M3BS de 29/05/2025 (outro finder); LinkedIn showcase "M3BS Licita" JSON-LD: "streetAddress":"Alameda Jaú 1754","postalCode":"01420-002".
- Data da mudança: entre jun/2025 e set/2026 (Sympla 29/05/2025 ainda Jaú; RFB atualizada em 2026-09-12 já Paulista; rodapé do site em 10/2026 Paulista). Nenhum post sobre a mudança (outro finder). [PROVÁVEL]
- Taubaté (filial baixada 2008): Av. Francisco Barreto Leme, 976, Jardim Califórnia, CEP 12062-001.
- Telefone único em todas as fontes: (11) 3115-2282 (RFB, site, posts). Filial Taubaté: (11) 3104-3875 (histórico).

## 6. NOMES ANTERIORES DA SOCIEDADE E LINHA DO TEMPO SOCIETÁRIA
- "Miglioli e Bianchi Advogados" — nome do registrante no registro.br (RDAP, entidade alterada em 2017-06-12 e nunca mais); bylines ConJur de Borrozzino 17/09/2020 e 18/12/2023 ("sócio do escritório Miglioli e Bianchi Advogados"); Glassdoor; YouTube "Miglioli e Bianchi na Rádio EBC" (c. 2018); webinar 2020 "Lucas Miglioli (Sócio de Miglioli e Bianchi Advogados...)". [CONFIRMADO como nome usado 2017-2021, ainda em bylines 2023]
- Razão social atual com os cinco nomes: em uso desde pelo menos 03/03/2022 (ConJur); entrada de Scarabel no QSA registrada em 21/03/2022.
- Nome intermediário (2014-2022, com Borrozzino e Bellinatti mas sem Scarabel — ex.: "Miglioli, Bianchi, Borrozzino e Bellinatti Advogados"): NÃO localizado em nenhuma fonte do corpus (grep em todos os arquivos). INCERTO se existiu como razão social; a marca pública era "Miglioli e Bianchi".
- Nome em 2005-2010 (só Miglioli como sócio): desconhecido (INCERTO). O domínio miglioli.com.br (2004) sugere marca "Miglioli Advogados".
- "Constituído em 2009" (LinkedIn M3BS Advogados e M3BS Licita: "Fundada em 2009"; site: "foi constituído em 2009") vs. abertura do CNPJ em 01/09/2005: CONCILIAÇÃO (PROVÁVEL): o CNPJ é da sociedade individual de Lucas Miglioli (2005, com filial em Taubaté 2005-2008); a sociedade "Miglioli e Bianchi" foi acertada em 2009 e formalizada na RFB em 10/05/2010 (entrada simultânea de Bianchi e Borrozzino). O escritório conta sua história a partir de 2009.
- Sigla "M3BS" = M (Miglioli) + 3 B (Bianchi, Borrozzino, Bellinatti) + S (Scarabel): só faz sentido após 2021/2022; domínio m3bs.com.br registrado em 21/09/2021.
- Linha do tempo: 2004-06-29 domínio miglioli.com.br → 2005-09-01 CNPJ aberto (Miglioli sócio-administrador) + filial Taubaté → 2008-03-25 filial Taubaté baixada → 2010-05-10 Bianchi (sócio-adm) e Borrozzino entram → 2014-01-31 Bellinatti entra → 2015-01-01 opção pelo Simples → 2017-06-12 entidade no registro.br nomeada "Miglioli e Bianchi Advogados" → 2021-09-21 domínio m3bs.com.br → 2022-03-03 ConJur: marca M3BS, Scarabel sócio, "primeira filial em Fortaleza", "mais de 450 clientes" → 2022-03-21 Scarabel no QSA → 2022-10-31 exclusão do Simples (comunicação obrigatória) → 2022-2024 Lucro Presumido → 2023-07-27/28 criação da página/canal "M3BS Licita" → ≥ jun/2025 mudança Alameda Jaú 1754 → Av. Paulista 854 → 2026-09-12 RFB já com Paulista.

## 7. PORTE, FUNCIONÁRIOS E FATURAMENTO (ESTIMATIVAS)
- Porte RFB: "DEMAIS" (não ME/EPP). MonitorCNPJ (outro finder): "Porte: Médio/Grande".
- Simples Nacional: optante 01/01/2015 → excluída em 31/10/2022 por "Comunicação Obrigatória do Contribuinte" (CNPJá). INFERÊNCIA (PROVÁVEL): a exclusão com efeitos a partir de nov/2022 é o rito de quem ultrapassa em mais de 20% o teto de R$ 4,8 milhões de receita bruta no ano-calendário (comunicação obrigatória até o último dia útil do mês seguinte ao excesso) → receita bruta acumulada jan-out/2022 superou ~R$ 5,76 milhões. Desde 2022 tributada pelo Lucro Presumido (permitido até R$ 78 mi/ano). Capital social R$ 150 mil.
- Faixa de faturamento de Econodata/Informe Cadastral/Casa dos Dados (paga): NÃO OBTIDA — Econodata e Informe Cadastral: HTTP 403 Cloudflare (curl, WebFetch e Playwright: "Executando verificação de segurança"); cnpj.biz: "Acesso Bloqueado — Detectamos uso de VPN, Proxy"; cnpj.info: "Anti-robot JS check"; cnpjagora.com: CONNECT 502; consultacnpj.com: só tela de aceite de termos; Serasa Experian: página abre sem dados ("Cadastre o seu CNPJ e utilize as soluções de Consulta...").
- Funcionários: LinkedIn "51-200 funcionários", "124 funcionários" (M3BS Advogados, 14.746 seguidores em 2026-10-13); showcase M3BS Licita 237 seguidores, "51-200". Glassdoor "Miglioli e Bianchi": "Micro empresa (até 19 funcionários)" (desatualizado). Estimativa Econodata/Casa dos Dados: não obtida (bloqueio/paywall).
- ConJur mar/2022: "mais de 450 clientes espalhados em todo o país e no exterior".

## 8. "M3BS LICITA" — É EMPRESA SEPARADA?  [CONFIRMADO: NÃO — é página showcase/canal de conteúdo do próprio escritório]
- LinkedIn: https://www.linkedin.com/company/m3bs-licita/ redireciona para https://br.linkedin.com/showcase/m3bs-licita/ (tipo SHOWCASE PAGE, não company page). Dados literais (curl 2026-10-13): "M3BS Licita | 237 seguidores no LinkedIn. Visão Jurídica Estratégica | Dicas, explicações descomplicadas, legislação e normativas, informações atualizadas sobre negócios públicos, tanto licitações e contratações diretas, quanto dispensas." ; Site https://m3bs.com.br/ ; Setor "Administração pública, defesa e seguridade social" ; Tamanho "51-200 funcionários" ; Sede "São Paulo, São Paulo" ; "Fundada em 2009" ; Especializações "negócios públicos, Licitações, Dispensas e Contratações Diretas" ; Páginas afiliadas: "M3BS Advogados — Atividades jurídicas — São Paulo, SP". JSON-LD: endereço "Alameda Jaú 1754", "01420-002" (endereço antigo); logo com timestamp 1690469124161 (= 2023-07-27).
- Sem CNPJ próprio encontrado: a raiz 07.848.463 tem apenas 2 estabelecimentos; busca por razão social "M3BS"/"M3BS LICITA" na API da Casa dos Dados bloqueada por Cloudflare (não foi possível excluir um CNPJ homônimo de terceiros, mas não há qualquer indício).
- Sem domínio próprio (m3bslicita.com.br não registrado). E-mail licita@m3bs.com.br e telefone (11) 3115-2282 (post 07/08/2023). Canal lançado no site em 28/07/2023 (https://m3bs.com.br/m3bs-licita/, outro finder); Instagram @m3bslicita (outro finder). Coordenadores da área: Davi Cunha (2023), Vanessa Lira (2025) — outro finder.

## 9. OAB — REGISTRO DA SOCIEDADE (CNSA) E DOS SÓCIOS (CNA)  [NÃO OBTIDO]
- CNSA (https://cnsa.oab.org.br/): app Angular; endpoint descoberto via Playwright: GET https://cnsa.oab.org.br/svc-cns/api/association/paged?SocietyName=Miglioli&Uf=SP&PageNumber=1&PageSize=10 → 428 {"message":"Recaptcha score below threshold","code":"recaptcha_fallback_required"} (headless) e 400 {"message":"Recaptcha token is missing"} (curl). A tela pede "Confirme que você não é um robô".
- CNA (https://cna.oab.org.br/): endpoint GET https://cna.oab.org.br/cna-interno/api/advogado/search?Uf=SP&Nome=Lucas%20Augustus%20Alves%20Miglioli → 428 (reCAPTCHA). Números OAB dos sócios não obtidos por aqui.
- Dado de outro finder: Luis Henrique Borrozzino — OAB/SP 262256 (Análise Advocacia). Os demais números OAB não foram localizados.
- Site e Código de Conduta não citam o nº de registro da sociedade na OAB/SP.

## 10. OUTRAS OBSERVAÇÕES ÚTEIS PARA O DOSSIÊ
- A Política de Privacidade do site ainda cita a sede antiga (Alameda Jaú) — sinal de que documentos institucionais não foram todos atualizados após a mudança (não usar o endereço antigo em correspondência).
- Scarabel entrou como "sócio com capital" (não administrador) em 2022; os únicos administradores legais são Miglioli e Bianchi — decisões de contratação/estrutura passam formalmente por eles. Lucas Miglioli se autodenomina "CEO" (Threads, outro finder).
- O e-mail cadastral da RFB (contato@miglioli.com.br) e o registrante do registro.br ("Miglioli e Bianchi Advogados") mostram que a área administrativa mantém cadastros com a identidade antiga.
- LinkedIn (curl 2026-10-13, https://www.linkedin.com/company/m3bsadvogados/): "M3BS Advogados | 14,746 followers" ; "Legal Services" ; "51-200 employees" ; "Type: Partnership" ; "Founded 2009" ; "Primary: Avenida Paulista 854, 3º andar, São Paulo, SP 01310-913, BR" ; "View all 124 employees" ; funcionários em destaque: Alessandro Gama, Luis Henrique Borrozzino, Marina Modelski, Juliana Antonangeli. Texto "Sobre": "O escritório Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados foi constituído em 2009. Desde então, tem prestado serviços legais da mais alta qualidade a clientes nacionais e internacionais..."

## 11. O QUE FOI TENTADO E NÃO DEU (GAPS)
- WebSearch: orçamento esgotado nesta rodada (nenhuma busca executada): não rodadas "@m3bs.com.br", "07.848.463/0001-57", "Miglioli, Bianchi, Borrozzino e Bellinatti", "M3BS Licita CNPJ", "Miglioli e Bianchi Advogados OAB/SP", "CNSA Miglioli", "escritório Fortaleza M3BS endereço".
- Econodata, Informe Cadastral, The Latin American Lawyer: Cloudflare (403 / desafio JS) em curl, WebFetch e Playwright headless.
- cnpj.biz (bloqueio de proxy/VPN), cnpj.info (anti-robot), cnpjagora.com (túnel 502), consultacnpj.com (aceite de termos sem dados), Serasa Experian (sem dados sem cadastro), Casa dos Dados API de busca por nome (Cloudflare).
- OAB CNSA/CNA: reCAPTCHA obrigatório.
- Faixa de faturamento e nº de funcionários estimados por bureau: não obtidos (só inferências).
- Nome exato da sociedade entre 2005-2010 e entre 2014-2022: não encontrado.
- Endereço/líder da filial de Fortaleza: ConJur não informa; TLAL bloqueado.
