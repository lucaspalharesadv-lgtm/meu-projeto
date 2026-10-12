# 04 MÉTODO: o que clipar, como escolher o momento e como editar

## 1. Marca GAMES: quem clipar

Ordem:
1. O streamer ou jogo de uma campanha aberta. Fonte e pagamento já resolvidos.
2. Um streamer brasileiro médio sem equipe de cortes, em jogo em alta no Brasil (LoL, Valorant, GTA RP, Tibia, terror, indie). Serve de portfólio para virar clipador oficial.
3. Lançamento de jogo com campanha na Whop, nas primeiras 48 h.

Nunca começar por Gaules, Casimiro ou alanzoka: canal oficial de cortes forte e centenas de clipadores.

Radar de streamer (30 min por semana, Lucas no navegador):
- SullyGnome (sullygnome.com, filtro Portuguese (Brazil), 30 dias, abas Trending e Most watched) e TwitchTracker (ranking português). Para a Kick, a página kick.com/categoria com idioma pt.
- Para cada candidato: busca "[nome] cortes" no YouTube (filtro "esta semana") e no TikTok. Contar contas ativas nos últimos 7 dias e a mediana de views delas.
- Verde: 2 a 8 contas de corte ativas, mediana acima de 5 mil views, e a página de clipes do canal somando 50 mil views na semana. Amarelo: mais de 8 contas (entrar só com ângulo novo: só sustos, só fails, só treta). Vermelho: clipes somando menos de 10 mil views.
- Se o streamer tem campanha ativa, ele passa na frente.

## 2. Como achar o momento (sem assistir a live inteira)

Sinais, do mais forte para o mais fraco:
1. Clipes criados pelos próprios viewers. Na Twitch: twitch.tv/CANAL/clips, filtro "últimas 24 h" ou "7 dias", ordenado por views. Na Kick: kick.com/CANAL/clips. Vários clipes no mesmo minuto = momento que vale.
2. Pico de chat. Onde a VOD mostra o chat, procurar rajadas de "kkkk", "KEKW", "CLIP", "NÃO", "MDS", "?".
3. "Mais repetidos" do YouTube (a curva cinza em cima da barra de progresso) em lives e VODs do YouTube.
4. O título que o viewer deu ao clipe: vira candidato a gancho.

Lucas anota os minutos (mm:ss) dos 5 a 10 melhores sinais e manda no CLIPAR. O Claude manda ao OpusClip só a janela de 2 a 4 min em volta de cada um (rangeStart e rangeEnd). Começar o corte 20 a 30 s antes do pico: o chat reage depois do momento.

Triagem de uma live de 6 h em 20 min:
- 0 a 5 min: Lucas abre a página de clipes do canal, ordena por views, anota os 10 melhores com minuto da VOD.
- 5 a 10 min: Claude agrupa os minutos em blocos, aplica a rubrica (abaixo) com título, views e contexto, escolhe 5.
- 10 a 20 min: submit_project com 1 range por bloco (ou 1 range largo cobrindo 2 blocos próximos), preview_clips, escolha final.

## 3. Rubrica de 0 a 10 (clipe de game)

| Critério | Pontos | Como pontuar |
|---|---|---|
| S: sinal do público | 0 a 2 | 2 = 3 ou mais clipes de viewers no mesmo minuto, ou top 3 de views da live. 1 = 2 clipes ou top 10. 0 = nenhum |
| G: gancho de 0 a 2 s sem contexto | 0 a 2 | 2 = grito, susto, morte ou reação visível no 1º segundo. 1 = precisa de 3 a 5 s. 0 = precisa conhecer a história |
| P: payoff dentro do corte | 0 a 2 | 2 = até 25 s (FPS) ou 45 s (RP, terror). 1 = depois disso. 0 = sem desfecho |
| E: emoção | 0 a 2 | 2 = susto, rage, fail engraçado, treta, reação a doação, "primeira vez". 1 = clutch, ace, recorde. 0 = neutro |
| U: entende quem não joga | 0 a 1 | |
| F: frescor | 0 a 1 | Menos de 24 h e nenhuma conta de corte postou o momento com 50 mil views ou mais |
| Penalidades | | −3 música licenciada audível, cassino ou bet na tela. −3 fora do material permitido pela campanha. −2 sem facecam quando o momento depende da reação. −1 Shorts acima de 60 s |

Decisão: 7 ou mais publica. 6 fica na fila. Abaixo de 6 descarta. A base dos critérios: os clipes mais vistos da Twitch quase não têm a ver com o jogo; dominam pessoas, susto, vergonha e treta.

## 4. Rubrica de 0 a 10 (viral)

