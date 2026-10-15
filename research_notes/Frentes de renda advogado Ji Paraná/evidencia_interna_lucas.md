# Evidência interna do próprio Lucas (coletada em 15/10/2026)

Fonte: conectores autorizados do próprio usuário (Google Drive, Gmail, Google Agenda, Claude Code Remote) e repositório git `lucaspalharesadv-lgtm/meu-projeto`. Não é pesquisa de web: é o histórico medido da operação dele. Tem precedência sobre estimativa externa quando houver conflito, porque é resultado real.

## Quem é

Lucas Alexandre Horas Palhares, advogado, OAB/RO 11.037, Ji-Paraná/RO. Mais de 5 anos de contencioso cível e administrativo (civil, consumidor, bancário, previdenciário, saúde, tributário, imobiliário). Começou na Justiça Federal e na AGU. Carteira declarada no currículo: mais de 150 processos ativos; clientes corporativos citados: Energisa e Bradesco. Atuação remota nacional. Fonte: `Lucas_Alexandre_Horas_Palhares_Curriculo_Premium.pdf`, Drive, 07/10/2026.

## Frentes já em operação e o que cada uma produziu

### 1. Prospecção jurídica por e-mail em massa (a frente mais madura)

Infraestrutura real, no branch `claude/busy-rubin-f7kvqj`: coletor em Python, enriquecimento, controle de envios, radar de respostas e follow-up, radar de vagas (Jobijoba, Gupy, Indeed), radar semanal de editais da AROM.

Listas construídas:
- `PARCERIAS_ASSOCIADO_500.csv`: 12.158 linhas
- `PROSPECCAO_JURIDICA_BRASIL.csv`: 397 linhas
- `EMAILS_PARA_CURRICULO.csv`: 110 linhas

**Resultado medido** (`prospeccao_juridica/rotina/controle_envios.csv`, 129 contatos rastreados):

| Status | Quantidade |
|---|---|
| rascunho criado (não enviado) | 76 |
| bounce (endereço inexistente) | 39 |
| respondeu: outro | 4 |
| respondeu: negativo | 4 |
| respondeu: automático | 4 |
| respondeu: cadastro | 2 |
| **respondeu: positivo** | **0** |

Leitura: dos 129 rastreados, 39 nem chegaram (taxa de bounce de 30%, altíssima: a coleta de e-mail em site de escritório produz endereço morto). Das 14 respostas humanas, **nenhuma positiva**. Nenhuma entrevista, nenhuma proposta, nenhum contrato. A frente consumiu semanas de automação e entregou zero real até 15/10/2026.

Em 15/10/2026 o Lucas enviou pessoalmente ~20 e-mails de parceria e banco de talentos (Gmail, pasta Enviados), e já voltou pelo menos 1 bounce no mesmo dia (`contato@palomaresadvocacia.com.br`). O padrão se repete.

### 2. Captação local em Ji-Paraná (rotina "Radar de Clientes")

Entradas diárias no Drive de 01/10 a 09/10/2026. Alvo: contabilidades, clínicas, imobiliárias, entidades (ACIJIP, sindicatos rurais).

Resultado medido, declarado nas próprias entradas:
- Rascunhos de parceria criados: E-Account, Premium, Ji-Paraná Contabilidade, Arrimo, KQueiroz, ACIJIP, G3, Investt, Nova Opção, City Imóveis.
- **Respostas de parceiros: nenhuma**, em todas as entradas de 01/10 a 09/10.
- Imobiliárias City, Nova Opção, Investt e G3 constam como enviadas em 07/10; sem resposta.

Gargalo identificado pela própria rotina, repetido em todas as entradas: **e-mail público é escasso em Ji-Paraná**. Contabilidades (24 listadas no Guia Fácil: ASSEC, AUDITEC, Lex, REC etc.) e imobiliárias (Calixto, Dias, Nogueira, Terra Brasil, Valentim, Jardins, A&L) publicam só telefone, WhatsApp ou formulário. A conclusão escrita pelo próprio radar: "abordagem por visita ou WhatsApp feita pelo Lucas rende mais que rascunho de e-mail".

Instagram (via Metricool, janela 09/09 a 09/10/2026): 1.604 seguidores, estável com leve queda (vinha de 1.608); alcance médio por post ~37,8; engajamento ~3,7%; **0 reels**; ~1 post no período. Melhores horários: sábado 19h-20h, dias úteis 12h-13h e 18h-20h. Há um lembrete recorrente na Agenda ("📸 Postar 1 story hoje", diário, 20h) com rotina de conteúdo detalhada, incluindo figurinha de link para o WhatsApp.

Leitura: a conta existe mas está parada. Alcance de 37 por post em cidade com concorrência de advogados não gera lead. Zero reels é o dado mais forte: o formato que distribui não está sendo usado.

### 3. Clipagem paga (a frente mais nova e mais ativa)

Painel `CLIPADOR - Painel` no Drive, criado 12/10/2026, **alterado 15/10/2026 às 14h29** (é a frente que ele está mexendo agora). Abas CORTES e CAMPANHAS.

