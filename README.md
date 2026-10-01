# robo-ig — Instagram da advocacia no piloto automático (com filtro OAB)

**Fase 1 (pronta):** gera pauta → legenda + carrossel → arte com sua marca/logo → filtro OAB (regras + revisor IA)
→ agenda → publica pela **API oficial** da Meta → coleta métricas e usa o que mais funcionou para gerar os próximos.

```
plan ─► Claude gera posts ─► filtro OAB (regras + juiz IA) ─► arte (Pillow) ─► fila
                                   │ ok                │ dúvida            │ infração
                               approved          needs_review          blocked
                                   └─► publish (cron 15 min) ─► insights ─► realimenta o plan
```

## Autonomia
- Sem nenhum achado no filtro: **publica sozinho** no horário (`POST_HOURS`).
- Achado leve (`warn`, ex.: "especialista", valores em R$): vai para `needs_review` e você é avisado (Telegram opcional).
- Achado grave (`block`: promessa de resultado, preço/gratuidade, depoimento, sorteio, superlativo, nº de processo): nunca publica.

Regras em `src/robo_ig/compliance.py` (Lei 8.906 art. 34 IV, CED arts. 39-47, Provimento 205/2021). Você continua responsável por cada post: revise as regras com a sua leitura do Provimento e do TED/OAB-RO.

## Instalar
```bash
pip install -e ".[dev]" && cp .env.example .env   # preencha o .env
pytest                                            # testa o filtro OAB
```
1. **Instagram**: conta Profissional (Comercial/Criador) ligada a uma Página do Facebook. Em developers.facebook.com crie um app,
   gere token de longa duração com `instagram_basic`, `instagram_content_publish`, `instagram_manage_insights`,
   `pages_show_list`, `pages_read_engagement`. Para a **sua própria conta** o app pode ficar em modo desenvolvimento (sem App Review).
2. **Mídia pública**: a Meta baixa a imagem por URL. Sirva `MEDIA_DIR` em um domínio (Cloudflare R2/S3/Caddy) e ponha em `PUBLIC_MEDIA_BASE_URL`.
3. Coloque seu logo em `assets/logo.png` (PNG transparente) e, se quiser, fontes da marca em `FONT_BOLD`/`FONT_REGULAR`.

## Uso
```bash
robo-ig plan -n 7        # gera uma semana, filtra, renderiza e agenda
robo-ig list             # fila e status
robo-ig show 12          # post completo + achados do filtro
robo-ig approve 12       # libera um post em revisão
robo-ig reject 12
robo-ig publish          # cron: */15 * * * *
robo-ig insights         # cron: diário
```

## Fase 2 – DM e comentários (pronta)
`robo-ig serve` sobe o webhook (`/webhook`, porta 8000, atrás de HTTPS). No app Meta, assine os campos `messages` e
`comments` do Instagram e use `WEBHOOK_VERIFY_TOKEN` e `META_APP_SECRET` do `.env` (a assinatura X-Hub-Signature-256 é validada).
Para DMs de terceiros, a permissão `instagram_manage_messages` exige App Review da Meta.

- Responde **só quem escreve primeiro** (ou comenta com dúvida, via resposta privada única). Nunca abordagem ativa.
- Se apresenta como assistente automático, aceita `PARAR`, não dá parecer sobre o caso, não fala de preço/resultado.
- Coleta nome, cidade e resumo; ao completar, envia o link do seu WhatsApp (`WHATSAPP_URL`) e avisa você (Telegram).
- Urgência (prisão, violência, risco de vida, prazo vencendo) ou resposta reprovada pelo filtro OAB: passa direto para você.
- Depois do repasse o robô fica em silêncio nessa conversa; você avisa quando assumir.

## Fase 3 – Reels com sua voz e rosto (pronta)
```
robo-ig plan-reels -n 3     # roteiro -> filtro OAB -> voz (ElevenLabs) -> avatar (HeyGen) -> legenda + logo -> fila
```
1. Clone sua voz no ElevenLabs (Instant Voice Clone, com amostra sua) e crie seu avatar na HeyGen (a partir de vídeo seu);
   preencha `ELEVENLABS_*` e `HEYGEN_*` no `.env`. **Requer `ffmpeg` instalado** (legenda palavra a palavra e logo).
2. O filtro OAB roda no roteiro **antes** de gastar com voz/avatar. Roteiro em `needs_review` só vira vídeo quando você
   rodar `robo-ig approve ID`; roteiro bloqueado nunca gera custo.
3. A legenda ganha o aviso de que o vídeo foi produzido com IA a partir da sua voz e imagem (transparência; a Meta
   também pede rótulo de conteúdo gerado por IA, marque no app se a opção aparecer).
4. Publica como Reel (`media_type=REELS`) no mesmo `publish` do cron.

Os endpoints da HeyGen estão em `avatar.py`, isolados: confira a documentação vigente no primeiro teste real.

## Próximas fases
- **Fase 4 – Otimização:** testes A/B de gancho, melhores horários por métrica, relatório semanal.

## Limites que o robô respeita
- Só API oficial (nada de automação de curtir/seguir/DM em massa: derruba a conta e configura captação).
- Não cita julgado/súmula sem fonte; qualquer dado jurídico preciso deve ser conferido por você.