| Critério | Pontos | Como pontuar |
|---|---|---|
| V: velocidade lá fora | 0 a 2 | 2 = top 5 do dia no subreddit ou 1 mi de views em 48 h. 1 = viral médio. 0 = parado |
| A: vácuo no Brasil | 0 a 2 | 2 = nenhuma versão em português com mais de 100 mil views. 1 = só versões pequenas. 0 = já estourou aqui |
| G: gancho visual de 0 a 2 s que não depende de idioma | 0 a 2 | |
| E: emoção de alta ativação (riso, espanto, raiva) | 0 a 2 | |
| C: camada própria possível | 0 a 1 | Narração, legenda em português, contexto, top 5 |
| O: origem rastreável | 0 a 1 | Dá para creditar e pedir permissão |
| Penalidades | | −3 marca de ViralHog, Jukin, Newsflare, Storyful, Collab ou "licensing" na descrição. −3 acidente com vítima, violência explícita, menor exposto. −2 página brasileira grande já postou. −1 piada que depende de áudio em inglês |

Onde garimpar (15 min de manhã e 15 à noite, Lucas no navegador): r/Unexpected, r/nextfuckinglevel, r/funny, r/PublicFreakout (só sem vítima), r/LivestreamFail, aba /top?t=day e /rising. X e TikTok de outros países. Regra: postar em até 24 h depois de achar, e só se não chegou ao Brasil.

## 5. Ganchos em português (fórmulas para testar)

| Fórmula | Exemplo |
|---|---|
| Lacuna | "ninguém viu o que tinha atrás dele" |
| Revelação + reação | "ele revelou quanto ganhou e o chat travou" |
| Erro caro | "o erro que custou a partida inteira" |
| Pergunta + virada | "perguntaram se ele ia desistir. olha a resposta" |
| Contrário | "todo mundo achou que era bug. não era" |
| Número | "3 segundos que mudaram o campeonato" |
| Momento de virada | "o segundo em que ele percebeu" |
| Condição | "se você joga de sniper, assiste até o fim" |

Regras: até 8 palavras na tela, nos 2 primeiros segundos. Abrir no pico (grito, cara, queda) e só depois voltar ao contexto. Nunca prometer o que o corte não entrega: título enganoso vira denúncia e derruba a campanha.

## 6. Edição que retém

- Layout: rosto em cima (30%) e jogo embaixo (70%), ou 50/50. No OpusClip é o layout Gameplay. FPS rápido: tela cheia com o rosto no canto.
- Legenda: 2 a 4 palavras por bloco, fonte grossa, uma cor de destaque, na faixa entre câmera e jogo, longe do terço de baixo (botões do app). Revisar nome de streamer, gíria e palavrão: a legenda automática erra.
- Zoom de 110 a 120% no rosto na hora da reação. SFX ou meme no máximo 1 a 2 vezes, no clímax.
- Áudio: cortar ou abaixar a música da live. Volume alvo −14 LUFS.
- Fim: no payoff ou em loop. Sem "tchau", sem respiro.
- Capa: frame do pico com o texto do gancho. No Shorts, capa personalizada só em conta verificada no Studio.
- Exportar 1080x1920, H.264. Um arquivo por rede, com gancho ou início diferente. Nunca repostar o MP4 baixado de outra rede com marca d'água.

## 7. Duração por rede

| Objetivo | Duração |
|---|---|
| Campanha por view | O mínimo do regulamento; para alcance, 15 a 35 s |
| FPS | 15 a 30 s. Battle royale 20 a 40 s. MOBA 30 a 60 s. RP, Minecraft e terror 45 a 90 s (hipótese para teste A/B) |
| YouTube Shorts com material de terceiros | Até 60 s (usar 59) |
| TikTok com Creator Rewards (conta de originais, no futuro) | 1 min ou mais |
| Viral com camada própria | 10 a 30 s; top 5 narrado 65 a 90 s |

Do mesmo momento, duas versões: curta (gancho + payoff) e longa (com contexto), cada uma na rede certa.

## 8. Postar nas 2 redes

- TikTok: 3 a 5 hashtags, a da campanha primeiro. Conta pessoal (o Creator Rewards exclui conta business). Som da campanha quando o regulamento pedir.
- Shorts: título com o gancho e o nome do streamer ou jogo (até 100 caracteres), descrição com a hashtag da campanha, checagem de direitos do Studio antes de publicar.
- Frequência: contas com 11 ou mais posts por semana tiveram 34% mais views por post do que 1 por semana; a mediana quase não muda, o que sobe é o topo. Volume compra bilhete.
- Horários: sem estudo com dado do Brasil. Até ter os seus dados, testar 12h a 14h e 19h a 22h. Depois de 2 semanas, fixar 2 ou 3 horários por rede pela planilha.
- Uma conta por rede em cada campanha. "Aquecer conta" não tem base oficial: completar o perfil, usar 1 dia e começar.
