"""Filtro de publicidade da advocacia (Lei 8.906/94 art. 34 IV, CED arts. 39-47, Provimento CFOAB 205/2021).

Duas camadas: regras determinísticas (sempre rodam) e um juiz LLM (segunda opinião).
Publicação automática só ocorre quando as duas não encontram nada.
"""
import re
import unicodedata
from dataclasses import asdict, dataclass

BLOCK, WARN = "block", "warn"


@dataclass
class Finding:
    rule: str
    severity: str
    excerpt: str
    message: str
    source: str = "regra"


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


RULES: list[tuple[str, str, str, str]] = [
    ("promessa_resultado", BLOCK,
     r"garantimos|garantido|garantida|garanto|sucesso garantido|resultado garantido|causa ganha|ganhe sua causa|vitoria certa|aprovacao garantida|certeza de (ganhar|vencer)",
     "Promessa ou garantia de resultado é vedada (CED art. 39; Prov. 205/2021)."),
    ("resultado_divulgado", BLOCK,
     r"depoimento|caso(s)? de sucesso|antes e depois|resultados? (obtido|alcancado|conquistado)|ganhamos|conquistamos|nosso cliente (ganhou|recebeu|conseguiu)|cliente (ganhou|recebeu|conseguiu)",
     "Divulgação de resultados, depoimentos ou casos concretos é vedada (Prov. 205/2021)."),
    ("consulta_gratuita", BLOCK,
     r"(consulta|analise|avaliacao|orcamento) (gratis|gratuita|sem custo|sem compromisso)|sem custo|sem cobrar|so paga se ganhar|pague so no final",
     "Oferta de gratuidade ou condição de pagamento é mercantilização (CED art. 39; Prov. 205/2021)."),
    ("preco_promocao", BLOCK,
     r"promocao|desconto|oferta imperdivel|preco (baixo|justo|popular)|honorarios (a partir|de r\$)|parcelamos|advogado barato",
     "Divulgação de preços, promoções ou parcelamento de honorários é vedada."),
    ("sorteio_brinde", BLOCK,
     r"sorteio|sortear|brinde|ganhe um|concorra",
     "Sorteios e brindes configuram captação indevida."),
    ("superlativo", BLOCK,
     r"melhor (advogado|escritorio|advocacia)|os melhores|numero 1|n[o°º]\.? ?1\b|\blider\b|referencia nacional|maior escritorio",
     "Autopromoção com superlativos é vedada (CED art. 39; Prov. 205/2021)."),
    ("numero_processo", BLOCK,
     r"\b\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}\b",
     "Número de processo pode identificar cliente (sigilo profissional, CED art. 35)."),
    ("cpf", BLOCK, r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", "Dado pessoal (CPF) não pode ser publicado."),
    ("especialista", WARN, r"\bespecialista\b",
     "Só pode usar 'especialista' quem tem título reconhecido; prefira 'atua em' / 'área de atuação'."),
    ("captacao_agressiva", WARN,
     r"ligue (agora|ja)|chame (agora|ja)|corra|ultimas vagas|so hoje|nao perca|aproveite|ultima chance|urgente!",
     "Chamada com urgência/escassez destoa da discrição exigida na publicidade da advocacia."),
    ("comparacao", WARN, r"outros advogados|advogados que (prometem|cobram|enganam)|escritorios? concorrente",
     "Comparação com colegas pode violar o dever de urbanidade e a vedação de captação."),
    ("valores", WARN, r"r\$ ?\d",
     "Valores em reais exigem revisão: só informativos (ex.: teto legal), nunca honorários."),
    ("gratuidade", WARN, r"\bgratis\b|gratuit[oa]",
     "Termo de gratuidade: confirme que é conteúdo informativo (ex.: justiça gratuita), não oferta do escritório."),
    ("percentual_absoluto", WARN, r"100 ?%", "Percentual absoluto pode soar como promessa de resultado."),
]
_COMPILED = [(r, s, re.compile(p), m) for r, s, p, m in RULES]


def check_text(text: str) -> list[Finding]:
    norm = _norm(text)
    findings = []
    for rule, severity, rx, message in _COMPILED:
        for m in rx.finditer(norm):
            findings.append(Finding(rule, severity, m.group(0), message))
    return findings


def check_post(caption: str, slides: list[dict], oab: str, hook: str = "", require_id: bool = True) -> list[Finding]:
    parts = [caption, hook] + [f"{s.get('title', '')} {s.get('body', '')}" for s in slides]
    findings = check_text("\n".join(parts))
    if require_id and _norm(oab) not in _norm(caption):
        findings.append(Finding("identificacao", WARN, "", f"Legenda sem identificação do advogado ({oab}).", "regra"))
    return findings


JUDGE_SYSTEM = """Você é revisor de publicidade da advocacia no Brasil. Avalie o post de Instagram de um advogado
contra: Lei 8.906/94 art. 34 IV; Código de Ética e Disciplina da OAB arts. 39 a 47; Provimento CFOAB 205/2021.
Verifique: caráter informativo e discreto; ausência de captação de clientela, mercantilização, promessa/garantia de
resultado, divulgação de preços/gratuidade, depoimentos e resultados, superlativos, sensacionalismo, sigilo
profissional, uso indevido de 'especialista', afirmações jurídicas imprecisas ou que induzam o leitor a erro,
citação de julgado/súmula/tema sem fonte fornecida (suspeita de invenção).
Responda SOMENTE JSON: {"approved": bool, "issues": [{"trecho": str, "problema": str, "gravidade": "block"|"warn"}]}"""


def judge_with_llm(llm, caption: str, slides: list[dict]) -> list[Finding]:
    payload = {"legenda": caption, "slides": slides}
    verdict = llm.json(JUDGE_SYSTEM, str(payload), max_tokens=1200)
    findings = [
        Finding("juiz_llm", i.get("gravidade", WARN) if i.get("gravidade") in (BLOCK, WARN) else WARN,
                i.get("trecho", ""), i.get("problema", ""), "llm")
        for i in verdict.get("issues", [])
    ]
    if not verdict.get("approved", False) and not findings:
        findings.append(Finding("juiz_llm", WARN, "", "Revisor automático não aprovou o post.", "llm"))
    return findings


def decide(findings: list[Finding]) -> str:
    """'auto' publica sozinho; 'review' espera aprovação humana; 'block' exige reescrita."""
    if any(f.severity == BLOCK for f in findings):
        return "block"
    return "review" if findings else "auto"


def to_dicts(findings: list[Finding]) -> list[dict]:
    return [asdict(f) for f in findings]
