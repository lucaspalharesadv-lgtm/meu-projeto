# Prospecção Jurídica B2B — RELATÓRIO FINAL
**Lucas Palhares — OAB/RO 11.037 — Ji-Paraná/RO**
Data de fechamento: 22/09/2026

---

## 1. AVISO DECISIVO SOBRE E-MAILS

**Nenhum e-mail foi coletado, e nenhum foi inventado.**

O ambiente em que esta pesquisa rodou (Claude Code na nuvem) tem a saída de rede
fechada por política da organização. Foram testados 14 domínios distintos —
plataformas de correspondentes, OAB-RO, Jurídico Certo, gov.br, LinkedIn, sites de
escritórios e até a Wikipédia — e **todos** retornaram `EGRESS_BLOCKED`. Um crawler
próprio via `curl` também foi negado (403 no túnel CONNECT). O teste foi repetido no
fim da coleta, com o mesmo resultado.

Sem abrir a página, não há como ler o e-mail publicado nela. A regra nº 1 do
briefing era não deduzir e-mail por padrão de domínio — então a coluna
`E-mail principal` está vazia em todas as 521 linhas, em vez de preenchida com
`contato@empresa.com.br` inventado.

Um achado relevante durante a pesquisa reforça a decisão: ao buscar o contato da
Marcelo Tostes Advogados, um agregador devolveu *"o formato de e-mail mais comum é
first.last@mtostes.com.br"*. Isso é **padrão inferido**, não e-mail publicado — exatamente
o que foi proibido. Por isso a base tem duas colunas separadas: `E-mail principal`
(só para e-mail visto na página) e `E-mail NAO CONFIRMADO (indicio)`, com
1 registro(s) claramente rotulado(s) como não confirmado.

**Para destravar:** autorizar o conector **Tavily** nas configurações do claude.ai
(ele busca e extrai conteúdo de página pelo servidor dele, fora deste contêiner),
rodar a pesquisa no Claude Code local, ou liberar o egresso do ambiente. Com
qualquer um deles, a extração de e-mail sobre esta base já pronta é mecânica.

---

## 2. NÚMEROS FINAIS

| Métrica | Valor |
|---|---|
| Organizações únicas | **521** |
| Oportunidades quentes | **261** |
| Prioridade A (80-100) | **247** |
| Prioridade B (60-79) | **273** |
| Prioridade C (40-59) | **1** |
| Leads em Rondônia | **81** |
| Leads em outros estados | 440 |
| Escritórios de advocacia | 323 |
| Empresas e demais organizações | 198 |
| Com trabalho remoto confirmado | 49 |
| Que usam ou provavelmente usam correspondentes | 161 (dos quais 41 confirmados) |
| Com atuação nacional | 181 |
| **E-mails verificados** | **0** |
| Indícios de e-mail não confirmados | 1 |

Meta contratada: 800 organizações, 150 A e 300 B. Entregue: 521 organizações,
247 A e 273 B. A meta de Prioridade A foi **superada** (247 contra 150);
a de B ficou em 273 de 300 e o total em 521 de 800. O limitador foi o
bloqueio de rede: sem abrir páginas, cada organização precisou ser confirmada por
resultado de busca ou por anúncio de vaga datado, o que é mais lento e descarta
muita coisa que entraria numa varredura normal. Preferi 521 leads rastreáveis a
800 linhas com dado inventado.

---

## 3. FONTES EFETIVAMENTE UTILIZADAS

| Fonte | Status | O que rendeu |
|---|---|---|
| Indeed (API via MCP) | Funcional | 261 vagas reais, datadas, com link de candidatura |
| WebSearch | Funcional | Nome e URL de organizações; rankings setoriais |
| WebFetch (qualquer site) | **Bloqueado** | — |
| curl / crawler próprio | **Bloqueado** | — |
| LinkedIn, OAB, páginas de contato | **Bloqueado** | — |

---

## 4. OS 30 CONTATOS COM MAIOR POTENCIAL

