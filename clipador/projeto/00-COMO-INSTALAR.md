# 00 COMO INSTALAR o projeto CLIPADOR no Claude Chat (12/10/2026)

Tempo: 20 min. Depois disso o projeto está operando.

## Passo 1: o Projeto no Claude Chat (5 min)
1. Abra o Projeto antigo "GTA VI - CLIPADOR". Em Configurações do projeto, apague os arquivos de conhecimento antigos (REGRA-DE-OURO, CLIPADOR-SKILL, ESTADO, CLIPAR-R0, REFERENCIAS, VARREDURA, MANUAL). Ou crie um Projeto novo chamado "CLIPADOR" e deixe o antigo morrer.
2. No campo "Instruções do projeto", cole o conteúdo inteiro de `01-INSTRUCOES-DO-PROJETO.md`.
3. Em "Conhecimento do projeto", suba estes 6 arquivos: `02-PAINEL.md`, `03-DINHEIRO.md`, `04-METODO.md`, `05-FERRAMENTAS.md`, `06-CALENDARIO.md`, `07-RADAR-ROTINA.md`.
4. Confira em Configurações > Conectores que OpusClip, Google Sheets e Google Drive estão ligados.

## Passo 2: a planilha (já criada, 1 min)
- CLIPADOR - Painel: https://docs.google.com/spreadsheets/d/1dXEjjHTLzzPUVy9Sg5Pw-CZZ3sh_mkVSSojsXPfuDrk/edit
- Está no seu Drive, com 5 abas e a aba CAMPANHAS já carregada com as 18 campanhas vistas em 12/10 (níveis, prazos, R$ por participante).
- Nada a fazer além de abrir e deixar nos favoritos.

## Passo 3: a rotina das 14h (já criada, 0 min)
- RADAR CLIPADOR, id `trig_01NZimqeU41Vg4NdWsX4dLX6`, todo dia às 13h46 de Manaus, notificação no celular. Primeira execução: 13/10.
- Ela aparece na lista de Rotinas do Claude. Para mudar o horário ou pausar: pelo chat ("pausa o radar") ou pela lista.
- A rotina antiga VARREDURA CLIPADOR (`trig_01LTdtdEQAcGoHgDYu3EmtM7`, 17h57, 37 conectores) está pausada. Pode apagar.

## Passo 4: o OpusClip (5 min, no site do OpusClip)
1. Configurações > Contas sociais: conectar o TikTok @zackairgames e o YouTube @zackfair1564.
2. Brand templates: criar o template "GAMES": proporção 9:16, layout Gameplay (rosto em cima, jogo embaixo), legenda em caixa alta, 2 a 4 palavras por linha, cor de destaque amarela, sem gancho automático, sem emoji.
3. Pronto. O Claude lê o id do template com `opusclip_list_brand_templates`.

## Passo 5: as plataformas de campanha (10 min)
Cadastro grátis, com Pix, e vínculo das contas da marca GAMES:
- Real Oficial: https://realoficial.com.br/pt/real-rewards (entrar em Wild Rift e Stream Gabriel Morais; olhar Kosky V2)
- Viewx: https://viewx.com.br/ (entrar no ranking João Pichau, #joaopichau)
- Klypex: https://klypex.com.br/
- Conty: https://appconty.com/seja-clipador
- Estourou: https://www.estourou.com/ (campanhas de música; usar na semana 2)
Em cada uma: abrir o regulamento da campanha e colar o texto no chat do projeto com a frase "regulamento [nome]". O Claude preenche a aba CAMPANHAS.

Whop (já tem conta, zackfairplay): abrir logado e ver se a campanha Dark Heresy ainda está em "suas campanhas". Se estiver, inscrever os 2 Shorts de Warhammer (1.350 e 1.123 views) dentro do prazo. Se fechou, esquecer.

## Passo 6: a marca VIRAIS (10 min, no celular)
- TikTok pessoal novo e canal do YouTube novo (Conta Google separada, verificação em 2 etapas).
- Nome curto, bio "fails e sustos que o Brasil ainda não viu". Sem nome de streamer na conta.

## Passo 7: deixar privado (1 min)
No YouTube Studio da @zackfair1564, o Short "A tense exchange..." (DEMO do OpusClip, restrito a maiores de 18): deixar privado.

## Primeira conversa no Projeto (hoje mesmo)
Cole isto:
> RADAR. Depois CLIPAR com a campanha Wild Rift: aqui vai o regulamento [cole]. Acervo da campanha: [link do Drive ou da pasta da campanha]. Momentos que separei: [minutos]. Quero 3 clipes hoje, cada um em TikTok e Shorts, e a FILA.

Se ainda não tiver o acervo, mande: "CLIPAR com a VOD de ontem do [streamer da campanha]: [link da Twitch ou YouTube], momentos [mm:ss, mm:ss, mm:ss]".

## Metas do mês (12/10 a 10/11)
150 a 180 clipes de games, 40 virais, 1 Pix recebido, R$ 50 a 300. Detalhe semana a semana em `06-CALENDARIO.md`.

## Arquivos
| Arquivo | Para quê |
|---|---|
| 01-INSTRUCOES-DO-PROJETO.md | O texto que vai no campo de instruções. É o cérebro |
| 02-PAINEL.md | Contas, ferramentas, decisões, pendências |
| 03-DINHEIRO.md | Plataformas, valores, regras que fazem perder dinheiro, golpes |
| 04-METODO.md | O que clipar, rubrica, ganchos, edição, duração |
| 05-FERRAMENTAS.md | Como o Claude usa o OpusClip e o resto, com os nomes exatos das funções |
| 06-CALENDARIO.md | Rotina diária e 30 dias programados |
| 07-RADAR-ROTINA.md | O que a rotina das 13h46 faz e o prompt dela |
| ../GUIA-DO-CLIPADOR.md | A pesquisa completa de 12/10 (fontes, preços, comparativos). Referência, não precisa subir no projeto |
