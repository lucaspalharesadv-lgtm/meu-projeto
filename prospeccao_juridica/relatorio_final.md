# Prospecção Jurídica B2B — RELATÓRIO DE STATUS (18/09/2026)

## STATUS: BLOQUEADO PARA COLETA DE E-MAILS

### O bloqueio, em uma frase
O ambiente desta sessão (Claude Code na nuvem) tem a saída de rede restrita por
política da organização: **nenhum site externo pode ser aberto**. Sem abrir a página,
não há como ler um e-mail publicado nela — e a regra nº 1 do trabalho é não inventar e-mail.

### Testes realizados (todos negados pelo proxy de egresso)
| Alvo | Ferramenta | Resultado |
|---|---|---|
| correspondentedinamico.com.br | WebFetch | EGRESS_BLOCKED |
| advogadosecorrespondentes.com.br | WebFetch | EGRESS_BLOCKED |
| brasilcorrespondentes.com.br | WebFetch | EGRESS_BLOCKED |
| meucorrespondentejuridico.com.br | WebFetch | EGRESS_BLOCKED |
| juriscorrespondente.com.br | WebFetch | EGRESS_BLOCKED |
| correspondentesnaweb.com.br | WebFetch | EGRESS_BLOCKED |
| oab-ro.org.br | WebFetch | EGRESS_BLOCKED |
| juridicocerto.com | WebFetch | EGRESS_BLOCKED |
| gov.br | WebFetch | EGRESS_BLOCKED |
| wikipedia.org | WebFetch | EGRESS_BLOCKED |
| linkedin.com | WebFetch | EGRESS_BLOCKED |
| oab.org.br | curl (crawler próprio) | CONNECT tunnel failed 403 |

O proxy libera apenas registries de pacote (pypi, npm) e a API da Anthropic.

### O que AINDA funciona (roda fora do contêiner)
- **WebSearch** — devolve nomes de organizações e URLs reais, mas **não o conteúdo das páginas**, logo não devolve e-mails.
- **Indeed MCP** — devolve vagas reais, datadas, com empresa, cidade e link de candidatura. Sem e-mails.

## O QUE JÁ FOI ENTREGUE (dados reais, nenhum inventado)
- `leads_juridicos.csv` — 25 organizações únicas (11 Prioridade A, 13 B, 1 C), 3 em Rondônia.
- `oportunidades_quentes.csv` — 30 oportunidades reais com vaga, data de publicação e link de candidatura.
- Campos de e-mail **vazios**, com a coluna `STATUS DO CONTATO` explicando o motivo.

Destaques em Rondônia:
1. **LOIT Contabilidade** — vaga de Advogado Trabalhista em **Ji-Paraná** (31/08/2026) e de Advogado de Execução/Recuperação de Crédito em Porto Velho (22/07/2026).
2. **Mind Consultoria** — vaga de **Advogado Associado PJ** em Ji-Paraná (27/08/2026), mais 4 vagas jurídicas na mesma cidade.
3. **Nelson Wilians & Advogados** — banca de atuação nacional com operação em Porto Velho; perfil clássico de contencioso de massa com rede de correspondentes.

## COMO DESBLOQUEAR A COLETA DE E-MAILS
1. **Autorizar o conector Tavily** (nas configurações de conectores do claude.ai). O Tavily busca e **extrai o conteúdo das páginas** pelo servidor dele, fora deste contêiner — é o caminho mais rápido e resolve o problema por inteiro.
2. **Rodar a pesquisa no Claude Code local** (app de desktop / terminal na sua máquina), onde a rede não é restrita.
3. **Liberar o egresso do ambiente** nas configurações do Claude Code na web.

Com qualquer um dos três, a base de 800 com e-mails verificados é executável.