Rotina agendada ativa: **RADAR CLIPADOR**, diária às 13h46 (America/Manaus), criada em 12/10/2026, rodou com sucesso em 15/10/2026. Varre clipmap.gg, Real Oficial, ViewX, Klypex, Conty, Autoclipper, Estourou e Whop Content Rewards, classifica campanhas em níveis 1 a 4 e exclui bet, cassino, cripto e política.

Pesquisa própria dele, em `clipador/projeto/03-DINHEIRO.md` (branch `claude/clipador-skills-guide-46w6oa`, 12/10/2026), com testes de realidade que merecem ser confirmados ou derrubados pela pesquisa externa:
- Real Oficial pagou R$ 108.321 a 6.683 clipadores desde o início: **~R$ 16 por clipador no acumulado**.
- Numa agência estrangeira, 1.300 de ~16 mil clipadores receberam algo em 9 meses (**~8%**).
- A R$ 1 por mil, R$ 100 exigem 100 mil views pagas; conta nova faz 300 a 500 views de mediana por post.
- Campanhas mapeadas em 12/10 no painel: Wild Rift / Wild Rounds 2026 (Real Oficial, R$ 1 por mil, verba R$ 15 mil, 4.233 envios), Stream Gabriel Morais (R$ 1 por mil, R$ 8 mil, 2.819 envios), Júnior e Cézar (Klypex, R$ 1 por mil, teto R$ 200 por vídeo).
- Regra de ranking que ele adotou: só entra se prêmio ÷ participantes passar de R$ 20.

Estado: **nenhum corte publicado consta no painel** (aba CORTES só com cabeçalho). Ou seja, a frente está pesquisada e zero executada.

### 4. Editais e setor público em RO

Rotina agendada ativa: **Radar semanal de editais: Diário dos Municípios de RO**, segundas 07h07 (America/Porto_Velho), com script `radar_arom.py` que varre o Diário Oficial dos Municípios de Rondônia e classifica em credenciamento aberto, contratação já feita, dativo ou falso positivo. Última execução 12/10/2026. Material em `prospeccao_juridica/materiais/DATIVOS_OAB_RO.md` e `prospeccao_juridica/vagas/EDITAIS_RO.md`.

Resultado medido: não consta nas fontes lidas nenhum edital convertido em inscrição, contrato ou receita até 15/10/2026.

### 5. Freelance jurídico já exercido

`[Instruções] QA de Autos` — Jusbrasil, compartilhado com ele em 29/06/2026, documento de instruções para **freelancers** fazerem conferência de documentos de processos contra o tribunal. É a única frente nas fontes em que ele aparece como prestador já engajado por uma empresa, não como candidato. Contatos: mariana.silva@jusbrasil.com.br, kelly.ribeiro@jusbrasil.com.br. Valor por tarefa: desconhecido nas fontes internas.

### 6. Outras frentes presentes nas fontes

- Candidaturas a vagas: planilha `E-mails para enviar` (07/10 a 13/10/2026) com vagas de LinkedIn (Fett Advogados, DSMA Zulay, BMM), e dossiê completo de um escritório alvo (`m3bs/`, branch `claude/sweet-meitner-7gbxm3`, 13/10/2026) com vagas abertas, pessoas e cultura: preparação séria para candidatura dirigida.
- Robô de Instagram (`claude/eloquent-volta-n5pq3h`, 01/10/2026): projeto Python com compliance, geração, render, voz e vídeo, com playbook diário e catálogo de canais. Construído, resultado não medido nas fontes.
- Literatura: `Glavenir - O núcleo.docx` (01/10/2026), romance de ~31 MB. Frente de renda apenas potencial, não explorada.

## Infraestrutura e limitações observadas nesta sessão

- Conectores ativos e úteis: Gmail, Google Drive, Google Agenda, Google Sheets, AdvPlan, GitHub, Metricool, Tavily (no limite de 432 nas rotinas recentes), busca web.
- **AdvPlan está vazio**: nenhum cliente e nenhum caso cadastrado; processos da OAB em importação. Qualquer frente que dependa dele está travada.
- Mais de 100 servidores MCP falharam ao conectar nesta sessão (403 no proxy): Canva, Adobe, Airtable, Figma, Common Room, bio-research, entre outros. Datadog pede OAuth.
- Rondônia usa America/Porto_Velho (UTC-4). As rotinas dele estão espalhadas entre America/Manaus, America/Porto_Velho e America/Sao_Paulo, o que desloca horários.

## O que esta evidência impõe ao relatório

1. O problema do Lucas **não é falta de frente**. São pelo menos 6 frentes abertas simultaneamente, com automação construída em 5 delas.
2. O problema é **conversão zero**: 0 resposta positiva em 129 contatos rastreados de prospecção, 0 resposta de parceiro local em 9 dias de radar, 0 corte publicado no painel de clipagem, 0 edital convertido.
3. O padrão comum a todas as falhas é o mesmo: **a etapa automatizada (pesquisar, coletar, redigir rascunho) é executada; a etapa humana e irredutível (enviar, visitar, ligar, publicar o vídeo) não é**. 76 rascunhos criados e não enviados é o retrato disso.
4. Portanto, qualquer ranqueamento de frentes precisa pesar não só "quanto paga" e "quanto demora", mas **quanto trabalho humano não delegável a frente exige por real ganho**, porque é exatamente aí que a operação dele para hoje.
