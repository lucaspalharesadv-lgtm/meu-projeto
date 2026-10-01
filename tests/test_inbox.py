import hashlib
import hmac
from dataclasses import replace

from robo_ig import db, inbox
from robo_ig.config import Config
from robo_ig.server import valid_signature


class FakeLLM:
    def __init__(self, out): self.out = out
    def json(self, *a, **k): return self.out


class FakeClient:
    def __init__(self): self.sent = []
    def send_dm(self, to, text): self.sent.append((to, text))
    def private_reply(self, cid, text): self.sent.append((cid, text))


def cfg_for(tmp_path):
    return replace(Config(), db_path=str(tmp_path / "t.db"), whatsapp_url="https://wa.me/5569", ig_user_id="me")


def test_signature():
    body = b'{"a":1}'
    sig = "sha256=" + hmac.new(b"s", body, hashlib.sha256).hexdigest()
    assert valid_signature("s", body, sig)
    assert not valid_signature("s", body, "sha256=00")
    assert not valid_signature("", body, sig)


def test_flow_handoff_and_dedupe(tmp_path):
    cfg, client = cfg_for(tmp_path), FakeClient()
    llm = FakeLLM({"reply": "Olá! Sou o assistente automático. Qual seu nome?", "ready_for_handoff": False})
    assert inbox.handle_message(cfg, llm, client, "u1", "oi, meu plano negou o remédio", "m1") == "bot"
    assert inbox.handle_message(cfg, llm, client, "u1", "oi, meu plano negou o remédio", "m1") == "duplicate"
    llm.out = {"reply": "Obrigado, João. Vou encaminhar.", "ready_for_handoff": True, "area": "saúde",
               "summary": "plano negou remédio", "lead": {"nome": "João", "cidade": "Ji-Paraná"}}
    assert inbox.handle_message(cfg, llm, client, "u1", "João, Ji-Paraná", "m2") == "handoff"
    assert "wa.me" in client.sent[-1][1]
    assert inbox.handle_message(cfg, llm, client, "u1", "alguém aí?", "m3") == "handoff-silent"


def test_optout_and_unsafe_reply(tmp_path):
    cfg, client = cfg_for(tmp_path), FakeClient()
    assert inbox.handle_message(cfg, FakeLLM({}), client, "u2", "PARAR", "m1") == "optout"
    assert inbox.handle_message(cfg, FakeLLM({}), client, "u2", "oi", "m2") == "optout"
    llm = FakeLLM({"reply": "Garantimos que você vai ganhar a causa!", "ready_for_handoff": False})
    assert inbox.handle_message(cfg, llm, client, "u3", "posso ganhar?", "m3") == "handoff"
    assert "Garantimos" not in client.sent[-1][1]


def test_urgent_keyword_forces_handoff(tmp_path):
    cfg, client = cfg_for(tmp_path), FakeClient()
    llm = FakeLLM({"reply": "Vou avisar o advogado agora.", "ready_for_handoff": False})
    assert inbox.handle_message(cfg, llm, client, "u4", "meu filho foi preso em flagrante", "m1") == "handoff"


def test_comment_trigger(tmp_path):
    cfg, client = cfg_for(tmp_path), FakeClient()
    assert inbox.handle_comment(cfg, client, "c1", "Como faço para recorrer?", "u9") == "replied"
    assert inbox.handle_comment(cfg, client, "c2", "Parabéns!", "u9") == "ignored"
    assert inbox.handle_comment(cfg, client, "c3", "como assim?", "me") == "ignored"
