# CLIPADOR: conhecimento do projeto (12/10/2026)

Arquivo único com as seções 02 a 07. As instruções do projeto citam cada seção pelo número.

---

# 02 PAINEL: referência fixa do projeto (12/10/2026)

Este arquivo não muda sozinho. O estado vivo (cortes, campanhas, semanas, fontes) está na planilha. Quando algo aqui ficar velho, Lucas pede "atualiza o PAINEL" e cola a versão nova no projeto.

## Planilha (o estado do projeto)
- CLIPADOR - Painel: https://docs.google.com/spreadsheets/d/1dXEjjHTLzzPUVy9Sg5Pw-CZZ3sh_mkVSSojsXPfuDrk/edit
- Abas: CORTES, CAMPANHAS (já carregada com as campanhas abertas em 12/10), SEMANA, FONTES, LEIA-ME.
- O Claude lê e grava pelo conector do Google Sheets.

## Contas
| Marca | Rede | Conta | Estado em 12/10 |
|---|---|---|---|
| GAMES | TikTok | @zackairgames | Existe. Conta pessoal. 7 posts, melhor: 330 views |
| GAMES | YouTube | @zackfair1564 | Existe. 7 Shorts, melhores: 1.350 e 1.123 views (Warhammer). Um DEMO do OpusClip foi publicado por engano com restrição de 18 anos: deixar privado |
| GAMES | Instagram | não existe | Criar só se uma campanha exigir |
| VIRAIS | TikTok e YouTube | a criar | Nicho: fails, sustos e momentos engraçados. Bio: "fails e sustos que o Brasil ainda não viu" |
| Whop | zackfairplay | Existe | Campanha Dark Heresy registrada em 10/10. A afirmação do projeto antigo de que o Chrome estava noutra conta (@lunartongue) estava errada |

## Ferramentas (lido em 11 e 12/10)
| Ferramenta | Plano | Estado | Uso no projeto |
|---|---|---|---|
| OpusClip | Pro, 370 min de processamento | Nenhuma conta social conectada, nenhum template | Motor principal. Lucas conecta TikTok e YouTube da GAMES e cria o template "GAMES" na interface |
| vidIQ | Free, 2 de 150 créditos, renova 01/11 | Ligado ao Gmail do escritório, sem o canal da operação | Parado até 01/11 |
| Metricool | Free | Ligado à marca do escritório | Não usar |
| Tavily | Free | Limite do plano atingido em 11/10 | O radar usa busca web, não Tavily |
| Google Sheets e Drive | | Conectados | Planilha e prints de prova |
| Claude | Max 20 | | Chat para o dia a dia; Claude Code só para trabalho pesado (triagem de live com API da Twitch), quando o PC estiver bom |
| PC | fraco (processador a trocar) | | Nada de gameplay própria nem render local por enquanto |

## Decisões de 12/10 (respostas de Lucas)
1. Dinheiro vem de campanha brasileira por view e Pix; o resto é complemento.
2. Qualquer campanha que pague entra. Fora: bet, cassino, política.
3. GTA VI parado até existir campanha paga.
4. 30 h ou mais por semana.
5. Duas marcas: GAMES e VIRAIS. As contas atuais viram a GAMES.
6. Redes: TikTok e YouTube Shorts. Instagram só se a campanha exigir. Kwai fora.
7. Português nas campanhas brasileiras, inglês só em campanha gringa.
8. OpusClip é o motor. R$ 0 em ferramentas novas. Até 60 min de OpusClip por dia sem perguntar (meta 20).
9. 4 a 6 posts por dia por marca. Lucas posta pelo app com a FILA pronta.
10. Checklist curto de 5 itens. Sem hash, manifesto, PUBLICA ou ENVIA. Scripts de QA do projeto antigo descartados: Lucas assiste o corte de 30 s antes de postar.
11. Radar automático às 13h46 (Manaus).
12. Virais: fails, sustos e engraçados. Gameplay própria só depois do PC novo.
13. Tudo roda no Projeto do Claude Chat.

