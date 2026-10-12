# 07 RADAR: a rotina automática das 13h46 (Manaus)

O que ela faz: todo dia, antes de Lucas começar às 14h, uma sessão nova do Claude varre as plataformas de campanha, ranqueia o que está aberto e entrega o bloco "RADAR DO DIA". Não gasta crédito, não posta, não entra em conta nenhuma. O resultado chega como notificação no celular e fica na lista de sessões do Claude Code.

Id: trig_01NZimqeU41Vg4NdWsX4dLX6. Cron: CRON_TZ=America/Manaus 46 13 * * *. Conectores: nenhum (só busca web e leitura de páginas). Criada em 12/10/2026; primeira execução em 13/10.

## Prompt da rotina (texto integral)

```text
RADAR CLIPADOR, rotina diária. Você roda sozinho, numa sessão nova, para Lucas, que ganha dinheiro com clipes (campanhas pagas por view e rankings de cortes no Brasil, lançamentos de jogo na Whop, cortes de streamers e página de virais). Hoje é a data do sistema. Use só busca web e leitura de páginas públicas (WebSearch e WebFetch). Não gaste crédito de nenhuma ferramenta paga, não publique nada, não envie nada, não entre em conta nenhuma, não instale nada.

Se existir o arquivo clipador/projeto/03-DINHEIRO.md no repositório, leia a seção 2 e 3 antes. Se não existir, siga só este prompt.

Varra, nesta ordem, e anote data e hora da leitura:
1. https://clipmap.gg/ (lista de campanhas ativas, filtros Stream, Esports, Games, Música, Brasil).
2. https://realoficial.com.br/pt/real-rewards e https://realoficial.com.br/pt/championships
3. https://viewx.com.br/ e https://viewx.com.br/campanhas
4. https://klypex.com.br/
5. https://appconty.com/seja-clipador
6. https://autoclipper.live/clip-and-pix
7. https://www.estourou.com/
8. https://contentrewards.com/discover (Whop; procure campanhas de games, lançamentos, streamers e música)
9. Busca web: "campeonato de cortes" e "campanha de cortes" dos últimos 7 dias; notícias de lançamento de jogo com campanha de clipes.

Para cada campanha ativa, extraia: nome; plataforma; modelo (por view ou ranking); valor por mil views ou prêmio total; participantes ou envios; R$ por participante (prêmio ÷ participantes); prazo final; redes aceitas; mínimo de views por vídeo; material permitido (acervo, live, qualquer); idioma e país do público; link do regulamento. Campo que não achou é "desconhecido", nunca inventado. Converta dólar a R$ 4,99.

Classifique:
- NÍVEL 1: por view no Brasil com Pix e verba ou prazo aberto.
- NÍVEL 2: ranking com R$ por participante acima de 20.
- NÍVEL 3: Whop ou gringa de lançamento de jogo com mais de 50% da verba restante e público brasileiro não excluído.
- NÍVEL 4: o resto. Ranking abaixo de R$ 20 por participante entra aqui com a nota "fraco".
- EXCLUÍDAS: bet, cassino, apostas, cripto sem registro, política e eleição. Liste o nome e o motivo.

Entregue o bloco "RADAR DO DIA" em português, sem travessão, resultado primeiro:
1. NOVAS DESDE ONTEM (campanhas que não apareciam ou mudaram de valor ou prazo). Se não der para comparar com ontem, diga "sem base de comparação".
2. FECHAM EM ATÉ 3 DIAS.
3. TABELA RANQUEADA por nível, com todas as colunas acima.
4. TRÊS IDEIAS DE CORTE PARA HOJE: para as 3 melhores campanhas, qual streamer, jogo ou acervo cortar, que tipo de momento procurar e por quê. Nada de link para baixar vídeo.
5. ALERTAS: regulamento que mudou, plataforma fora do ar, campanha com reclamação pública de não pagamento (cite a fonte).
6. PRÓXIMA AÇÃO QUE GERA DINHEIRO: uma frase.
Termine com a linha TETO: "Isto é o máximo possível com o que tenho" ou "Dá para ficar impecável com [X], custo [Y]". Liste as URLs lidas com hora. Se uma página bloquear a leitura, diga qual e siga com as outras.
```

## Como ajustar

- Mudar horário ou pausar: pedir no chat ("pausa o radar", "radar às 15h"). Lucas também pode fazer isso na lista de Rotinas do Claude.
- A rotina antiga "VARREDURA CLIPADOR" (trig_01LTdtdEQAcGoHgDYu3EmtM7, 17h57, 37 conectores, aprovação automática) continua pausada e pode ser apagada por Lucas.
