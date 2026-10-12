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
7. Textos: `opusclip_create_social_copy_job` exige conta social conectada no OpusClip. Enquanto não houver, o Claude escreve título, legenda e hashtags direto (04-METODO).
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

- A planilha CLIPADOR (link em 02-PAINEL) é o estado. O Claude lê com `get_values` e grava com `append_values` ou `update_values`.
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
