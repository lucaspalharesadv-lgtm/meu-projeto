from .config import Config
from .llm import LLM

SYSTEM = """Você é redator de conteúdo jurídico para o Instagram do advogado {nome} ({oab}), de {cidade}.
Áreas de atuação: {areas}.

OBJETIVO: conteúdo educativo que gere autoridade, salvamentos, compartilhamentos e mensagens espontâneas de pessoas
que reconhecem o próprio problema no post. Nunca captação ativa.

TOM: claro, humano, sem juridiquês, sem sensacionalismo. O leitor é leigo.

REGRAS ÉTICAS (OAB, Provimento 205/2021) - inviolável:
- informativo e discreto; nada de promessa/garantia de resultado, preço, gratuidade, promoção, sorteio, superlativos;
- sem depoimentos, casos reais, resultados obtidos, nomes de clientes ou números de processo;
- não use 'especialista'; use 'atuo em' ou 'área de atuação';
- NÃO cite julgado, súmula, tema repetitivo nem número de lei que não tenha sido fornecido abaixo; fale do direito de
  forma geral e correta. Quando houver dúvida sobre um dado, omita;
- fecha com convite discreto e informativo (ex.: 'Salve para consultar depois' / 'Dúvidas? Fale pelo direct'),
  nunca urgência ou escassez.

FORMATO DE SAÍDA: JSON puro, lista de objetos:
{{"area": str, "topic": str, "format": "carousel"|"single", "hook_style": str, "hook": str (<=70 caracteres, abre o carrossel),
 "slides": [{{"title": str (<=60), "body": str (<=220)}}] (carousel: 6 a 9 slides; single: 1),
 "caption": str (gancho na 1ª linha, 600-1200 caracteres, termina com: {footer}),
 "hashtags": [str] (5 a 8, sem # ),
 "alt_text": str}}"""


HOOK_STYLES = ["pergunta direta", "número ou lista", "dor do leitor", "mito vs verdade", "passo a passo", "erro comum"]


def build_user_prompt(n: int, assignments: list[tuple[str, str]], recent_topics: list[str], winners: list[dict]) -> str:
    plan = "\n".join(f"{i}. área: {a} | estilo do gancho: {st}" for i, (a, st) in enumerate(assignments, 1))
    parts = [f"Gere exatamente {n} itens, na ordem, cada um com a área e o estilo de gancho indicados. "
             f"Devolva em cada objeto o campo hook_style com o estilo usado.\n{plan}"]
    if winners:
        lines = "\n".join(f"- [{w['area']}] {w['topic']} | gancho ({w.get('style') or 'sem estilo'}): {w['hook']}" for w in winners)
        parts.append("Posts anteriores de MELHOR desempenho (mesmo estilo/ângulo, outros temas):\n" + lines)
    if recent_topics:
        parts.append("NÃO repita estes temas recentes:\n" + "\n".join(f"- {t}" for t in recent_topics))
    parts.append("Priorize dúvidas reais e frequentes de leigos (negativas de plano/SUS, INSS indeferido, nome sujo "
                 "indevido, cobranças bancárias, distrato de imóvel, verbas trabalhistas, execução fiscal).")
    return "\n\n".join(parts)


def _assign(cfg: Config, n: int, assignments):
    return assignments or [(cfg.areas[i % len(cfg.areas)], HOOK_STYLES[i % len(HOOK_STYLES)]) for i in range(n)]


def generate_posts(cfg: Config, llm: LLM, n: int, recent_topics: list[str], winners: list[dict],
                   assignments=None) -> list[dict]:
    system = SYSTEM.format(nome=cfg.nome, oab=cfg.oab, cidade=cfg.cidade,
                           areas=", ".join(cfg.areas), footer=cfg.footer)
    posts = llm.json(system, build_user_prompt(n, _assign(cfg, n, assignments), recent_topics, winners), max_tokens=8000)
    for p in posts:
        if cfg.footer not in p["caption"]:
            p["caption"] = p["caption"].rstrip() + "\n\n" + cfg.footer
    return posts


REEL_SYSTEM = """Você escreve roteiros de Reels (35 a 55 segundos) falados pelo próprio advogado {nome} ({oab}), de {cidade}.
Áreas: {areas}.

ESTRUTURA: gancho de 1 frase (dúvida real do leigo) -> 3 pontos curtos e corretos -> fecho discreto
('Salve este vídeo para consultar depois'). 85 a 130 palavras, frases curtas, fala natural, sem juridiquês, sem
emojis nem marcações de cena: o texto é lido em voz alta.

REGRAS ÉTICAS (OAB, Provimento 205/2021): as mesmas do conteúdo escrito - informativo e discreto; sem promessa de
resultado, preço, gratuidade, promoção, sorteio, superlativos, depoimentos, casos reais, 'especialista', julgado/súmula/
lei não fornecidos. Não diga seu nome nem OAB no roteiro (vão na legenda).

SAÍDA: JSON puro, lista de objetos:
{{"area": str, "topic": str, "hook_style": str, "hook": str, "script": str,
 "caption": str (300-700 caracteres, termina com: {footer}), "hashtags": [str] (5 a 8, sem #)}}"""

AI_NOTICE = "Vídeo produzido com inteligência artificial, a partir da minha voz e imagem, com roteiro revisado por mim."


def generate_reels(cfg: Config, llm: LLM, n: int, recent_topics: list[str], winners: list[dict],
                   assignments=None) -> list[dict]:
    system = REEL_SYSTEM.format(nome=cfg.nome, oab=cfg.oab, cidade=cfg.cidade,
                                areas=", ".join(cfg.areas), footer=cfg.footer)
    reels = llm.json(system, build_user_prompt(n, _assign(cfg, n, assignments), recent_topics, winners), max_tokens=6000)
    for r in reels:
        base = r["caption"].replace(cfg.footer, "").rstrip()
        r["caption"] = f"{base}\n\n{AI_NOTICE}\n\n{cfg.footer}"
    return reels


STORY_SYSTEM = """Você cria Stories de Instagram para o advogado {nome} ({oab}), de {cidade}. Áreas: {areas}.
Cada story tem 1 a 3 quadros de texto curto (título até 55 caracteres; corpo até 140). Formatos que funcionam: "Você sabia?",
"Mito ou verdade", "3 sinais de que...", "Dúvida da semana" (responda em termos gerais). Tom humano e simples.
Mesmas regras éticas do conteúdo escrito (Provimento 205/2021): informativo e discreto; nada de promessa de resultado,
preço, gratuidade, promoção, sorteio, superlativos, depoimentos, casos reais, 'especialista', julgado/súmula/lei não
fornecidos; sem urgência ou escassez; sem 'chame agora'.
SAÍDA: JSON puro, lista de objetos: {{"area": str, "topic": str, "hook_style": str, "frames": [{{"title": str, "body": str}}]}}"""


def generate_stories(cfg: Config, llm: LLM, n: int, recent_topics: list[str], winners: list[dict],
                     assignments=None) -> list[dict]:
    system = STORY_SYSTEM.format(nome=cfg.nome, oab=cfg.oab, cidade=cfg.cidade, areas=", ".join(cfg.areas))
    return llm.json(system, build_user_prompt(n, _assign(cfg, n, assignments), recent_topics, winners), max_tokens=5000)
