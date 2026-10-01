import random

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
{{"area": str, "topic": str, "format": "carousel"|"single", "hook": str (<=70 caracteres, abre o carrossel),
 "slides": [{{"title": str (<=60), "body": str (<=220)}}] (carousel: 6 a 9 slides; single: 1),
 "caption": str (gancho na 1ª linha, 600-1200 caracteres, termina com: {footer}),
 "hashtags": [str] (5 a 8, sem # ),
 "alt_text": str}}"""


def build_user_prompt(n: int, areas: list[str], recent_topics: list[str], winners: list[dict]) -> str:
    parts = [f"Gere {n} posts, variando entre estas áreas (uma por post, sem repetir em sequência): {', '.join(areas)}."]
    if winners:
        lines = "\n".join(f"- [{w['area']}] {w['topic']} (hook: {w['hook']})" for w in winners)
        parts.append("Posts anteriores de MELHOR desempenho (mesmo estilo/ângulo, outros temas):\n" + lines)
    if recent_topics:
        parts.append("NÃO repita estes temas recentes:\n" + "\n".join(f"- {t}" for t in recent_topics))
    parts.append("Priorize dúvidas reais e frequentes de leigos (negativas de plano/SUS, INSS indeferido, nome sujo "
                 "indevido, cobranças bancárias, distrato de imóvel, verbas trabalhistas, execução fiscal).")
    return "\n\n".join(parts)


def generate_posts(cfg: Config, llm: LLM, n: int, recent_topics: list[str], winners: list[dict]) -> list[dict]:
    system = SYSTEM.format(nome=cfg.nome, oab=cfg.oab, cidade=cfg.cidade,
                           areas=", ".join(cfg.areas), footer=cfg.footer)
    areas = random.sample(cfg.areas, k=min(len(cfg.areas), n)) if n <= len(cfg.areas) else cfg.areas
    posts = llm.json(system, build_user_prompt(n, areas, recent_topics, winners), max_tokens=8000)
    for p in posts:
        if cfg.footer not in p["caption"]:
            p["caption"] = p["caption"].rstrip() + "\n\n" + cfg.footer
    return posts