## Configuração guiada (o Claude conduz, um passo por vez, na ordem)
1. Whop (whop.com, conta zackfairplay): abrir "suas campanhas" e ver se a Warhammer Dark Heresy ainda aparece. Se sim, abrir as regras, colar o texto no chat e inscrever os 2 Shorts ("Dark Heresy looks INSANE", 1.350 views, 10/10; "Dark Heresy has co-op for 1-4 players", 1.123 views, 11/10). Se exigir #ad ou #publi, editar a descrição antes. Se a campanha fechou, segue.
2. Real Oficial (realoficial.com.br/pt/real-rewards): criar conta, vincular TikTok @zackairgames e YouTube @zackfair1564, entrar em Wild Rift e Stream Gabriel Morais, colar os dois regulamentos no chat.
3. Viewx (viewx.com.br): criar conta, vincular as mesmas contas, entrar no ranking João Pichau, colar o regulamento.
4. Klypex (klypex.com.br), Conty (appconty.com/seja-clipador) e Estourou (estourou.com): criar conta e vincular. Só olhar as campanhas; não entrar ainda.
5. OpusClip (opus.pro), no computador: Configurações > Contas sociais > conectar TikTok @zackairgames e YouTube @zackfair1564.
6. OpusClip: Brand templates > novo template "GAMES": 9:16, layout Gameplay, legenda em caixa alta, 2 a 4 palavras por linha, destaque amarelo, sem gancho automático, sem emoji. Depois o Claude confere com opusclip_list_brand_templates.
7. YouTube Studio da @zackfair1564: deixar privado o Short "A tense exchange..." (DEMO publicado por engano, restrito a 18 anos).
8. Marca VIRAIS, no celular: criar TikTok pessoal novo e canal do YouTube novo (Conta Google separada, verificação em 2 etapas). Bio: "fails e sustos que o Brasil ainda não viu". Mandar os @ no chat; o Claude grava na aba LEIA-ME.
9. Rotinas do Claude: apagar a rotina antiga VARREDURA CLIPADOR (17h57). A nova, RADAR CLIPADOR (13h46), fica.
10. Primeiro CLIPAR: com o regulamento do Wild Rift, o Claude pede o link do acervo ou da VOD e os minutos dos momentos, e entrega os 3 primeiros clipes e a FILA.

## Rotina automática
- RADAR CLIPADOR: id trig_01NZimqeU41Vg4NdWsX4dLX6, diária, 13h46 de Manaus, sessão nova, só busca web, notificação no celular. Criada em 12/10. Prompt na seção 07 RADAR.

## O que ficou do projeto antigo e o que saiu
Ficou: as contas da GAMES, o plano Pro do OpusClip, a pasta D:\Videos com os clipes feitos, o aprendizado de que Warhammer no Shorts deu view e GTA no YouTube não.
Saiu: as 3 trilhas que não se misturavam, o esforço 50% em GTA, PRÉ-VOO de 4 checagens, PÓS-VOO com scripts, hash e manifesto, PUBLICA e ENVIA, a lista de erros, o pipeline de cookies e yt-dlp, o teto de 1 post por dia, a varredura das 17h57 com 37 conectores.

---

# 03 DINHEIRO: de onde vem e o que faz perder (12/10/2026)

Câmbio usado: R$ 4,99 por US$ 1. Cartão internacional soma 3,5% de IOF. Valores mudam toda semana: o radar das 13h46 atualiza, e Lucas confirma no painel de cada campanha antes de cortar.

## 1. Fontes de renda, da melhor para a pior para quem está começando

| # | Fonte | Quanto paga | Aceita conta nova? | 1º real em | Veredito |
|---|---|---|---|---|---|
| 1 | Campanha brasileira por view (Real Oficial, Klypex, Viewx, Conty, Autoclipper, Estourou) | R$ 0,50 a 2,50 por mil views, Pix | Sim. Nenhuma publica mínimo de seguidores. Conta recente com número alto passa por auditoria | Dias a 60 dias, conforme o regulamento | Motor do mês 1 |
| 2 | Ranking (campeonato de cortes) com pouca concorrência | Prêmio fixo aos primeiros. Vale se prêmio ÷ participantes passar de R$ 20 | Sim | Fim da campanha + apuração | Bônus, 1 por vez |
| 3 | Whop Content Rewards, lançamento de jogo | US$ 1 a 1,75 por mil (R$ 5 a 8,73). Verba acaba em dias. Vídeo abaixo do mínimo (2.000 a 4.700 views) vale zero. País do público pode não contar | Na maioria, sim | Cai na hora depois da aprovação; saque em dólar | Extra, só nas primeiras 48 h de cada lançamento |
| 4 | Clipador oficial de streamer | Gringa: R$ 2 a 2,50 por mil ou fixo de US$ 200 a 2.000 por mês. Brasil: sem dado público; referência de editor CLT R$ 2.186 a 5.299 por mês | Precisa de 2 a 4 semanas de cortes publicados como prova | 1 a 3 meses | Maior potencial do mês 3 em diante |
| 5 | Publi na página de virais | R$ 572 a 858 por post com 28 mil seguidores (referência usepora); gringa US$ 50 a 150 entre 10 e 50 mil seguidores | Não. Precisa de ~10 mil seguidores | 2 a 6 meses | Do mês 3 em diante |
| 6 | Prêmios da Garena (Free Fire) no TikTok | Até R$ 50 mil e R$ 150 mil por evento, "proporcional ao desempenho" | Exige gameplay própria | Por evento | Só depois de trocar o PC |
| 7 | Monetização nativa | TikTok Creator Rewards: R$ 0,50 a 1,60 por mil, só vídeo original com 1 min ou mais, 10 mil seguidores e 100 mil views em 30 dias. Shorts no Brasil: ≈ R$ 0,22 por mil, e a partir de 01/02/2027 exige 10 mi de views em 90 dias | Não | 3 a 6 meses | Corte de terceiro não paga aqui |