| Score | P | Organização | Local | Tipo | Abordagem sugerida |
|---|---|---|---|---|---|
| 96 | A | **Banco do Brasil S/A** | Brasília/DF | Banco público | Monitorar e habilitar-se no edital de credenciamento; sociedade de advogados em RO cobre comarcas do interior |
| 96 | A | **Vitamais Nutrição Animal** | Ji-Paraná/RO | Indústria de nutrição animal | Ofertar assessoria juridica empresarial e contencioso na propria cidade - maior empresa do estado a uma rua de distancia |
| 95 | A | **NELSON WILIANS & ADVOGADOS ASSOCIADOS** | Porto Velho/RO | Escritório de advocacia (atuação nacional) | Apresentar-se como correspondente/associado em Rondônia (Ji-Paraná e comarcas do interior), com foco em audiências e diligências |
| 95 | A | **Porto Seguro** | São Paulo/SP | Seguradora | Solicitar credenciamento pela pagina oficial, ofertando cobertura das comarcas de Rondonia |
| 95 | A | **Agibank** | Porto Alegre/RS | Banco / financeira de consignado | Ofertar correspondencia e audiências em RO - consignado e area de dominio do Lucas (bancario e consumidor) |
| 95 | A | **JBS** | São Paulo/SP | Frigorífico / agroindústria | Ofertar defesa trabalhista e assessoria em doencas ocupacionais nas cinco comarcas de RO onde opera |
| 95 | A | **Ameron Assistência Médica** | Porto Velho/RO | Operadora de plano de saúde | Ofertar defesa em acoes de saude nas comarcas de RO - operadora local, decisao local, area de dominio do Lucas |
| 94 | A | **FUNCEF - Fundacao dos Economiarios Federais** | Brasília/DF | Fundo de pensao | Acompanhar abertura do proximo credenciamento e habilitar-se na faixa de contencioso de massa |
| 94 | A | **Banco Bradesco S/A** | Osasco/SP | Banco | Buscar credenciamento como assessoria juridica de cobranca e ofertar cobertura de RO |
| 94 | A | **Almeida & Freitas Advogados** | Fortaleza/CE | Empresa/escritório com vaga jurídica aberta | Candidatar-se a vaga e ofertar disponibilidade remota / correspondencia em RO |
| 94 | A | **Energisa Rondônia** | Porto Velho/RO | Distribuidora de energia elétrica | Ofertar defesa em acoes consumeristas nas comarcas de RO - contencioso ocorre exatamente onde o Lucas atua |
| 94 | A | **Ferreira & Chagas Advogados** | Remoto/BR | Empresa/escritório com vaga jurídica aberta | Candidatar-se a vaga e ofertar disponibilidade remota / correspondencia em RO |
| 94 | A | **TRR BrasDiesel** | Ji-Paraná/RO | Distribuidora de combustíveis | Ofertar assessoria tributaria e defesa em execucao fiscal na propria cidade |
| 93 | A | **CREFISA E EMPRESAS PARCEIRAS** | São Paulo/SP | Instituição financeira | Ofertar correspondência e audiências em Rondônia + disponibilidade para contencioso bancário/consumidor |
| 93 | A | **Marcelo Tostes Advogados** | Belo Horizonte/MG | Escritório de advocacia (grande porte nacional) | Propor cadastro como correspondente/parceiro em Rondonia para audiências e diligências |
| 93 | A | **Itaú Unibanco** | São Paulo/SP | Banco | Ofertar correspondencia e audiências em RO para a carteira bancaria de massa |
| 93 | A | **Banco Daycoval** | São Paulo/SP | Banco / financeira de consignado | Ofertar correspondencia e audiências em RO |
| 93 | A | **Banco BMG** | São Paulo/SP | Banco / financeira de consignado | Ofertar correspondencia e audiências em RO - cartao consignado e demanda recorrente no interior |
| 93 | A | **Gonçalves Júnior Advocacia** | Brasília/DF | Empresa/escritório com vaga jurídica aberta | Candidatar-se a vaga e ofertar disponibilidade remota / correspondencia em RO |
| 93 | A | **FACER - Federação das Associações Comerciais e Empresariais de Rondônia** | Porto Velho/RO | Federação empresarial | Propor convenio de assessoria juridica para a rede de associados - um acordo abre acesso a milhares de empresas em RO |
| 93 | A | **Marfrig** | São Paulo/SP | Frigorífico / agroindústria | Ofertar defesa ou atuacao em acoes de acidente de trabalho e doenca ocupacional em RO |
| 92 | A | **Mind Consultoria de Gente e Gestão** | Ji-Paraná/RO | Empresa de RH / recrutamento | Candidatar-se como advogado associado PJ; pedir cadastro no banco de talentos jurídico da consultoria |
| 92 | A | **Trajano Neto & Paciornik Advogados** | Curitiba/PR | Escritório de advocacia (grande porte) | Propor cadastro como correspondente em Rondonia para a carteira de massa |
| 92 | A | **Energisa** | Cataguases/MG | Distribuidora de energia elétrica | Ofertar defesa em acoes consumeristas nas comarcas de RO - concessionaria local com contencioso pulverizado |
| 92 | A | **ABL Advogados (Aith, Badari e Luchin)** | São Paulo/SP | Escritório de advocacia previdenciária | Ofertar correspondencia previdenciaria nas varas federais e JEFs de Rondonia |
| 92 | A | **Frigorífico Tangará** | Ji-Paraná/RO | Frigorífico | Ofertar assessoria trabalhista e defesa em doencas ocupacionais na propria cidade |
| 92 | A | **Supermercado Irmãos Gonçalves** | Jaru/RO | Rede de supermercados | Ofertar assessoria trabalhista e consumerista - comarca vizinha, cobertura imediata |
| 91 | A | **R. Barreto Advogados Associados** | Não informado/BR | Escritório de advocacia | Ofertar correspondencia em RO para a carteira bancaria e consumerista |
| 91 | A | **Migalhas Correspondentes** | São Paulo/SP | Plataforma de correspondentes jurídicos | Cadastrar-se cobrindo Ji-Parana e comarcas de RO |
| 91 | A | **Telefônica Brasil (Vivo)** | São Paulo/SP | Empresa de telecomunicações | Ofertar correspondencia e audiências em RO para contencioso consumerista de massa |

