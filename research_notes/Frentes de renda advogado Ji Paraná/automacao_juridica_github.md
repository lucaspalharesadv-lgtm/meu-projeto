# Automação e IA jurídica no Brasil — sinais de adoção verificáveis (GitHub + documentação oficial), outubro de 2026

> **AVISO METODOLÓGICO QUE MUDA A LEITURA DE TUDO ABAIXO.**
> O ambiente desta pesquisa roda atrás de um proxy corporativo que **bloqueou por política (HTTP 403 no CONNECT) todos os domínios `.jus.br`, `.org.br` e `.com.br`** testados. Teste executado em 2026-10-15 ~23:00 UTC:
> `www.oab.org.br => 000`, `www.aurum.com.br => 000`, `juridico.ai => 000`, `themisjuridico.com.br => 000`, `api-publica.datajud.cnj.jus.br => 000`, `comunicaapi.pje.jus.br => 000`, `pypi.org => 200`.
> **Consequência prática:** NÃO foi possível ler em primeira mão a wiki do DataJud, o Termo de Uso em PDF do CNJ, os atos normativos em `atos.cnj.jus.br`, o site da OAB nem as páginas de preços das legaltechs. Tudo que está marcado como **[SECUNDÁRIO]** veio de resumos do buscador ou de espelhos (README de repositórios), e **precisa ser reconferido na fonte primária antes de qualquer decisão de produto**. O que está marcado **[VERIFICADO]** foi lido diretamente (github.com, raw.githubusercontent.com e pypi.org estavam acessíveis).
> Nenhum repositório foi clonado, instalado ou executado. Nenhuma conta foi criada, nenhuma credencial gerada.

---

## 1. APIs e dados oficiais (DataJud, PJe/PDPJ, DJEN, Domicílio Judicial Eletrônico)

### Takeaway
Existe uma camada de dados pública e gratuita razoavelmente boa — DataJud (metadados de processos de 91 tribunais) e DJEN (publicações/intimações, aparentemente sem autenticação) — e ela é a base técnica de praticamente todo produto brasileiro de automação jurídica hoje. Mas **não consegui ler a documentação primária neste ambiente**, e as duas informações comercialmente mais críticas (limite de requisições do DataJud e se o Termo de Uso autoriza uso comercial/revenda) ficaram **sem confirmação primária** — são exatamente as duas que decidem se um produto é viável.

### Cited Findings

