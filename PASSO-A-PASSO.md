# Como ligar o robô (em português simples)

O robô já está pronto. Ele escreve, faz a arte, confere as regras da OAB, posta carrosséis, Reels e stories
nos melhores horários, responde mensagens e manda um relatório todo domingo.

Ele só precisa de 5 "chaves" suas, porque só você pode autorizar o acesso às suas contas.
Se preferir, peça para um técnico ou para o Claude te guiar em cada uma. Cada uma leva uns 10 minutos.

## 1. Instagram
- Seu Instagram precisa ser conta **Profissional** e estar ligado a uma **Página do Facebook**.
- Em developers.facebook.com, crie um "app" e gere o token de acesso (a chave) com permissão de publicar e ler métricas.
- Anote: **IG_USER_ID** e **IG_ACCESS_TOKEN**.

## 2. Inteligência artificial (textos)
- Em console.anthropic.com, crie uma chave: **ANTHROPIC_API_KEY**.

## 3. Sua voz e seu rosto (só para os Reels)
- ElevenLabs: clone sua voz e anote **ELEVENLABS_API_KEY** e **ELEVENLABS_VOICE_ID**.
- HeyGen: crie seu avatar com um vídeo seu e anote **HEYGEN_API_KEY** e **HEYGEN_AVATAR_ID**.
- Sem isso o robô faz carrosséis e stories normalmente; só não faz os Reels.

## 4. Um servidor (computador ligado 24h)
- Contrate um servidor simples (VPS, uns R$ 30 a 50 por mês) com Docker instalado.
- Copie esta pasta para ele.

## 5. Preencher e ligar
1. Copie `.env.example` para `.env` e preencha com as chaves acima e seus dados.
2. Coloque seu logo em `assets/logo.png`.
3. Rode: `docker compose up -d --build`
4. Pronto. O robô monta a semana sozinho e começa a postar.

## Como acompanhar
- Você recebe aviso no Telegram quando um post precisar da sua aprovação e o relatório de domingo.
- Para ver a fila: `docker compose run --rm piloto robo-ig list`
- Para aprovar um post em dúvida: `docker compose run --rm piloto robo-ig approve NÚMERO`