Testes de realidade, para não se iludir:
- Real Oficial pagou R$ 108.321 a 6.683 clipadores desde o início: ~R$ 16 por clipador no acumulado.
- Numa agência gringa, 1.300 de ~16 mil clipadores receberam algo em 9 meses (~8%).
- A R$ 1 por mil, R$ 100 exigem 100 mil views pagas. Conta nova faz 300 a 500 views de mediana por post. O que muda o jogo é o outlier: 1 corte em 20 ou 30 passa de 50 mil.
- Quem ganha de verdade posta volume, em várias campanhas, com conta aquecida, e vira clipador oficial de alguém.

## 2. Plataformas brasileiras (todas com Pix)

| Plataforma | Como paga | Taxas e saque | Observação |
|---|---|---|---|
| Real Oficial, realoficial.com.br/pt/real-rewards | Por view (R$ 0,50 a 1 por mil) e rankings | Pix depois da validação. Blog fala em 30 a 60 dias após o fim; regulamento do Yuri22 fala em 7 dias após a apuração | Programa oficial do Podpah. Posts precisam ficar públicos. Só contam views depois da inscrição |
| Viewx, viewx.com.br | Rankings (R$ 2,5 mil a 40 mil) e por view (Gustavo Borges, R$ 1 por mil) | Pix | Sem audiência mínima. Termos completos só com login |
| Klypex, klypex.com.br | Por view (Júnior e Cézar: R$ 1 por mil, teto R$ 200 por vídeo) e rankings diários | Grátis, sem convite, Pix | TikTok, Reels, Shorts, Facebook, X |
| Conty, appconty.com/seja-clipador | Por campanha | 5% no saque, sem mensalidade | Contas precisam estar autorizadas na campanha |
| Autoclipper Clip & Pix, autoclipper.live/clip-and-pix | R$ 1 a 2,50 por mil | Grátis, Pix | Empurra o uso da ferramenta Autoclipper; não é obrigatório |
| Estourou, estourou.com | Campanhas de música: taxa por campanha, só com login | Saque do dia 1 ao 3 de cada mês, Pix em até 3 dias úteis | Vídeo viral com a música da campanha de fundo rende views e R$ por mil. Revisa crescimento anormal antes de liberar |
| Cut.pro campeonatos | Exemplo R$ 1,50 por mil; vídeo com menos de 1.000 views vale zero | Pix, 1 saque a cada 7 dias | |
| Clipou | Por campanha | 12% no saque no plano grátis | Caro. Só se a campanha for muito boa |
| Radar: clipmap.gg e contentrewards.com/discover | Lista as campanhas ativas e o orçamento restante | | O radar diário usa os dois |

Entrada sem cobrança confirmada por escrito: Klypex, Conty, Autoclipper. Real Oficial e Viewx não cobram nada visível, mas leia o regulamento. Se qualquer uma pedir pagamento para entrar, é golpe.

## 3. Conta de ranking: entrar ou não