**DataJud — API Pública do CNJ**
- A autenticação usa uma chave pública do CNJ no cabeçalho `Authorization: APIKey [Chave Pública]`; a chave é divulgada na wiki oficial e "poderá ser alterada pelo CNJ a qualquer momento" — não é chave individual por usuário. [SECUNDÁRIO] — [resumo de busca sobre termos de uso DataJud](https://formularios.cnj.jus.br/wp-content/uploads/2023/05/Termos-de-uso-api-publica-V1.1.pdf) (PDF oficial identificado na busca, mas **inacessível** daqui)
- Host da API: `api-publica.datajud.cnj.jus.br`; a chave é descrita como "chave pública rotacionada pelo CNJ". [VERIFICADO — leitura direta do README] — [rvsanches/skills-datajud-djen](https://raw.githubusercontent.com/rvsanches/skills-datajud-djen/main/README.md) (lido em 2026-10-15)
- Um servidor MCP ativo afirma que o DataJud cobre **91 tribunais** e que "a variável `DATAJUD_API_KEY` é necessária para consultas ao DataJud CNJ", solicitada em datajud-wiki.cnj.jus.br. Afirma também que **processos em segredo de justiça não são retornados pela API**. [VERIFICADO — leitura direta da página] — [DeHor-Labs/mcp-juridico-brasil](https://github.com/DeHor-Labs/mcp-juridico-brasil) (lido em 2026-10-15)
- **CONFLITO NÃO RESOLVIDO sobre a chave:** uma fonte diz que a chave é pública e já publicada na documentação (basta copiar), outra (guia de terceiro, legalsuite) diz que é preciso registro e gerar chave pessoal. O README do mcp-juridico-brasil fala em "solicitar" a chave. [SECUNDÁRIO] — [resumo de busca](https://legalsuite.com.br/blog/datajud-api-cnj)
- **Limite de requisição: NÃO CONFIRMADO.** Um post no TabNews menciona 120 requisições por minuto citando o termo de uso, mas o próprio autor não sabe se o limite é global ou por IP. O README do skills-datajud-djen apenas lista "circuit breaker, rate limiting" como tema, **sem número**. [SECUNDÁRIO / DESCONHECIDO] — [TabNews — discussão sobre limite da API](https://www.tabnews.com.br/lukexp/4b2885d9-cbae-49ce-8647-b15e7847976d)
- Termo de uso (trechos relatados): a API destina-se a "fins legais e autorizados", uso indevido/abusivo é proibido, o usuário se responsabiliza pelo uso da interface e das informações derivadas, e o CNJ reserva-se o direito de alterar as regras. **A cláusula de "finalidade não comercial" foi citada por um projeto open source mas NÃO apareceu nos trechos oficiais recuperados.** [SECUNDÁRIO — não verificável daqui]
- A API entrega **metadados processuais de processos públicos, sem o conteúdo dos documentos**. [SECUNDÁRIO]
- O README do mcp-brasil cita a **Res. CNJ 446/2022** na seção de disclaimers, como referência à Política de Uso Aceitável. [VERIFICADO — leitura direta] — [Mcp-Brasil/mcp-brasil](https://github.com/Mcp-Brasil/mcp-brasil)

**DJEN — Diário de Justiça Eletrônico Nacional**
- Host de produção: `comunicaapi.pje.jus.br`; homologação `hcomunicaapi.cnj.jus.br`. Documentação oficial em Swagger no SwaggerHub (`app.swaggerhub.com/apis-docs/cnj/pcp/1.0.0`). [SECUNDÁRIO, origem Portal CNJ] — [CNJ — Orientações aos Tribunais](https://www.cnj.jus.br/programas-e-acoes/processo-judicial-eletronico-pje/comunicacoes-processuais/orientacoes-aos-tribunais/) (**inacessível daqui**)
- A documentação oficial do CNJ trata do **envio** de comunicações pelos tribunais e exige "credenciais do Corporativo do CNJ com permissão de acesso à plataforma". [SECUNDÁRIO]
- A **consulta** pública é descrita como `GET /api/v1/comunicacao`, com filtros por OAB+UF, número do processo, sigla do tribunal e janela de datas, e certidão em PDF em `GET /api/v1/comunicacao/{hash}/certidao`. **Essa parte aparece só em fonte secundária, não na documentação oficial recuperada.** [SECUNDÁRIO] — [ChatJurídico — API do DJEN](https://chatjuridico.com.br/api-do-djen-consulta-oficial-cnj/)
- Caracterização técnica independente e mais confiável: DJEN acessível **"sem autenticação"**; `itensPorPagina` com **máximo 50**; `count` limitado a **~10.000**; **geo-bloqueio com 403 para IPs fora do Brasil**; **"rate limit não documentado"**; "sem SLA nem versionamento formal" e tudo pode mudar "sem aviso". [VERIFICADO — leitura direta do README] — [rvsanches/skills-datajud-djen](https://raw.githubusercontent.com/rvsanches/skills-datajud-djen/main/README.md)
- A consulta programática é **pull**: a fonte responde o que você perguntar, mas **não avisa quando sai publicação nova** (não há webhook/push). [SECUNDÁRIO] — [Lexnode — API do DJEN](https://www.lexnode.com.br/blog/api-do-djen)
- Consulta humana (não-API) em `comunica.pje.jus.br/consulta`, com filtros por OAB, nome do advogado, número do processo ou nome da parte. [SECUNDÁRIO]

**Domicílio Judicial Eletrônico (DJE) e repartição DJE × DJEN**
- Resolução CNJ nº 455/2022 disciplina o DJE e o DJEN; a Resolução CNJ nº 569, de 13/08/2024, a alterou. [SECUNDÁRIO, atos identificados na busca] — [Resolução CNJ 455/2022](https://atos.cnj.jus.br/atos/detalhar/4509); [Resolução CNJ 569/2024](https://atos.cnj.jus.br/atos/detalhar/5691) (**ambas inacessíveis daqui**)
- Após a 569/2024, o **DJE ficou restrito a citações eletrônicas e comunicações que exigem intimação pessoal da parte/terceiro**; **as intimações dirigidas a advogados passam pelo DJEN**. [SECUNDÁRIO]
- Cadastro no DJE é **obrigatório para órgãos públicos e empresas**, com isenção para micro e pequenas empresas com Redesim atualizado; **facultativo para pessoas físicas**. [SECUNDÁRIO]
- Regra dos 10 dias: sem confirmação de leitura em 10 dias corridos do envio ao DJE, a comunicação é considerada realizada no último dia do prazo. [SECUNDÁRIO]
- Para intimação via DJEN, **não há mais prazo de 10 dias para leitura**: o prazo processual corre do **primeiro dia útil após a data de publicação no DJEN**. [SECUNDÁRIO] — [AASP — novas regras de contagem de prazos](https://www.aasp.org.br/comunicado/atencao-as-novas-regras-sobre-contagem-de-prazos-processuais/)
- Há crítica pública relevante: as comunicações via DJE foram apontadas como geradoras de insegurança e violadoras da legislação. [SECUNDÁRIO] — [ConJur, 29/05/2024](https://conjur.com.br/2024-mai-29/comunicacoes-processuais-via-domicilio-judicial-eletronico-inseguranca-e-violacao-a-legislacao/)

**PJe / PDPJ e consultas dos tribunais**
- Não existe uma "API do PJe" unificada e aberta equivalente ao DataJud. O que aparece são: (a) a PDPJ, consultada por projetos de terceiros; (b) sistemas tribunal a tribunal (eSAJ/TJSP, eproc, Projudi) que exigem **scraping**, não API. [VERIFICADO — inferido da cobertura declarada dos repositórios, ver seção 2]
- O raspador `juscraper` declara cobertura por sistema, não por API única: STF, TJSP (cpopg, cposg, cjsg, cjpg), TJES, TJTO, TJAP (**indisponível: CAPTCHA Cloudflare Turnstile**), TJBA, TJCE, TJDFT, TJMT, TJPA, TJPB, TJPI, TJPR, TJRN, TJRO, TJRR, TJRS, TJSC, TJPE, além de Datajud, Jusbr e **PDPJ** (cpopg, documentos, movimentos, partes, pesquisa, download_documents). [VERIFICADO — leitura direta] — [jtrecenti/juscraper](https://github.com/jtrecenti/juscraper)
- Autenticação no PJe com certificado digital é problema de engenharia real e tem solução open source: `MrSchrodingers/pje_headless`, "Autenticador headless compatível com o PJe Office (Jus.br)", Go, 7 estrelas, atualizado em 19/06/2026. [VERIFICADO] — [GitHub topics/pje](https://github.com/topics/pje)
- Existe módulo **oficial do governo** para peticionamento eletrônico no SEI: `anatelgovbr/mod-sei-peticionamento`, "Projeto Oficial do Módulo do SEI de Peticionamento e Intimação Eletrônicos", PHP, GPL-3.0, 30 estrelas, 19 forks, último push **2026-10-06**. [VERIFICADO — GitHub API]

### Inferences
- A combinação **DataJud (metadados, com chave) + DJEN (publicações, sem autenticação, geo-restrito ao Brasil)** é o par de blocos de construção confiáveis. Tudo o mais — conteúdo de peças, documentos, autos — exige scraping ou credencial do advogado, com risco técnico (CAPTCHA, Cloudflare) e jurídico maior.
- O fato de o DJEN ser **pull sem webhook** é a oportunidade de produto mais óbvia e mais verificável desta pesquisa: um serviço de polling + deduplicação + notificação + prazo calculado é exatamente a lacuna entre o dado público grátis e o que as legaltechs cobram R$ 79–220/mês (seção 3).
- O geo-bloqueio do DJEN (403 fora do Brasil) significa que qualquer produto SaaS precisa de infraestrutura hospedada no Brasil — barreira pequena, mas elimina o deploy ingênuo em Vercel/us-east-1.
- A ausência de SLA e de versionamento formal nas APIs do CNJ é risco de produto, não detalhe: um produto que promete monitoramento precisa de fallback e de contrato que não garanta o que o CNJ não garante.

### Gaps
- **Limite de requisições do DataJud: desconhecido.** O número 120 req/min circula, mas não pude ler o Termo de Uso oficial (PDF em `formularios.cnj.jus.br`, bloqueado).
- **Uso comercial dos dados do DataJud: não confirmado.** Há indício de cláusula de finalidade não comercial citada por terceiros, mas não apareceu nos trechos oficiais. **Esta é a pergunta mais importante que ficou aberta** — ela decide se um produto pago sobre DataJud é legítimo.
- **Rate limit do DJEN: não documentado** (afirmação explícita da fonte técnica, não é omissão minha).
- Não consegui ler o Swagger oficial do CNJ para confirmar se o endpoint público de consulta do DJEN existe formalmente ou é uso tolerado.
- Não consegui ler o texto vigente das Resoluções 455/2022 e 569/2024.

---

## 2. GitHub — sinais de adoção (estrelas, forks, último commit, licença, releases, pacotes)

### Takeaway
O ecossistema existe, está **vivo e acelerou em 2026**, mas é **raso**: fora de dois ou três projetos, quase tudo tem menos de 50 estrelas, poucos commits e um único autor. O padrão dominante de 2026 é **servidor MCP + skill de agente** — ou seja, o ecossistema já migrou de "biblioteca para dev" para "ferramenta para agente de IA", que é exatamente o perfil de quem encomendou esta pesquisa.

**Critério de classificação usado:** VIVO = último push ≤ 6 meses (≥ 2026-04-15); MORNO = 6 a 18 meses; ABANDONADO = > 18 meses. Datas de `pushed_at` obtidas via API do GitHub em 2026-10-15; datas "Updated on" obtidas das páginas de tópicos na mesma data.

### Cited Findings — tabela de projetos

Fonte das linhas com `pushed_at` em formato ISO: **[VERIFICADO]** consulta à API de busca do GitHub (`search/repositories`) em 2026-10-15 ~23:05 UTC. Linhas com data em formato "Mmm DD, AAAA": **[VERIFICADO]** páginas [github.com/topics/datajud](https://github.com/topics/datajud) e [github.com/topics/pje](https://github.com/topics/pje), lidas em 2026-10-15.

| Projeto | Link | ⭐ | Forks | Último commit/push | Licença | Linguagem | Status |
|---|---|---|---|---|---|---|---|
| Mcp-Brasil/mcp-brasil — MCP para 70 APIs públicas brasileiras, inclui feature `datajud` (7 tools) e `jurisprudencia` STF/STJ/TST (6 tools) | https://github.com/Mcp-Brasil/mcp-brasil | **1.809** | 283 | 2026-09-19 | MIT | Python | **VIVO** |
| Vaquill-AI/awesome-legaltech — lista curada de legaltech open source (global, não BR) | https://github.com/Vaquill-AI/awesome-legaltech | 246 | 127 | 2026-09-10 | nenhuma | — | **VIVO** |
| DeHor-Labs/mcp-juridico-brasil — MCP de acompanhamento processual sobre o DataJud, 91 tribunais | https://github.com/DeHor-Labs/mcp-juridico-brasil | **114** | 27 | 2026-09-14 | MIT | Python | **VIVO** |
| jtrecenti/juscraper — raspador de tribunais (TJSP, PDPJ, Datajud, Jusbr, ~18 TJs) | https://github.com/jtrecenti/juscraper | 54 | 21 | 2026-10-14 | MIT | Python/HTML | **VIVO** |
| chapirousIA/pje-mcp-server | https://github.com/chapirousIA/pje-mcp-server | 42 | 22 | 2025-06-13 | MIT | JavaScript | **MORNO** (16 meses) |
| nferdica/brazil-visible-sdk — SDK TS para 93+ fontes públicas BR | https://github.com/nferdica/brazil-visible-sdk | 41 | 9 | 2026-03-30 | MIT | TypeScript | **MORNO** (6,5 meses) |
| marcosmarf27/pje-ia — extensão Chrome gratuita para ler/analisar processos do PJe | https://github.com/marcosmarf27/pje-ia | 39 | 10 | 2026-10-13 | nenhuma | — | **VIVO** |
| anatelgovbr/mod-sei-peticionamento — módulo **oficial** SEI de peticionamento e intimação | https://github.com/anatelgovbr/mod-sei-peticionamento | 30 | 19 | 2026-10-06 | GPL-3.0 | PHP | **VIVO** |
| rvsanches/skills-datajud-djen — Agent Skills com conhecimento de produção das APIs CNJ | https://github.com/rvsanches/skills-datajud-djen | 27 | 9 | 2026-07-12 | MIT | — | **VIVO** |
| abjur/datajudScraper — dados do Painel de Estatísticas (DataJud) | https://github.com/abjur/datajudScraper | 23 | 3 | 2023-01-24 | NOASSERTION | R | **ABANDONADO** |
| Mipdv/API-CNJ — consultas simplificadas junto à **PDPJ** | https://github.com/Mipdv/API-CNJ | 22 | 2 | 2026-09-11 | nenhuma | Java | **VIVO** |
| hadtrindade/conversor-e-divisor — conversor/divisor de mídias para o PJe | https://github.com/hadtrindade/conversor-e-divisor | 14 | — | Oct 17, 2022 | — | Python | **ABANDONADO** |
| DanielFillol/DataJUD_API_CALLER | https://github.com/DanielFillol/DataJUD_API_CALLER | 9 | — | Oct 27, 2023 | — | Go | **ABANDONADO** |
| MrSchrodingers/pje_headless — autenticador headless do PJe Office (Jus.br) | https://github.com/MrSchrodingers/pje_headless | 7 | — | Jun 19, 2026 | — | Go | **VIVO** |
| TeamGHCP/JusTraduz — SaaS legaltech PHP/MySQL com IA e consultas DataJud | https://github.com/TeamGHCP/JusTraduz | 5 | — | Sep 14, 2026 | — | PHP | **VIVO** |
| Mosimann-adv/tarrafa_scraper — CLI multi-fonte de captura, inclui DJEN e Datajud | https://github.com/Mosimann-adv/tarrafa_scraper | 5 | — | Aug 31, 2026 | — | Python | **VIVO** |
| pliniohavila/destaque-de-prazos-PJE-TJMG | https://github.com/pliniohavila/destaque-de-prazos-PJE-TJMG | 4 | — | Jan 2, 2023 | — | JavaScript | **ABANDONADO** |
| Dramorimrodrigues/maat-monitor — monitor local-first de processos via DataJud | https://github.com/Dramorimrodrigues/maat-monitor | 3 | — | Sep 16, 2026 | — | Python | **VIVO** |
| lorenzoalberto/datajud-sdk — SDK TypeScript do DataJud com paginação e tipagem | https://github.com/lorenzoalberto/datajud-sdk | 3 | — | Aug 3, 2026 | — | TypeScript | **VIVO** |
| fxbarros/MCP-PJe-TJMA — MCP para consultar PJe-TJMA via Claude Desktop | https://github.com/fxbarros/MCP-PJe-TJMA | 3 | — | Jul 18, 2026 | — | Python | **VIVO** |
| ehrodan/lexmcp — MCP de dados jurídicos BR (DataJud, LexML, prazos CPC, minutas) | https://github.com/ehrodan/lexmcp | 2 | — | Jul 24, 2026 | — | HTML | **VIVO** |
| cleisabino/datajud-cli — CLI Python da API pública DataJud | https://github.com/cleisabino/datajud-cli | 2 | — | May 14, 2026 | — | Python | **VIVO** |
| reluviari/datajud-consulta-processual — interface Flask de consulta | https://github.com/reluviari/datajud-consulta-processual | 2 | — | May 14, 2026 | — | HTML | **VIVO** |
| Fransuelton/teste-incaas | https://github.com/Fransuelton/teste-incaas | 2 | — | Jun 13, 2025 | — | HTML | **MORNO** |
| FlaviaLopes/CNJINOVA-DESAFIO2 — desafio CNJ Inova 2020 | https://github.com/FlaviaLopes/CNJINOVA-DESAFIO2 | 2 | — | Oct 21, 2020 | — | JavaScript | **ABANDONADO** |
| luccas-amorim/argos — monitoramento determinístico de tribunais superiores e fontes CNJ | https://github.com/luccas-amorim/argos | 1 | — | Oct 4, 2026 | — | Python | **VIVO** |
| lucmolero/nanojud — toolkit Python para eSAJ/TJSP, DataJud e DJEN | https://github.com/lucmolero/nanojud | 1 | — | Oct 15, 2026 | — | Python | **VIVO** |
| hebervalverde/mcp-consulta-processual-tjes — MCP e CLIs TJES (DataJud e Solr) | https://github.com/hebervalverde/mcp-consulta-processual-tjes | 1 | — | May 26, 2026 | — | Python | **VIVO** |
| gabrielmaialva33/juridicai — SaaS multi-tenant de gestão de escritório | https://github.com/gabrielmaialva33/juridicai | 1 | — | Jul 2, 2026 | — | TypeScript | **VIVO** |
| ricarossetto/Atrium-Senda — gestão local-first para escritórios BR | https://github.com/ricarossetto/Atrium-Senda | 1 | — | Sep 12, 2026 | — | JavaScript | **VIVO** |
| alexander-stack1/jurimetria-trabalhista-bancaria — jurimetria educacional com DataJud (TRT1) | https://github.com/alexander-stack1/jurimetria-trabalhista-bancaria | 1 | — | Aug 31, 2026 | — | Jupyter | **VIVO** |
| ML-Axis/triagem-acordo-trabalhista — subagente Claude Code para triagem trabalhista | https://github.com/ML-Axis/triagem-acordo-trabalhista | 0 | — | Jun 20, 2026 | — | Shell | **VIVO** |

**Dados agregados de volume**
- O tópico `datajud` no GitHub lista **28 repositórios públicos**; a página mostra 20 sem expandir. [VERIFICADO] — [github.com/topics/datajud](https://github.com/topics/datajud)
- O tópico `pje` lista **13 repositórios**. [VERIFICADO] — [github.com/topics/pje](https://github.com/topics/pje)
- A busca `datajud OR djen OR peticionamento OR "processo judicial eletronico"` retornou `total_count: 2027`, mas a maioria dos top-25 por estrelas é ruído (projetos Django com "djen" no nome, `Quantco/datajudge` que é qualidade de dados, livros de Python). O núcleo realmente jurídico-brasileiro é o que está na tabela acima. [VERIFICADO — API do GitHub, 2026-10-15]

**Detalhes de repositório lidos diretamente (2026-10-15)**
- `Mcp-Brasil/mcp-brasil`: 1,8k estrelas, 283 forks, **53 watchers**, **246 commits**, **seção Releases vazia (nenhuma release publicada)**, licença MIT. Feature `datajud` descrita como "processos judiciais, movimentações", 7 tools, **chave de API opcional**. Não cita DJEN nem PJe. Contagem de contributors: **desconhecida** (seção presente, sem número renderizado). — https://github.com/Mcp-Brasil/mcp-brasil
- `DeHor-Labs/mcp-juridico-brasil`: 114 estrelas, 27 forks, **apenas 14 commits**, MIT, **sem releases visíveis**, contributors **desconhecido**. `HTTP_TIMEOUT` padrão 30s; sem rate limit documentado. — https://github.com/DeHor-Labs/mcp-juridico-brasil
- `jtrecenti/juscraper`: 54 estrelas, 21 forks, **1.023 commits**, MIT, contributors e releases **desconhecidos na página**. — https://github.com/jtrecenti/juscraper

**Pacotes publicados (PyPI — `pypi.org` estava acessível)**
- `juscraper` **v0.4.0**, **10 releases**, último upload **2026-09-15T21:20:53**, licença MIT (Copyright 2024, Julio Trecenti). Summary: "Raspador de tribunais e outros sistemas relacionados ao poder judiciário." [VERIFICADO] — https://pypi.org/project/juscraper/
- `nanojud` **v0.5.1**, **apenas 2 releases**, último upload **2026-10-15T19:36:52** (mesmo dia da pesquisa), summary: "NanoJud: toolkit Python para extração responsável, normalização e exportação de dados públicos". Licença não declarada no campo `license`. [VERIFICADO] — https://pypi.org/project/nanojud/
- Os nomes `datajud`, `pyjud` e `cnj-datajud` **não existem no PyPI** (404 na API JSON). [VERIFICADO]
- **Contagem de downloads: DESCONHECIDA.** `pypistats.org` foi bloqueado pelo proxy (403 no CONNECT) e o PyPI não expõe downloads na API JSON. Não estimei.
- Não verifiquei pacotes npm (o SDK TypeScript `lorenzoalberto/datajud-sdk` e o `nferdica/brazil-visible-sdk` são candidatos óbvios) — **gap**.

### Inferences
- **Há exatamente um projeto com massa crítica real** (`mcp-brasil`, 1,8k estrelas, 283 forks) e ele não é jurídico-especializado: é um agregador de 70 APIs públicas em que o DataJud é uma feature entre muitas, e **nem toca DJEN ou PJe**. Isso é a melhor notícia desta pesquisa para quem quer construir: o nicho especificamente jurídico ainda não tem um vencedor open source.
- O segundo colocado (`mcp-juridico-brasil`, 114 estrelas) conseguiu 114 estrelas e 27 forks **com 14 commits**. Isso é sinal de demanda muito maior que oferta: quase qualquer coisa funcional nesse nicho ganha tração desproporcional ao esforço.
- `juscraper` é o projeto tecnicamente mais sério (1.023 commits, 10 releases no PyPI, mantenedor conhecido da jurimetria brasileira/abjur) e é o bloco de construção que eu trataria como confiável para scraping de tribunais.
- A concentração de últimos commits em **jul–out/2026** (pelo menos 15 dos 32 projetos da tabela) indica que o ecossistema está em expansão agora, não em declínio. O padrão MCP/skill domina os projetos novos.
- Quase nenhum projeto tem release publicada, licença clara em todos os casos, ou mais de um contribuidor identificável. **Nenhum deles é uma dependência que eu colocaria no caminho crítico de um produto pago sem fork e manutenção própria.**

### Gaps
- **Contagem de contribuidores: desconhecida para todos os projetos.** As páginas HTML do GitHub não renderizaram o número via WebFetch e a API de busca não traz o campo; o endpoint `repos/{owner}/{repo}/contributors` foi negado (sessão `gh` restrita aos repositórios configurados).
- **Downloads de PyPI e npm: desconhecidos** (pypistats bloqueado; npm não consultado).
- Não pesquisei explicitamente os termos "jusbrasil scraper", "escavador" e "oab" como buscas isoladas no GitHub — a busca combinada falhou por limite de 5 operadores booleanos da API e não houve orçamento para refazer. Possível subcobertura nesse recorte.

---

## 3. Mercado de produto — legaltechs para advogado autônomo e pequeno escritório

### Takeaway
A faixa de preço que o mercado brasileiro aceita para advogado solo está, consistentemente entre fontes, em **R$ 55–220/mês** para IA jurídica e **R$ 90–380/mês** para gestão de escritório. **Nenhum preço abaixo foi lido na página oficial do fornecedor** — todos os sites de legaltech estavam bloqueados — e as fontes secundárias divergem bastante entre si.

### Cited Findings

**IA jurídica (geração de peças, pesquisa de jurisprudência)**
- **Jurídico AI**: página oficial de planos citada como "a partir de R$ 55,92/mês" no plano anual, com plano gratuito sem cartão; outro blog cita R$ 79/mês; uma terceira tabela cita R$ 149/mês para planos individuais e outra R$ 99–299. **Fontes em conflito.** [SECUNDÁRIO] — [juridico.ai/planos-valores](https://juridico.ai/planos-valores/) (inacessível daqui); [comparativo](https://ialocus.com.br/blog/post-ia-juridica-preco.html)
- **Themis**: página oficial citada com **Plano Inicial R$ 69,90/mês, Avançado R$ 129,99/mês, Pro R$ 199,99/mês**, cobrança mensal, 7 dias de garantia, sem fidelidade. Um guia de 2025 citava R$ 89/mês no plano Solo (provavelmente desatualizado). [SECUNDÁRIO] — [themisjuridico.com.br](https://themisjuridico.com.br/) (inacessível daqui)
- **Jusbrasil / Jus IA**: blog de out/2026 informa que, para o advogado autônomo, os planos vão de **R$ 78,90 a R$ 208,90/mês**; outro guia afirma que desde **abril de 2026 o Jus IA vem incluído em todos os planos pagos sem custo adicional**, com anuais a partir de 12x R$ 58,90. [SECUNDÁRIO] — [Jus IA guia 2026](https://juridicoagil.com/blog/introducao-a-jus-ia-a-revolucao-da-inteligencia-artificial-no-direito)

**Gestão de escritório**
- **Astrea (Aurum)**: o site oficial destaca um plano a **R$ 379/mês no anual e R$ 439/mês no mensal**; um comparativo cita entrada ~R$ 89/mês por usuário e plano Completo ~R$ 179/usuário; outro menciona plano gratuito limitado. **Fontes em conflito — provavelmente planos diferentes (por usuário vs. pacote).** [SECUNDÁRIO] — [aurum.com.br/astrea](https://www.aurum.com.br/astrea/) (inacessível daqui)
- **ADVBOX**: ficha atualizada em set/2026 indica **4 planos: R$ 220, R$ 450, R$ 900 e R$ 1.800/mês**, a partir do Essencial a R$ 220/mês, **mais taxa de ativação única cobrada à parte**. Outro blog cita plano básico ~R$ 99/mês por usuário. [SECUNDÁRIO] — [melhorcrm.com/juridico/advbox](https://melhorcrm.com/juridico/advbox/)
- **Projuris ADV**: fontes divergem entre "a partir de R$ 197/mês com modelo modular e IA vendida à parte", "R$ 170 flat rate per month" (GetApp) e "preço sob consulta". [SECUNDÁRIO] — [GetApp — Projuris ADV](https://www.getapp.com/legal-law-software/a/saj-adv/)
- **Legal One e Lawdesk**: **nenhum preço público encontrado.** [GAP]

### Inferences
- O teto psicológico do advogado solo está perto de **R$ 200/mês**; acima disso o produto precisa se posicionar como gestão de escritório, não como ferramenta.
- O movimento do Jusbrasil de **embutir o Jus IA sem custo adicional nos planos pagos (abril/2026)** é o fato competitivo mais relevante: comoditiza "IA jurídica genérica" e empurra qualquer entrante para nichos que o incumbente não cobre — monitoramento confiável de DJEN com cálculo de prazo, automações sob medida, integração com o fluxo específico do escritório.
- Nenhum dos preços encontrados cobre o que o ecossistema open source já faz de graça (consulta DataJud, raspagem). O valor vendável não é o acesso ao dado: é **confiabilidade, prazo calculado, notificação e responsabilidade**.

### Gaps
- **Todos os preços são de terceiros.** Nenhuma página oficial de preços pôde ser lida. Os conflitos (Astrea R$ 89 vs R$ 379; Jurídico AI R$ 55,92 vs R$ 149) não foram resolvidos.
- Legal One e Lawdesk: sem preço público.
- Não encontrei número de clientes, receita ou market share de nenhuma delas.

---

## 4. Vagas — existe demanda paga por quem junta Direito e automação?

### Takeaway
Existe demanda, mas **o perfil híbrido "advogado que programa" quase não aparece como cargo**. O mercado separa: ou vaga de Legal Ops (processos, sem código), ou vaga de dev (código, sem Direito). A evidência que encontrei é fina e vem toda de agregadores.

### Cited Findings
- **Chazin Mello Secondment — Desenvolvedor(a) Pleno – Legal Operations**: criar scripts e apoiar rotinas de sistemas jurídicos; PJ, remoto com presença ocasional em São Paulo. É a vaga mais próxima do perfil híbrido encontrada. [SECUNDÁRIO, agregador] — [Indeed — Legal Ops](https://br.indeed.com/q-legal-ops-vagas.html)
- **Jusbrasil**: vagas remotas de Legal Ops, incluindo um **Team Lead de Operações Jurídicas envolvendo automações com IA**, além de vagas técnicas que pedem Python. [SECUNDÁRIO] — [Remote Rocketship — Jusbrasil](https://www.remoterocketship.com/br/empresa/jusbrasil-com-br/)
- **Elaw Tecnologia — Analista de Legal Ops Pleno** (Rio de Janeiro, sem indicação de remoto nem de Python). [SECUNDÁRIO]
- Faixa salarial estimada para Legal Operations no Brasil: **R$ 51.000 a R$ 81.000/ano**, variando com experiência e empresa — estimativa de agregador, não oferta concreta. [SECUNDÁRIO] — [bebee — Legal Operations Brasil](https://bebee.com/br/jobs/role/legal-operations)
- Uma vaga de automação com Python remota citou **R$ 8.600/mês (PJ ou CLT)** — **não é legal ops**, serve só como referência do preço do lado "automação". [SECUNDÁRIO]
- Agregadores com listagens no recorte: [Indeed Legal Ops](https://br.indeed.com/q-legal-ops-vagas.html), [Glassdoor — 48 vagas legal support remoto](https://www.glassdoor.com.br/Vaga/trabalho-remoto-legal-support-vagas-SRCH_IL.0,15_IS12226_KO16,29.htm), [Remote Rocketship — jurídico](https://www.remoterocketship.com/br/vagas/juridico/), [bebee — 105+ vagas Legal Operations Brasil 2026](https://bebee.com/br/jobs/role/legal-operations)

### Inferences
- O arbitrage está evidente nos números: Legal Ops puro paga ~R$ 4,2–6,8 mil/mês (R$ 51–81 mil/ano), enquanto automação com Python sozinha paga R$ 8,6 mil/mês. Quem junta os dois tem argumento para o teto da faixa de dev, não o da faixa jurídica — mas **não achei nenhuma vaga que precifique explicitamente o híbrido**, então isso é inferência, não dado.
- Para o objetivo do usuário (advogado que opera ferramentas de código), o caminho de renda com evidência mais forte **não é CLT/PJ em vaga de legal ops** — é vender automação a escritórios, porque é lá que há preço de tabela público e concorrência mapeável (seção 3).

### Gaps
- Nenhuma vaga com faixa salarial publicada que exija explicitamente Direito + Python.
- Os links de agregador são listagens dinâmicas: as vagas citadas podem já ter encerrado, e não pude abrir cada anúncio (domínios `.com.br` bloqueados).
- Não pesquisei LinkedIn Jobs nem Gupy diretamente.

---

## 5. Marketplaces de agentes e skills — já se vende automação jurídica pronta?

### Takeaway
**Esta é a pergunta pior respondida da pesquisa.** Há evidência de que se vendem templates n8n no Brasil e de que **já existem templates jurídicos específicos** circulando, mas **não encontrei um único preço, volume de vendas ou taxa de plataforma** para automação jurídica. Sobre Whop e GPT Store, as buscas não retornaram **nada**.

### Cited Findings
- O marketplace oficial do n8n aceita workflows gratuitos e pagos; guias brasileiros descrevem cadastro, precificação e publicação, e recomendam incluir guia ou vídeo de configuração. [SECUNDÁRIO] — [Como vender workflows e templates n8n](https://horadecodar.com.br/vender-workflows-templates-n8n-marketplace/)
- **Já existe concorrência no nicho jurídico**: há vendedores de template de agente jurídico para WhatsApp em site brasileiro de templates n8n, e cursos que incluem como bônus "um template de advocacia que faz triagem, identifica a demanda do cliente e agenda automaticamente". [SECUNDÁRIO] — [Agente de qualificação e marketing jurídico com n8n](https://horadecodar.com.br/agente-qualificacao-marketing-juridico-etico-n8n/)
- Conteúdo em vídeo vendendo o modelo: "Agente de IA Para Advogados no N8N: Como Vender de Forma Automática Serviços Jurídicos no WhatsApp". [SECUNDÁRIO] — [YouTube](https://www.youtube.com/watch?v=nfMah4aGEa8)
- **Hotmart** é o canal brasileiro visível para empacotar automação: há produtos de n8n à venda, geralmente curso + templates (ex.: ["Automação com n8n + de 10 templates prontos"](https://hotmart.com/pt-br/marketplace/produtos/automacao-com-n8n/V99149681D), ["N8N TurboPack"](https://hotmart.com/pt-br/marketplace/produtos/n8n-turbopack-automacao-poderosa-para-escalar-seu-negocio/V98566642B)). **Nenhum voltado a advocacia entre os encontrados.** [SECUNDÁRIO]
- **Gumroad** citado como alternativa para vender templates como produto digital. [SECUNDÁRIO]
- **Sinal indireto forte no GitHub, este sim verificado**: o ativo de maior razão tração/esforço do ecossistema é justamente um pacote de conhecimento vendável — `rvsanches/skills-datajud-djen`, "Agent Skills com conhecimento de produção sobre as APIs públicas do CNJ", 27 estrelas e 9 forks, MIT, atualizado em 2026-07-12. Alguém já está empacotando o know-how de DataJud/DJEN como skill de agente — de graça. [VERIFICADO] — https://github.com/rvsanches/skills-datajud-djen

### Inferences
- Existe oferta inicial de agente jurídico pronto (triagem/WhatsApp/captação), mas o nicho está em estágio de **infoproduto** (curso + template no Hotmart), não de marketplace maduro com preço de tabela. Isso é consistente com a imaturidade vista no GitHub.
- O fato de alguém já ter publicado as skills de DataJud/DJEN sob MIT significa que **o conhecimento das APIs não é mais defensável como produto** — o que é vendável é a operação (rodar, monitorar, responder pelo prazo), não a receita.
- Um template de captação de clientes via WhatsApp esbarra direto nas regras de publicidade da OAB (seção 6) — risco que os vendedores de template atuais parecem tratar superficialmente.

### Gaps
- **Zero dados de preço** de automação jurídica em qualquer marketplace.
- **Whop: nenhum resultado.** **GPT Store: nenhum resultado.** Não posso afirmar que não existe — apenas que não encontrei.
- Não consultei diretamente n8n.io/workflows (domínio não testado) nem o diretório de MCP servers.

---

## 6. Risco regulatório — OAB e CNJ sobre IA

### Takeaway
Do lado do **Judiciário**, a regra é clara e está em vigor: Resolução CNJ 615/2025. Do lado do **advogado**, o quadro em outubro de 2026 é de **vácuo normativo específico**: existe uma Recomendação de 2024 (não vinculante na forma de provimento) e um provimento do Conselho Federal **ainda não publicado**. Na prática, quem automatiza hoje opera sob Estatuto, Código de Ética, LGPD e CPC — e assume o risco de a regra específica chegar depois.

### Cited Findings

**CNJ — Resolução 615/2025**
- Resolução nº 615, de 11 de março de 2025, regulamenta o uso de IA no Poder Judiciário e **substitui a Resolução CNJ nº 332/2020**. Uma fonte indica publicação em 14/03/2025 e vigência a partir de 14/07/2025; outra fala em prazo de até 12 meses para adequação dos tribunais — **datas conflitantes**. [SECUNDÁRIO] — [Resolução 615/2025 no JusLaboris/TST](https://juslaboris.tst.jus.br/handle/20.500.12178/247151); [TRF1/SJGO — CNJ regulamenta uso da IA no Judiciário](https://www.trf1.jus.br/sjgo/noticias/cnj-regulamenta-uso-da-inteligencia-artificial-no-judiciario)
- Conteúdo relatado: supervisão humana é central; IA admitida como apoio à redação de atos e documentos **desde que haja revisão humana posterior**; **vedado** usar IA para analisar depoimentos, prova pericial e documentos dos autos para concluir automaticamente a solução do caso; **expressamente proibidos** sistemas que impeçam ou dificultem a revisão humana de decisões automatizadas; classificação de soluções em **alto e baixo risco** por anexo (baixo risco inclui transcrição de áudio/vídeo e anonimização). [SECUNDÁRIO] — [análise da Resolução 615/2025](https://juridico.ai/juridico/resolucao-cnj-615-2025-ia-no-judiciario/)
- A **OAB tem assento** no comitê nacional de IA previsto na norma, ao lado de Judiciário, MP, Defensoria e sociedade civil. [SECUNDÁRIO]
- Também relevante para uso de dados: Res. CNJ 446/2022 é citada como referência de Política de Uso Aceitável. [VERIFICADO — README do mcp-brasil]

**OAB / CFOAB**
- **Recomendação nº 001/2024**, aprovada pelo Conselho Federal em **11 de novembro de 2024**, com cinco capítulos: legislação aplicável, confidencialidade e privacidade, práticas jurídicas éticas, comunicação sobre o uso de IA generativa, e disposições finais. Vincula o uso ao Estatuto da Advocacia, ao Código de Ética, à LGPD e ao CPC, e inclui **dever de revisão integral do conteúdo gerado** e **supervisão dos sócios sobre associados e estagiários**. [SECUNDÁRIO] — [Proposição 49.0000.2024.007325-9/COP (PDF OAB)](https://s.oab.org.br/arquivos/2024/11/7160d4fe-9449-4aed-80bc-a2d7ac1f5d2f.pdf) (inacessível daqui); [IBET — OAB aprova recomendações](https://www.ibet.com.br/oab-aprova-recomendacoes-para-o-uso-de-inteligencia-artificial-na-advocacia/)
- **Consentimento do cliente**: se o cliente não consentir com o uso de IA, o advogado deve respeitar a decisão e informar abordagens tecnológicas alternativas ou manuais. [SECUNDÁRIO] — [Maeda, Ayres & Sarubbi](https://maedaayres.com.br/info/oab-aprova-recomendacao-sobre-o-uso-de-inteligencia-artificial-generativa-na-pratica-juridica%C2%B9/)
- **OAB/SP** decidiu que **advogados sócios devem garantir supervisão no uso de IA**. [SECUNDÁRIO] — [Migalhas](https://www.migalhas.com.br/quentes/455537/advogados-socios-devem-garantir-supervisao-em-uso-de-ia-decide-oab-sp)
- **Plano Nacional de Integração da Inteligência Artificial na Advocacia (PNIAA)**: anunciado em **10/06/2026** e lançado em **15/06/2026** no Conselho Pleno, em João Pessoa; pesquisa feita com a Universidade de Stanford com ~250 mil profissionais convidados e **18.668 respostas**, primeiros números divulgados em **agosto de 2026**. [SECUNDÁRIO, com origem em notícia oficial da OAB] — [OAB — Conselho Federal anuncia plano nacional](https://www.oab.org.br/noticia/64268/conselho-federal-da-oab-anuncia-plano-nacional-para-integrar-inteligencia-artificial-a-advocacia) (**inacessível daqui**)
- **Provimento específico: ainda não existe.** A OAB afirmou que os resultados da pesquisa servirão de base para um provimento do Conselho Federal. Um guia de **setembro de 2026** afirma que o Código de Boas Práticas de IA na Advocacia e o provimento **ainda não haviam saído**; um texto de julho/2026 estimava 2026 ou 2027. [SECUNDÁRIO] — [juridicoagil — Plano Nacional de IA da Advocacia](https://juridicoagil.com/blog/plano-nacional-ia-advocacia-oab)
- Enquanto não há provimento, as referências que valem são Código de Ética, EOAB, Resolução CNJ 615/2025 e, para publicidade, o **Provimento 205/2021**. [SECUNDÁRIO] — [Como usar IA sem violar a ética da OAB](https://www.jusbrasil.com.br/artigos/como-usar-ia-sem-violar-a-etica-da-oab/5748497466)
- Alerta específico para automação de captação: material técnico sobre n8n para advocacia registra que "a automação precisa ser feita dentro das normas estabelecidas pela OAB". [SECUNDÁRIO] — [horadecodar](https://horadecodar.com.br/agente-qualificacao-marketing-juridico-etico-n8n/)

### Inferences
- **Sobre oferta de serviço jurídico automatizado ao público: não encontrei nenhuma norma que autorize ou proíba expressamente.** O risco real não está em uma norma de IA, mas nas normas antigas — publicidade (Provimento 205/2021), captação de clientela, e exercício ilegal da profissão se um agente der orientação jurídica sem advogado responsável. Um produto B2C que "responde dúvidas jurídicas" é claramente mais arriscado que um produto B2B vendido a advogados.
- O vetor regulatório mais seguro, dado o conjunto de normas: ferramenta **vendida a advogado**, com **revisão humana obrigatória embutida no fluxo**, **registro de auditoria** e **cláusula de consentimento do cliente final sobre uso de IA** — esses três itens são respostas diretas a cláusulas identificadas na Recomendação 001/2024 e na Res. 615/2025.
- A janela de 2026 é favorável a quem constrói: o provimento ainda não saiu, mas a direção já está sinalizada (supervisão humana, consentimento, confidencialidade). Construir já conforme essas três diretrizes reduz o risco de retrabalho.

### Gaps
- **Não li o texto da Recomendação 001/2024, da Resolução 615/2025 nem do Provimento 205/2021.** Todos os domínios oficiais estavam bloqueados. Tudo acima é relato de terceiros.
- **Datas conflitantes** sobre vigência da Res. 615/2025 (14/07/2025 vs. prazo de 12 meses para adequação).
- Nenhuma fonte encontrada trata diretamente de **oferta de serviço jurídico automatizado ao público leigo** — a pergunta ficou essencialmente sem resposta normativa.
- Não localizei manifestação da OAB especificamente sobre **venda de automações/templates jurídicos por advogado** a outros advogados.

---

## FERRAMENTAS E FONTES USADAS

Todas as chamadas foram feitas em **2026-10-15**, entre aproximadamente **22:50 e 23:20 UTC** (relógio do proxy registrado em `2026-10-15T22:52:43Z`). Os horários por item são aproximados dentro dessa janela; o buscador não devolve timestamp por resultado.

**Ferramentas:** `Read` (instruções), `WebSearch` (9 buscas), `WebFetch` (8 fetches, 5 bem-sucedidos), `Bash`/`curl` (4 execuções: teste de conectividade, status do proxy, consulta ao PyPI, parsing JSON), `mcp__github__search_repositories` (2 consultas à API de busca do GitHub), `gh api` (1 tentativa, negada por escopo de sessão), `Write`.

**Lidas diretamente e com sucesso (~23:00–23:12 UTC):**
- https://github.com/topics/datajud — 28 repos, 20 exibidos, com estrelas e datas
- https://github.com/topics/pje — 13 repos com estrelas e datas
- https://raw.githubusercontent.com/rvsanches/skills-datajud-djen/main/README.md — hosts, autenticação DJEN, paginação, geo-bloqueio
- https://github.com/Mcp-Brasil/mcp-brasil — 1.8k⭐, 283 forks, 53 watchers, 246 commits, sem releases, MIT
- https://github.com/DeHor-Labs/mcp-juridico-brasil — 114⭐, 27 forks, 14 commits, MIT, DATAJUD_API_KEY
- https://github.com/jtrecenti/juscraper — 54⭐, 21 forks, 1.023 commits, MIT, cobertura de tribunais
- API de busca do GitHub (`search/repositories`) — `pushed_at`, forks, licença, linguagem de 50 repositórios
- https://pypi.org/pypi/juscraper/json e https://pypi.org/pypi/nanojud/json — versões, nº de releases, data de upload, licença

**Buscas executadas (WebSearch, ~22:53–23:18 UTC):** `github datajud cnj api python`; `DataJud API pública chave pública limite requisições termo de uso CNJ`; `API DJEN comunica.pje.jus.br documentação pública consulta comunicações`; `Astrea ADVBOX Projuris preço mensal advogado autônomo plano 2026`; `CNJ Resolução 615/2025 inteligência artificial Judiciário OAB uso de IA advogado`; `preço mensal Jusbrasil Legal One Themis Lawdesk Juridico.ai plano advogado`; `vaga legal operations automação jurídica Python salário remoto Brasil`; `OAB CFOAB inteligência artificial advogado provimento recomendação 2025 2026`; `Domicílio Judicial Eletrônico obrigatório Resolução CNJ 455 DJEN intimações prazo advogado 2026`; `n8n template jurídico advocacia marketplace agente IA venda Whop GPT store`; `vender automação jurídica pronta marketplace preço n8n workflow advocacia Hotmart Whop`.

**Tentadas e BLOQUEADAS pelo proxy (403 no CONNECT / ENOTFOUND), ~22:55–23:10 UTC:**
- https://datajud-wiki.cnj.jus.br/api-publica/acesso — **documentação primária do DataJud**
- https://formularios.cnj.jus.br/wp-content/uploads/2023/05/Termos-de-uso-api-publica-V1.1.pdf — **Termo de Uso oficial**
- https://www.cnj.jus.br/programas-e-acoes/processo-judicial-eletronico-pje/comunicacoes-processuais/orientacoes-aos-tribunais/
- https://api-publica.datajud.cnj.jus.br/ e https://comunicaapi.pje.jus.br/
- https://www.oab.org.br/noticia/64268/... — notícia oficial do PNIAA
- https://www.aurum.com.br/astrea/planos/ ; https://juridico.ai ; https://themisjuridico.com.br
- https://pypistats.org/api/packages/nanojud/recent — contagem de downloads
- `gh api search/repositories` — negado: "sessions are bound to their configured repositories"

**Restrições respeitadas:** nenhum repositório clonado, instalado ou executado; nenhum script de terceiro rodado; nenhuma conta criada; nenhuma credencial de API gerada; nenhuma compra; ninguém contatado. Nenhum número de estrelas, forks ou data foi estimado — onde o dado não apareceu, está escrito "desconhecido".

---

## COMO CADA FONTE MUDOU A CONCLUSÃO

1. **O bloqueio do proxy aos domínios `.jus.br` / `.com.br`** — mudou a natureza do entregável. A pergunta pedia leitura de fonte primária; o ambiente tornou isso impossível. Resultado: rebaixei toda a seção de APIs e toda a seção regulatória para "relato de terceiros, reconferir", e desloquei o peso probatório da pesquisa para o GitHub e o PyPI, que eram acessíveis. **Sem esse bloqueio, as seções 1 e 6 seriam as mais fortes; com ele, são as mais fracas.**

2. **`github.com/topics/datajud` (28 repos) e `topics/pje` (13 repos)** — derrubaram a hipótese de que "não existe nada". Existe, e com datas de 2026. Mas o tamanho das listas mostrou que o ecossistema é pequeno o bastante para ser mapeado inteiro, o que permitiu a tabela exaustiva em vez de uma amostra.

3. **A API de busca do GitHub (`pushed_at`, forks, licença)** — foi o que permitiu classificar VIVO/MORNO/ABANDONADO com data dura em vez de impressão. Também revelou que boa parte dos 2.027 resultados é ruído (projetos Django com "djen" no nome), o que impediu a conclusão ingênua de "milhares de projetos de legaltech no Brasil".

4. **`Mcp-Brasil/mcp-brasil` com 1,8k estrelas, mas sem DJEN e sem PJe** — mudou a conclusão central sobre oportunidade. O líder absoluto do ecossistema não cobre as duas fontes que importam para o dia a dia do advogado (publicações e autos). Isso transformou "o espaço está tomado" em "o espaço especificamente jurídico está vago".

5. **`DeHor-Labs/mcp-juridico-brasil`: 114 estrelas e 27 forks com 14 commits** — foi o dado que mais mudou a avaliação de esforço/retorno. Demanda muito acima da oferta no nicho; esforço pequeno ganha tração desproporcional.

6. **O README do `skills-datajud-djen` (DJEN sem autenticação, paginação máx. 50, geo-bloqueio 403, rate limit não documentado, sem SLA)** — substituiu suposições por restrições de engenharia concretas e gerou três requisitos de produto: hospedar no Brasil, paginar agressivamente, e não prometer SLA ao cliente que o CNJ não dá. Também mostrou que o know-how das APIs já está publicado sob MIT, o que derrubou a ideia de vender "acesso ao dado" como produto.

7. **A caracterização do DJEN como `pull` sem webhook (Lexnode)** — foi o que converteu a pesquisa em uma tese de produto específica: a lacuna monetizável é polling + deduplicação + cálculo de prazo + notificação, não a consulta em si.

8. **Os preços das legaltechs (R$ 55–220/mês IA; R$ 90–380/mês gestão)** — fixaram o teto de preço de qualquer produto novo para solo. Mas, como todos vieram de blogs e se contradizem entre si, usei-os para definir a **faixa**, nunca um número.

9. **"Jus IA incluído sem custo adicional nos planos pagos do Jusbrasil desde abril/2026"** — mudou a recomendação competitiva. Tornou inviável competir em "IA jurídica genérica" e empurrou a conclusão para nicho operacional.

10. **As vagas (Legal Ops R$ 51–81 mil/ano vs. automação Python R$ 8,6 mil/mês)** — enfraqueceram a tese de emprego e fortaleceram a de produto/serviço. A ausência de vaga que precifique o híbrido foi, ela própria, o achado.

11. **Marketplaces: templates jurídicos existentes no n8n/Hotmart, mas zero resultado para Whop e GPT Store** — impediram qualquer afirmação sobre preço de mercado de automação jurídica pronta. A conclusão virou "estágio de infoproduto, não de marketplace maduro", que é mais fraca e mais honesta do que a pergunta original pressupunha.

12. **Recomendação OAB 001/2024 + ausência de provimento até set/2026 + Res. CNJ 615/2025** — definiram as três travas de design (revisão humana, consentimento do cliente, supervisão/confidencialidade) e deslocaram o risco regulatório real das normas de IA para as normas antigas de publicidade e exercício profissional. Também mostraram que a janela ainda está aberta: a regra específica para advogados não chegou.
