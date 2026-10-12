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
- RADAR CLIPADOR: id trig_01NZimqeU41Vg4NdWsX4dLX6, diária, 13h46 de Manaus, sessão nova, só busca web, notificação no celular. Criada em 12/10. Prompt em 07-RADAR-ROTINA.

## O que ficou do projeto antigo e o que saiu
Ficou: as contas da GAMES, o plano Pro do OpusClip, a pasta D:\Videos com os clipes feitos, o aprendizado de que Warhammer no Shorts deu view e GTA no YouTube não.
Saiu: as 3 trilhas que não se misturavam, o esforço 50% em GTA, PRÉ-VOO de 4 checagens, PÓS-VOO com scripts, hash e manifesto, PUBLICA e ENVIA, a lista de erros, o pipeline de cookies e yt-dlp, o teto de 1 post por dia, a varredura das 17h57 com 37 conectores.