R$ por participante = prêmio total ÷ participantes (ou envios, se for o único número). Regra: entra só acima de R$ 20. Exemplos de 12/10: Pichau R$ 69, Kosky V2 R$ 58, LOUD Miller R$ 31, LOUD Facada R$ 26 (entram); LOUD VTzim R$ 8, Yuri22 R$ 8,63, LOUD Coringa R$ 2,80 (não entram). Em ranking, o 1º lugar leva a maior parte: só vale com 1 corte por dia do streamer e um ângulo diferente dos outros.

## 4. Whop e campanhas gringas

- contentrewards.com/discover lista as campanhas com verba restante. Entre só com mais de 50% da verba e nas primeiras 48 h.
- Cada campanha tem mínimo por vídeo: a US$ 1,75 por mil com mínimo de US$ 3,50, o corte precisa de 2.000 views para valer algo.
- País e público aceitos ficam num documento da campanha. Views do Brasil podem não contar. Ler antes de postar.
- Divulgação: os termos da Whop exigem identificar a parceria (#ad; no Brasil, #publi).
- Pagamento em Whop Credits, saque depois do KYC. Não há Pix. PayPal custa perto de 10%. Abaixo de ~US$ 50, a taxa fixa come o ganho: acumule.
- Vyro: mínimo de US$ 10, 1 saque a cada 7 dias, Brasil não citado nos termos.
- Warhammer Dark Heresy (Owlcat): campanha de wishlist que Lucas entrou em 10/10. Pendência no seção 02 PAINEL.

## 5. Clipador oficial de streamer (mês 2 em diante)

1. Escolher 1 ou 2 streamers brasileiros médios, sem equipe de cortes visível, em jogo que está em alta (LoL, Valorant, GTA RP, Tibia, terror, indie). Gaules, Casimiro e alanzoka não servem: já têm equipe.
2. Cortar as lives deles por 2 a 4 semanas numa conta sua, com o @ e o link da VOD.
3. No Discord do streamer, procurar canais #clips, #clip-program, #clippers, #clip-submissions.
4. Mandar DM ou e-mail com os 3 melhores cortes, as views de cada um e 3 momentos da última live que você cortaria.
5. Propor teste pago de 2 semanas; depois, fixo mensal. Combinar fonte do material, redes, valor, tag ou marca d'água.
6. Nunca pagar por "vaga de clipador". DM sem amostra converte perto de zero.

## 6. Página de virais (marca VIRAIS)

- Repost seco perde alcance em todas as redes. Toda peça precisa de uma camada sua: narração com roteiro seu, legenda-piada em template, top 5 com comentário, ou react. Borda, marca d'água, velocidade e crédito não contam.
- Rende dinheiro assim: música de campanha (Estourou) no fundo quando o viral não depende do áudio; Whop com campanhas de música e marca; publi quando passar de ~10 mil seguidores; TikTok Creator Rewards só em conta de originais com vídeo de 1 min ou mais.
- Nunca usar vídeo de ViralHog, Jukin (FailArmy), Newsflare, Storyful ou Collab: eles registram a impressão digital e reivindicam ou derrubam. Sinais: marca d'água dessas empresas, "licensing@" ou "for licensing" na descrição.
- Pedir permissão ao autor por DM ("Posso postar seu vídeo na @pagina com crédito? Vou adicionar narração.") e guardar o print do sim.
- Nunca comprar nem vender página: os termos do Instagram proíbem e o vendedor pode retomar a conta.

## 7. O que faz perder dinheiro ou conta

Campanha (views recusadas):
- Inscrever o vídeo depois de postar: só contam as views ganhas depois da inscrição. Inscrever no mesmo minuto.
- Retocar corte de outro clipador (aparar, espelhar, filtro, trocar trilha): recusa, saque bloqueado, banimento.
- Abaixo do mínimo por vídeo: vale zero.
- Verba esgotada: a Whop paga por ordem de chegada.
- Sem a tag, o @ ou a hashtag da campanha: não conta.
- Várias contas na mesma campanha, VPN, conta comprada, view comprada: desclassificação na primeira auditoria.
- Apagar e repostar, deixar privado ou arquivar durante a apuração: perde as views.
- Auditoria: conta recente com número alto é indício de fraude. Guardar prints de 24 h, 72 h e 7 dias de cada post. A plataforma pode pedir chamada de vídeo mostrando a analytics.

Conta:
- Música da live ou do jogo (rádio do GTA, Spotify do streamer): claim. Short com mais de 1 min e claim ativo é bloqueado no mundo todo. Cortar o trecho ou abaixar a música.
- 3 strikes em 90 dias encerram o canal do YouTube e afetam os canais vinculados. O TikTok remove quem reincide.
- Imagem oficial de esports (CBLOL, VCT) em trecho longo: cortar a reação do streamer, não a partida.
- Corte de live alheia sem camada própria: sai do Para Você e não monetiza no YouTube. Para campanha paga isso não importa; para conta própria, importa.
- Bet, cassino e política: maior taxa de banimento, e ban durante a verificação perde o saldo pendente.

Golpes: cobrança para entrar, promessa de ganho fixo, regras escondidas, pedido de senha, código 2FA ou QR code no Discord, "curso de método", "vaga paga de clipador", falso funcionário com avatar copiado. Nenhuma plataforma séria pede nada disso.

## 8. Receber

- Brasil: Pix. Guardar comprovante na planilha (aba SEMANA).
- Dólar: preencher o W-8BEN no KYC da Whop. Comparar PayPal (~10%) com Wise. Acumular antes de sacar.
- Imposto: renda de plataforma brasileira entra na declaração anual; renda do exterior vai no carnê-leão. Levar ao contador junto com a outra renda.

---

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

---

# 05 FERRAMENTAS: como o Claude opera cada uma (12/10/2026)

## 1. OpusClip pelo conector (plano Pro, saldo lido em 12/10: 370 min)

1 crédito = 1 minuto de vídeo importado. O que gasta crédito é o submit_project. Leituras (list, preview, describe, get_usage) são grátis. Por isso: nunca mandar a live inteira. Mandar só a janela em volta do momento.

Passo a passo do CLIPAR:
1. `opusclip_get_usage` no começo do dia. Se o saldo for menor que o dia precisa, avisar.
2. `opusclip_submit_project` com:
   - `videoUrl`: link público. Aceita YouTube, Twitch (VOD e clipe), Google Drive (arquivo compartilhado "qualquer pessoa com o link"), Vimeo, X, Facebook, Dropbox ou MP4 público. Vídeo do YouTube com restrição de idade pode falhar: usar o arquivo no Drive.
   - `rangeStart` e `rangeEnd` em segundos: a janela de 2 a 4 min em volta de cada momento. Esse é o controle de custo.
   - `aspectRatio`: "portrait".
   - `clipDurationsSec`: [[15,35]] para campanha por view; [[20,60]] para RP e terror; [[60,90]] só para conta de originais.
   - `customPrompt`: o que procurar, em português. Exemplos: "reações fortes do streamer: susto, raiva, risada, treta com o chat. Ignorar menu, loading e silêncio." Para viral sem fala, usar `model: "ClipAnything"` e `topicKeywords` como ["queda", "susto", "reação"].
   - `enableCaption: true`. `enableAutoHook: false` (o gancho é escrito pela rubrica, não pelo padrão da ferramenta). `sourceLang: "pt"` para streamer brasileiro.
   - `brandTemplateId` quando o template "GAMES" existir (criar na interface do OpusClip: layout Gameplay, legenda grossa 2 a 4 palavras, cor de destaque). Até lá, sem template.
   - Arquivo local (acervo de campanha baixado): `opusclip_create_upload_link` dá um link de upload; Lucas sobe o arquivo; o `upload_id` entra como `videoUrl`. Mais simples: subir no Drive e mandar o link.
3. Esperar o processamento: `opusclip_list_clips` com o projectId até aparecerem os clipes. Depois `opusclip_preview_clips` (limit 6) para ver rank, score, duração e hashtags.
4. Aplicar a rubrica em cima do preview (título, transcrição, score, duração). Escolher 1 a 2 clipes por janela.
5. `opusclip_edit_clip`, numa chamada só, com os ops na ordem:
   - `add_text_overlay` com o gancho (até 8 palavras), `atClipSec: 0`, `durationSec: 2.5`, `position: "top"`.
   - `remove_pauses` (minPauseSec 0.6) e, se tiver muleta, `remove_filler_words`.
   - `replace_phrase` para corrigir nome de streamer ou gíria na legenda (mesmo número de palavras).
   - `set_style` com `uppercase: true`, `captionPosition: "middle"`, `highlightColor` da marca.
   - `trim_section` se o fim passar do payoff. `dryRun: true` primeiro quando houver dúvida sobre as seções.
   - `undo` desfaz a última chamada por 24 h.
6. `opusclip_export_clip` com `target: "hd"`. Se vier "rendering", chamar de novo em alguns segundos até "ready". O `export_url` é o link de download para a FILA.
7. Textos: `opusclip_create_social_copy_job` exige conta social conectada no OpusClip. Enquanto não houver, o Claude escreve título, legenda e hashtags direto (seção 04 METODO).
8. Publicação pelo OpusClip (`schedule_publish`) só depois que Lucas conectar TikTok e YouTube na interface do OpusClip. Até lá, Lucas posta pelo app. Mesmo conectado, cada post pede aprovação no app do OpusClip.

Outros usos:
- `opusclip_analyze_video` (startMs, endMs): diz onde estão rosto, pessoas e tela em cada frame da janela. Serve para conferir se a facecam entrou no enquadramento sem assistir. Grátis.
- `opusclip_create_thumbnail_job`: capa a partir do clipe.
- `opusclip_list_brand_templates`, `opusclip_list_social_accounts`: conferir o que está configurado.
- Dublagem (`dubbingLanguage`): 10 créditos por minuto. Não usar sem pedir.

Orçamento: meta de 20 min de fonte por dia (5 janelas de 4 min), teto de 60. Com 370 min, a meta dura 18 dias. O plano Pro renova 300 min por mês. Avisar o saldo no fim de cada sessão.

## 2. vidIQ pelo conector

Saldo lido em 12/10: 2 de 150 créditos, renova em 01/11. Até lá, só `vidiq_balance` (0 crédito). A partir de 01/11, orçamento de 15 créditos por semana:
- `vidiq_trending_videos` (5): Shorts em alta em português, por views por hora.
- `vidiq_instagram_tiktok_outlier_search` (5): viral gringo e se já chegou em português.
- `vidiq_video_transcript` (5): transcrição de vídeo do YouTube quando o OpusClip não for usado.
- `vidiq_watch_shortform_content` (10): análise cena a cena de 1 vídeo de concorrente. Só 1 por mês.
O canal do YouTube da operação não está autorizado no vidIQ (ele está no Gmail do escritório). Sem isso, analytics do canal vem por print do YouTube Studio.

## 3. Google Sheets e Drive pelo conector

- A planilha CLIPADOR (link em seção 02 PAINEL) é o estado. O Claude lê com `get_values` e grava com `append_values` ou `update_values`.
- Abas: CORTES (uma linha por post), CAMPANHAS (uma linha por campanha), SEMANA (fechamento de domingo), FONTES (streamers e páginas vigiadas).
- Drive: pasta "CLIPADOR" com subpastas "acervo-campanhas", "prints-de-prova" (24 h, 72 h, 7 d de cada post) e "permissoes" (prints de DM de autor de viral).

## 4. Metricool, Descript, Higgsfield, ElevenLabs

- Metricool: ligado à marca do escritório, não à operação. Não usar até Lucas criar a marca "CLIPADOR" lá (o Free aceita 1 marca; trocar de marca pode custar). Hoje não compensa: 20 posts por mês no Free.
- Descript: edição pelo texto. Pouco útil em game. Não usar.
- Higgsfield: `virality_predictor` só para desempatar 2 ganchos, e só com saldo conferido. `reframe` e `upscale_video` como resgate de fonte ruim. Custo em créditos não publicado: pedir antes.
- ElevenLabs: voz para narração de viral. O plano Free não tem licença comercial: não usar em post de campanha. Alternativa R$ 0: Google Cloud TTS (até 1 milhão de caracteres por mês) ou a própria voz do Lucas gravada no celular.

## 5. No PC do Lucas (R$ 0)

- CapCut grátis: acabamento manual, facecam, legenda, zoom, SFX. Exporta 1080p sem marca d'água se não usar item Pro.
- Página de clipes da Twitch e da Kick no navegador: a fonte dos momentos.
- SullyGnome, TwitchTracker, clipmap.gg, contentrewards.com/discover: radar.
- Depois de trocar o PC: OBS com Replay Buffer para gameplay própria (conta de originais).

## 6. O que o Claude não faz

- Não assiste vídeo nem ouve áudio. Trabalha com transcrição, preview e análise de frames do OpusClip, títulos de clipes dos viewers e números.
- Não entra em conta nenhuma. Whop, Real Oficial, Viewx, Klypex, TikTok, YouTube: Lucas abre, lê o regulamento e cola o texto.
- Não posta. Entrega a FILA.
- Não sabe se uma campanha fechou hoje. O radar mostra o estado às 13h46; Lucas confirma no painel antes de cortar.
- Não baixa vídeo com restrição de idade nem com cookies. Esse material vai pelo Drive.

---

# 06 CALENDÁRIO: rotina diária e os primeiros 30 dias (12/10 a 10/11/2026)

Horário de Manaus. Base: 30 h ou mais por semana, 6 dias, 5 h por dia. Domingo é fechamento, 1 h.

## Rotina diária (segunda a sábado)

| Hora | O quê | Quem |
|---|---|---|
| 13h46 | Radar automático roda: campanhas abertas, R$ por participante, prazos, 3 ideias de corte | Claude (rotina) |
| 14h00 a 14h30 | Lucas lê o radar, confirma no painel das campanhas o que ainda está aberto, escolhe as 2 campanhas do dia e os streamers. Cola no chat o regulamento do que for novo | Lucas |
| 14h30 a 15h00 | Momentos: Lucas abre a página de clipes dos streamers (24 h, por views), anota 8 a 10 minutos de VOD. Garimpo de 2 virais no Reddit | Lucas |
| 15h00 a 15h30 | CLIPAR: Claude aplica a rubrica, manda as janelas ao OpusClip (meta 20 min de fonte), espera o preview | Claude |
| 15h30 a 17h30 | Escolha e edição: Claude edita (gancho, legenda, pausas) e exporta 5 clipes de games e 2 de virais, com 2 versões (TikTok e Shorts) cada. Lucas assiste cada um (30 s) e aprova ou pede ajuste. Acabamento no CapCut só quando precisar | Os dois |
| 17h30 a 18h15 | FILA e postagem da leva 1: Lucas posta 4 a 6 vídeos (metade da fila) pelo app e inscreve cada link na campanha no mesmo minuto. REGISTRA na planilha | Lucas, Claude registra |
| 18h15 a 19h00 | Prints de 24 h dos posts de ontem (pasta prints-de-prova). Pedido de permissão aos autores dos virais | Lucas |
| 20h30 a 21h30 | Leva 2: o resto da fila, no horário nobre. REGISTRA | Lucas |

Total: ~5 h, sendo ~1 h de postagem e registro. Se o dia tiver só 2 h, a ordem é: postar o que está pronto > cortar campanha por view > cortar ranking > virais.

## Semana 1 (12 a 18/10): base e primeiros 60 clipes

Dia 1 (segunda, 12/10):
- Lucas: instalar o projeto (3 passos) e fazer com o Claude a configuração guiada da seção 02 PAINEL: 10 passos, um de cada vez, cerca de 1 h.
- Claude: ficha das 3 campanhas na aba CAMPANHAS. Primeira rodada de CLIPAR com o acervo.
- Meta do dia: 3 clipes publicados em 2 redes (6 posts), todos inscritos.

Dias 2 a 6 (13 a 17/10):
- 5 clipes de games por dia (Wild Rift, Gabriel Morais, Pichau) + 2 virais, cada um em TikTok e Shorts. Inscrever na hora.
- Dia 3: testar a mesma janela de 10 min no OpusClip e no CapCut manual, para decidir onde o acabamento compensa.
- Dia 4: adicionar 1 streamer médio de portfólio (1 corte por dia, com @ e link da VOD).
- Dia 5: entrar no 2º ranking (Kosky V2, R$ 58, até 31/10, ou LOUD Miller, R$ 31, até 10/11).
Metas da semana: 30 clipes de games e 10 virais (~80 posts). Mediana acima de 300 views em pelo menos 1 rede. Zero claim. R$ esperado: 0 a 30.

Domingo 18/10: FECHAMENTO 1 (abaixo).

## Semana 2 (19 a 25/10): volume e primeiro teste

- 5 a 6 clipes de games por dia. Testar 2 formatos: só a reação (15 a 25 s) contra contexto + reação com pergunta na tela (30 a 45 s).
- Entrar numa campanha de música na Estourou e empilhar a música nos virais sem áudio.
- Se uma campanha pedir Instagram, criar o Instagram da marca GAMES (profissional, criador) e começar com 1 Reel por dia.
- Calcular a razão views pagas ÷ views postadas por campanha.
Metas: 1 corte com 10 mil views ou mais. 3 cortes acima do mínimo pago. R$ 10 a 80 acumulados.

Domingo 25/10: FECHAMENTO 2.

## Semana 3 (26/10 a 01/11): calibrar

- 6 a 8 clipes de games por dia. O acumulado passa de 100.
- Cortar os 50% piores formatos e streamers pelas regras abaixo.
- Lançamento na Whop: entrar em 1 campanha de jogo com mais de 50% de verba, só na rede em que a mediana bate o mínimo por vídeo.
- Dia 01/11: vidIQ renova 150 créditos. Primeira rodada de trending e outliers (15 créditos).
- Fechamento dos rankings Pichau (01/11) e Kosky V2 (31/10): print do resultado.
Metas: os 10% melhores posts com 5 mil views ou mais. R$ 50 a 150 acumulados.

Domingo 01/11: FECHAMENTO 3.

## Semana 4 (02 a 10/11): sistema e primeiro saque

- Saques: Estourou (janela de 01 a 03/11), Real Oficial e Viewx conforme regulamento. Guardar comprovante na aba SEMANA.
- PROPOSTA ao streamer do portfólio, com os 3 melhores cortes e as views.
- Entrar em 2 campanhas novas pelo radar.
- Preparar o lançamento do GTA VI (19/11): só se o radar mostrar campanha paga de GTA.
Metas do mês: 150 a 180 clipes de games, 40 virais, 1 Pix recebido, R$ 50 a 300 no total (faixa realista: R$ 0 a 400). A R$ 1 por mil, R$ 300 exigem 300 mil views pagas.

## FECHAMENTO de domingo (30 min)

1. Claude lê a aba CORTES e calcula: views em 24 h e 7 d, mediana por conta e rede, os 5 melhores e os 5 piores, views pagas, CPM efetivo (R$ ÷ views pagas × 1.000), razão paga ÷ postada, R$ por hora.
2. O que os 5 melhores têm em comum: tipo de momento, streamer, duração, horário.
3. Decisões pelas regras abaixo. Uma mudança de cada vez.
4. Grava na aba SEMANA. Define 1 teste A/B para a semana.

## Regras de decisão (limiares para calibrar com os seus dados)

- Dobrar: streamer, jogo ou formato com 10 cortes ou mais, mediana 2 vezes a da conta, razão paga ÷ postada de 60% ou mais e CPM efetivo de R$ 0,80 ou mais. Passa a receber metade do volume.
- Trocar de streamer ou campanha: 15 cortes com mediana abaixo de 300 views; nenhum corte acima do mínimo pago; verba restante abaixo de 20%; regra que não dá para cumprir.
- Trocar de formato: 20 cortes com os 10% melhores abaixo de 2 mil views. Mudar 1 variável por vez.
- Cortar uma rede: mediana abaixo de 30% da rede principal por 2 semanas.
- Parar e revisar: 1 strike, 1 Short bloqueado, mais de 20% dos posts com áudio silenciado, ou CPM efetivo abaixo de R$ 0,30.
- Semana 8: se a hora não render mais de R$ 5, o peso vai para a frente que pagou mais por hora (quase sempre: clipador oficial de streamer).

---

# 07 RADAR: a rotina automática das 13h46 (Manaus)

O que ela faz: todo dia, antes de Lucas começar às 14h, uma sessão nova do Claude varre as plataformas de campanha, ranqueia o que está aberto e entrega o bloco "RADAR DO DIA". Não gasta crédito, não posta, não entra em conta nenhuma. O resultado chega como notificação no celular e fica na lista de sessões do Claude Code.

Id: trig_01NZimqeU41Vg4NdWsX4dLX6. Cron: CRON_TZ=America/Manaus 46 13 * * *. Conectores: nenhum (só busca web e leitura de páginas). Criada em 12/10/2026; primeira execução em 13/10.

## Prompt da rotina (texto integral)

```text
RADAR CLIPADOR, rotina diária. Você roda sozinho, numa sessão nova, para Lucas, que ganha dinheiro com clipes (campanhas pagas por view e rankings de cortes no Brasil, lançamentos de jogo na Whop, cortes de streamers e página de virais). Hoje é a data do sistema. Use só busca web e leitura de páginas públicas (WebSearch e WebFetch). Não gaste crédito de nenhuma ferramenta paga, não publique nada, não envie nada, não entre em conta nenhuma, não instale nada.

Se existir o arquivo clipador/projeto/seção 03 DINHEIRO.md no repositório, leia a seção 2 e 3 antes. Se não existir, siga só este prompt.

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