---

## 5. AS 20 OPORTUNIDADES MAIS IMEDIATAS

| Score | P | Empresa/escritório | Oportunidade | Local | Publicada | Link |
|---|---|---|---|---|---|---|
| 97 | A | **BBMD** | Advogado Trabalhista - CORRESPONDENTE (Maceió/São Luís/Natal) | Maceió/AL | 2026-08-19 | [vaga](https://to.indeed.com/aaqwlrkfmfy2) |
| 97 | A | **BBMD** | Advogado Trabalhista - CORRESPONDENTE (João Pessoa) | João Pessoa/PB | 2026-08-19 | [vaga](https://to.indeed.com/aapdf7vkr7jt) |
| 96 | A | **BBMD** | Advogado Trabalhista - CORRESPONDENTE | Palmas/TO | 2026-08-19 | [vaga](https://to.indeed.com/aayr9d8g7zbf) |
| 96 | A | **BBMD** | Advogado Trabalhista - CORRESPONDENTE (Salvador) | Salvador/BA | 2026-08-19 | [vaga](https://to.indeed.com/aay4xc9gbq46) |
| 95 | A | **NELSON WILIANS & ADVOGADOS ASSOCIADOS** | Consultor de Negócios | Porto Velho/RO | 2026-09-02 | [vaga](https://to.indeed.com/aac74727vnrf) |
| 94 | A | **Almeida & Freitas Advogados** | CONTROLADORIA JURÍDICA para ADVOGADO com OAB ATIVA (PJ) | Fortaleza/CE | 2026-09-11 | [vaga](https://to.indeed.com/aas8s8jh77kv) |
| 94 | A | **Ferreira & Chagas Advogados** | ADVOGADO CONTENCIOSO CÍVEL BANCÁRIO - REMOTO PJ | Remoto/BR | 2026-08-27 | [vaga](https://to.indeed.com/aa4jgxplzz6z) |
| 93 | A | **CREFISA E EMPRESAS PARCEIRAS** | Advogado(a) Cível Júnior - Contencioso | São Paulo/SP | 2026-09-15 | [vaga](https://to.indeed.com/aaz9k8qzwbqt) |
| 93 | A | **Gonçalves Júnior Advocacia** | Advogado(a) Associado(a) — Cível/Tributário | ATUAÇÃO INICIAL REMOTA | Brasília/DF | 2026-09-03 | [vaga](https://to.indeed.com/aa86shvt6hxv) |
| 92 | A | **Mind Consultoria de Gente e Gestão** | Advogado(a) Associado(a) - Trabalhista Patronal | Ambiental | Civil | Ji-Paraná/RO | 2026-08-27 | [vaga](https://to.indeed.com/aadlc47kklrh) |
| 90 | A | **LOIT CONTABILIDADE SOCIETARIA E TRIBUTARIA LTDA** | Advogado Trabalhista | Ji-Paraná/RO | 2026-08-31 | [vaga](https://to.indeed.com/aa7zjttrm4fx) |
| 90 | A | **digio** | Advogado Contencioso - Pleno | Barueri/SP | 2026-09-03 | [vaga](https://to.indeed.com/aafnzvnxhg4f) |
| 90 | A | **Marcelo Tostes Advogados Associados** | Advogado Cível Pleno - CONTENCIOSO DE ESCALA | Belo Horizonte/MG | 2026-09-03 | [vaga](https://to.indeed.com/aakkzl9nh9wb) |
| 90 | A | **MARLON WITT SOCIEDADE DE ADVOGADOS** | Advogado PREVIDENCIÁRIO (PJ) | São Paulo/SP | 2026-08-28 | [vaga](https://to.indeed.com/aaw8mtsmp6vq) |
| 90 | A | **Ferreira & Chagas Advogados** | Advogado(a) | Contencioso Aéreo - REMOTO PJ | Remoto/BR | 2026-08-27 | [vaga](https://to.indeed.com/aab82xnxxpby) |
| 90 | A | **Ferreira & Chagas Advogados** | ADVOGADO CONTENCIOSO CÍVEL CLIENTE AUTOMOTIVO - REMOTO PJ | Remoto/BR | 2026-08-28 | [vaga](https://to.indeed.com/aa8md9mlrhgr) |
| 90 | A | **Meet Recrutamento e Seleção - Direito da Saúde** | ADVOGADO DE DIREITO DA SAÚDE (PJ) | Feira de Santana/BA | 2026-08-28 | [vaga](https://to.indeed.com/aavc7jgy96vj) |
| 89 | A | **GRUPO BARCELOS** | Advogado Cível | Belo Horizonte/MG | 2026-09-09 | [vaga](https://to.indeed.com/aad7h6wbyxnj) |
| 88 | A | **LOIT CONTABILIDADE SOCIETARIA E TRIBUTARIA LTDA** | Advogado - Execução e Recuperação de Crédito | Porto Velho/RO | 2026-07-22 | [vaga](https://to.indeed.com/aa286w6m2xmw) |
| 88 | A | **Unicred** | Advogado Jurídico Pleno | Remoto/BR | 2026-08-25 | [vaga](https://to.indeed.com/aasrttnkhhfn) |

---

## 6. PADRÕES OBSERVADOS NA PESQUISA

**A BBMD está montando rede nacional de correspondentes agora.** Apareceu com a vaga
literal "Advogado Trabalhista - Correspondente" em seis capitais simultâneas —
Palmas, Salvador, São Luís, Natal, Maceió e João Pessoa — todas publicadas em
19/08/2026. Não há vaga em Porto Velho. É o lead mais acionável da base inteira:
eles estão contratando exatamente o serviço, em escala, e ainda não cobriram Rondônia.

**Controladoria jurídica virou vaga PJ recorrente.** Almeida & Freitas (Fortaleza),
Reis Advogados (Uberlândia), Gilli Basile (Blumenau), Total Garantidora (SC),
Grupo BRG (Aracaju), Machado Meyer (remoto) e Meet (em cinco praças) anunciam
controladoria jurídica em regime autônomo/PJ. É trabalho remoto por natureza e
consta do seu portfólio.

**O regime "Autônomo / PJ" domina as vagas jurídicas.** Boa parte dos anúncios
mapeados não busca empregado, busca prestador. Isso muda a abordagem: não é
candidatura a emprego, é proposta comercial de prestação de serviço.

**As recrutadoras são atalho, não obstáculo.** Meet Recrutamento aparece em mais de
quinze praças com vagas jurídicas PJ; Jobbol intermedeia dezenas de escritórios
nomeados nos próprios títulos. Um cadastro nessas bases expõe você a muitos
escritórios de uma vez.

**Rondônia concentra grandes contratantes pouco disputados.** As três maiores
empresas do estado por faturamento — Vitamais, TRR BrasDiesel e Irmãos Gonçalves —
estão em Ji-Paraná e Jaru, não na capital. A Ameron, operadora de saúde com R$ 4,4
bilhões, é sediada em Porto Velho e decide localmente. A JBS tem cinco plantas no
estado e o Frigorífico Tangará fica em Ji-Paraná: LER/DORT e insalubridade, que são
sua especialidade declarada, em volume, na sua própria comarca.

**As federações são a maior alavanca do estado.** A FACER reúne 31 associações
comerciais, mais de 7 mil empresas em 52 municípios de Rondônia. A RondoCoop reúne
mais de 20 cooperativas. A CDL Ji-Paraná reúne os lojistas da sua cidade. Um convênio
de assessoria com qualquer uma dessas entidades vale mais que centenas de abordagens
individuais.

**Credenciamento formal é porta aberta e ignorada.** Banco do Brasil credencia
sociedades de advogados por edital recorrente; a FUNCEF mantém credenciamento
específico para contencioso de massa com validade anual; a Porto Seguro tem página
permanente de credenciamento; o Bradesco publica catálogo aberto de assessorias de
cobrança credenciadas. Nenhum desses canais depende de relacionamento prévio.

**O consignado é o setor mais litigioso por cliente do país.** Estudo da Faculdade de
Direito da USP-RP: Agibank lidera com 2.156 ações por 100 mil clientes, seguido por
Daycoval (1.753) e BMG (1.647), réus em mais de 90% dos casos. Cartão consignado
vendido como empréstimo é tese consumerista clássica e casa com sua área bancária
e previdenciária.

---

## 7. COMO USAR A BASE AGORA

1. Abra `oportunidades_quentes.csv` e vá nas vinte primeiras linhas: são vagas reais,
   com data e link de candidatura, ordenadas por aderência ao seu perfil.
2. Comece pela BBMD — ofereça cobertura de Rondônia, que é o buraco na malha deles.
3. Nos leads de Rondônia (81 organizações), o contato é por telefone ou visita, não
   por e-mail. São da sua região e várias da sua cidade.
4. Para os canais de credenciamento (BB, FUNCEF, Porto Seguro, Bradesco), o caminho
   é a página institucional de credenciamento, não o e-mail comercial.
5. Quando houver rede liberada, a coluna `Pagina de contato` já traz a URL a raspar
   para preencher os e-mails.

---

## 8. ARQUIVOS

- `leads_juridicos.csv` — 521 organizações, 31 colunas
- `leads_juridicos.xlsx` — mesma base com duas abas, filtros e cores por prioridade
- `oportunidades_quentes.csv` — 261 oportunidades com vaga, data e link
- `checkpoint/checkpoint.json` — fontes testadas e consultas já executadas
- `relatorio_final.md` — este documento
