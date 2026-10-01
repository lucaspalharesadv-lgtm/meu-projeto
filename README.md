# robo-ig — Instagram da advocacia no piloto automático (com filtro OAB)

> **Estado real (01/10/2026):** todo o código foi testado com objetos simulados (44 testes). **Nenhuma chamada real** foi feita à
> Meta, à Claude API, ao ElevenLabs ou à HeyGen; nada está em produção. Os endpoints da HeyGen não foram validados e DM de
> terceiros exige App Review da Meta. Por padrão `REVIEW_ALL=true`: tudo passa pela sua aprovação (`robo-ig approve ID`) até
> você decidir liberar a publicação automática.


**Fase 1 (implementada; testada só com simulações):** gera pauta → legenda + carrossel → arte com sua marca/logo → filtro OAB (regras + revisor IA)
→ agenda → publica pela **API oficial** da Meta → coleta métricas e usa o que mais funcionou para gerar os próximos.

```
plan ─► Claude gera posts ─► filtro OAB (regras + juiz IA) ─► arte (Pillow) ─► fila
                                   │ ok                │ dúvida            │ infração
                               approved          needs_review          blocked
                                   └─► publish (cron 15 min) ─► insights ─► realimenta o plan
```

## Autonomia
- Com `REVIEW_ALL=false` e nenhum achado no filtro: **publica sozinho** no horário. Padrão atual (`true`): todo post espera sua aprovação.
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

## Fase 2 – DM e comentários (implementada; testada só com simulações)
`robo-ig serve` sobe o webhook (`/webhook`, porta 8000, atrás de HTTPS). No app Meta, assine os campos `messages` e
`comments` do Instagram e use `WEBHOOK_VERIFY_TOKEN` e `META_APP_SECRET` do `.env` (a assinatura X-Hub-Signature-256 é validada).
Para DMs de terceiros, a permissão `instagram_manage_messages` exige App Review da Meta.

- Responde **só quem escreve primeiro** (ou comenta com dúvida, via resposta privada única). Nunca abordagem ativa.
- Se apresenta como assistente automático, aceita `PARAR`, não dá parecer sobre o caso, não fala de preço/resultado.
- Coleta nome, cidade e resumo; ao completar, envia o link do seu WhatsApp (`WHATSAPP_URL`) e avisa você (Telegram).
- Urgência (prisão, violência, risco de vida, prazo vencendo) ou resposta reprovada pelo filtro OAB: passa direto para você.
- Depois do repasse o robô fica em silêncio nessa conversa; você avisa quando assumir.

## Fase 3 – Reels com sua voz e rosto (implementada; testada só com simulações)
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

## Fase 4 – Piloto automático de marketing (implementada; testada só com simulações)
Um único cron faz tudo: `*/15 * * * * robo-ig tick` (e `robo-ig serve` ligado para as DMs).

| O que | Como |
|---|---|
| Calendário | Mantém a fila dos próximos 7 dias cheia conforme `WEEK_MIX` (padrão: 3 carrosséis, 2 Reels, 7 stories) |
| Stories | 1 a 3 quadros 9:16 dentro das zonas seguras do app, com sua identificação; além disso, todo post novo no feed gera um story-aviso 20 min depois |
| Horários | Aprende com as suas métricas: pontuação por hora local (feed e stories separados), encolhida para a média quando há poucos dados; `EXPLORE` (20%) sorteia horários ainda não testados. Sem dados, começa por 12h, 19h, 20h, 18h. Limites: `FEED_PER_DAY`, `STORIES_PER_DAY`, 3h entre posts do mesmo tipo |
| Conteúdo | Cada item recebe (área, estilo de gancho) sorteados com peso no que performa: pergunta, número, dor, mito vs verdade, passo a passo, erro comum |
| Formato | Com 5+ posts de cada, se um formato engaja 30% mais que o outro, move 1 vaga semanal para ele |
| Métricas | Feed: 1x/dia por 30 dias; stories: a cada 3h enquanto estão no ar. Pontuação = (salvos×3 + compart.×4 + comentários×2 + curtidas) / alcance |
| Relatório | Domingo, 20h (local): `data/reports/AAAA-MM-DD.md` + resumo no Telegram. Também: `robo-ig report` |
| Segurança | Todo item passa pelo filtro OAB; título/gancho agora também são checados. Planejamento roda no máx. a cada 12h (sem laço de custo) |

Comandos manuais: `plan-week`, `plan-stories -n 7`, `plan -n 3`, `plan-reels -n 2`, `report`, `list`, `approve ID`.
Limitações da API da Meta: stories saem só como imagem/vídeo (sem figurinhas de enquete/pergunta), e métricas de story somem após ~24h.

## Próximas ideias
- Biblioteca de temas sazonais (ex.: reajuste de planos, calendário do INSS) e gatilhos por notícia jurídica.
- Teste de capa/gancho em Reels a partir dos resultados de retenção.
