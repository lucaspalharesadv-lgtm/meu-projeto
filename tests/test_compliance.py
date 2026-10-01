import pytest

from robo_ig import compliance as c

OAB = "OAB/RO 11.037"


def rules(text):
    return {f.rule for f in c.check_text(text)}


@pytest.mark.parametrize("text,rule", [
    ("Garantimos a aprovação do seu benefício", "promessa_resultado"),
    ("Veja o depoimento de um cliente", "resultado_divulgado"),
    ("Primeira consulta gratuita!", "consulta_gratuita"),
    ("Só paga se ganhar", "consulta_gratuita"),
    ("Promoção de honorários", "preco_promocao"),
    ("Participe do sorteio", "sorteio_brinde"),
    ("O melhor advogado da região", "superlativo"),
    ("Processo 0001234-56.2023.8.22.0005", "numero_processo"),
    ("Sou especialista em INSS", "especialista"),
    ("Corra, últimas vagas", "captacao_agressiva"),
])
def test_detects(text, rule):
    assert rule in rules(text)


def test_clean_educational_text_passes():
    text = ("Plano de saúde negou seu medicamento? Em geral, a negativa deve ser fundamentada por escrito. "
            "Guarde o laudo médico e o protocolo. Salve este post.")
    assert c.check_text(text) == []


def test_missing_identification_is_flagged():
    findings = c.check_post("Texto informativo.", [{"title": "a", "body": "b"}], OAB)
    assert [f.rule for f in findings] == ["identificacao"]


def test_decide():
    assert c.decide([]) == "auto"
    assert c.decide(c.check_text("sou especialista")) == "review"
    assert c.decide(c.check_text("resultado garantido")) == "block"
