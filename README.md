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

## Próximas fases
- **Fase 2 – DM e comentários:** webhook da Messaging API (resposta só dentro da janela de 24h após o contato do usuário),
  triagem do lead por área e envio para o seu WhatsApp. Sem abordagem ativa (captação vedada).
- **Fase 3 – Vídeo com voz e rosto:** roteiro → voz clonada (ElevenLabs) → avatar (HeyGen) → legenda e logo → Reels. Só com
  consentimento próprio e aviso de conteúdo sintético quando exigido.
- **Fase 4 – Otimização:** testes A/B de gancho, melhores horários por métrica, relatório semanal.

## Limites que o robô respeita
- Só API oficial (nada de automação de curtir/seguir/DM em massa: derruba a conta e configura captação).
- Não cita julgado/súmula sem fonte; qualquer dado jurídico preciso deve ser conferido por você.
