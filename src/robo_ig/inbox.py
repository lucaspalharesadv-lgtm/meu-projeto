"""Atendimento automático de DMs e comentários.

Regras: só responde a quem escreveu primeiro (janela de 24h da Meta), se identifica como assistente automático,
informa sem aconselhar caso concreto, não promete resultado nem fala de preço, e entrega o lead ao advogado.
Qualquer resposta do robô passa pelo mesmo filtro de publicidade da OAB.
"""
import re
import unicodedata

from . import compliance, db
from .config import Config
from .instagram import InstagramClient, InstagramError
from .llm import LLM
from .notify import notify

OPT_OUT = {"parar", "sair", "stop", "cancelar"}
URGENT = re.compile(r"\b(preso|prisao|flagrante|violencia|ameaca|risco de vida|uti|internad[oa]|audiencia amanha|prazo (vence|acaba) hoje)\b")

SYSTEM = """Você é o assistente virtual de atendimento do advogado {nome} ({oab}), de {cidade}. Atue em português, com tom
humano, empático e simples. Áreas: {areas}.

REGRAS (OAB, Provimento 205/2021, LGPD) - invioláveis:
- Na 1ª resposta diga que é um assistente automático do escritório e que a pessoa pode digitar PARAR a qualquer momento.
- Você NÃO presta consultoria jurídica nem opina sobre o caso concreto, prazo, chance de ganhar ou valor a receber.
  Dê só informação geral e cuidadosa e explique que quem avalia o caso é o advogado.
- Nunca prometa ou sugira resultado, nunca fale de honorários, preço, gratuidade ou desconto; se perguntarem, diga que
  o advogado trata disso na conversa.
- Não peça CPF, senhas, documentos nem dados de saúde detalhados. Colete só: nome, cidade e um resumo de 1-2 frases do
  problema. Faça UMA pergunta por mensagem. Mensagens curtas (até 450 caracteres).
- Não cite julgado, súmula ou número de lei.
- Quando tiver nome, cidade e o resumo (ou a pessoa pedir para falar com o advogado), marque ready_for_handoff.
- Se houver urgência (prisão, violência, risco à saúde/vida, prazo vencendo), marque urgent.

Responda SOMENTE JSON: {{"reply": str, "area": str|null, "urgent": bool, "ready_for_handoff": bool,
"summary": str, "lead": {{"nome": str|null, "cidade": str|null}}}}"""

FALLBACK = ("Obrigado pela mensagem! Vou encaminhar para o advogado, que retorna pessoalmente assim que possível. "
            "Se preferir, digite PARAR para não receber mais mensagens automáticas.")


def _norm(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", t.lower()) if not unicodedata.combining(c)).strip(" .!")


def _conv(conn, ig_user: str) -> dict:
    row = conn.execute("SELECT * FROM conversations WHERE ig_user=?", (ig_user,)).fetchone()
    if row is None:
        conn.execute("INSERT INTO conversations (ig_user, created_at) VALUES (?,?)", (ig_user, db.now_iso()))
        row = conn.execute("SELECT * FROM conversations WHERE ig_user=?", (ig_user,)).fetchone()
    return dict(row)


def _log(conn, conv_id: int, direction: str, text: str, mid: str | None = None) -> bool:
    try:
        conn.execute("INSERT INTO messages (conv_id, direction, text, mid, at) VALUES (?,?,?,?,?)",
                     (conv_id, direction, text, mid, db.now_iso()))
        return True
    except Exception:
        return False


def handle_message(cfg: Config, llm: LLM, client: InstagramClient, sender: str, text: str, mid: str | None) -> str:
    with db.connect(cfg.db_path) as conn:
        conv = _conv(conn, sender)
        if not _log(conn, conv["id"], "in", text, mid):
            return "duplicate"
        status = conv["status"]
        if status == "handoff":
            notify(cfg, f"Nova mensagem de lead em atendimento humano ({sender}): {text[:200]}")
            return "handoff-silent"
        if status == "optout" and _norm(text) not in {"voltar", "iniciar"}:
            return "optout"
        if _norm(text) in OPT_OUT:
            conn.execute("UPDATE conversations SET status='optout' WHERE id=?", (conv["id"],))
            reply, new_status, handoff = "Tudo bem, não enviarei mais mensagens automáticas. Obrigado pelo contato!", "optout", False
            return _send(cfg, conn, client, conv, sender, reply, new_status, handoff, None)
        if conv["bot_replies"] >= cfg.max_bot_replies:
            return _send(cfg, conn, client, conv, sender, FALLBACK, "handoff", True, {"summary": "limite de respostas do robô"})

        history = conn.execute("SELECT direction, text FROM messages WHERE conv_id=? ORDER BY id DESC LIMIT 12",
                               (conv["id"],)).fetchall()[::-1]
        convo = "\n".join(f"{'Cliente' if d == 'in' else 'Assistente'}: {t}" for d, t in history)
        system = SYSTEM.format(nome=cfg.nome, oab=cfg.oab, cidade=cfg.cidade, areas=", ".join(cfg.areas))
        try:
            out = llm.json(system, f"Conversa até agora:\n{convo}\n\nResponda à última mensagem do cliente.", max_tokens=700)
        except Exception as e:
            notify(cfg, f"Falha do assistente em {sender}: {e}")
            out = {"reply": FALLBACK, "urgent": True, "ready_for_handoff": True, "summary": "erro do assistente"}

        reply = out.get("reply") or FALLBACK
        urgent = bool(out.get("urgent")) or bool(URGENT.search(_norm(text)))
        handoff = bool(out.get("ready_for_handoff")) or urgent
        if any(f.severity in (compliance.BLOCK, compliance.WARN) for f in compliance.check_text(reply)):
            reply, handoff = FALLBACK, True
        info = {"area": out.get("area"), "summary": out.get("summary", ""), "lead": out.get("lead") or {}, "urgent": urgent}
        return _send(cfg, conn, client, conv, sender, reply, "handoff" if handoff else "bot", handoff, info)


def _send(cfg, conn, client, conv, sender, reply, new_status, handoff, info) -> str:
    if handoff and cfg.whatsapp_url and new_status == "handoff":
        reply += f"\n\nPara falar diretamente com o advogado: {cfg.whatsapp_url}"
    try:
        client.send_dm(sender, reply)
    except InstagramError as e:
        notify(cfg, f"Falha ao responder DM de {sender}: {e}")
        return "send-failed"
    _log(conn, conv["id"], "out", reply)
    conn.execute("UPDATE conversations SET bot_replies=bot_replies+1, status=? WHERE id=?", (new_status, conv["id"]))
    if info:
        import json
        conn.execute("UPDATE conversations SET area=?, summary=?, lead_json=? WHERE id=?",
                     (info.get("area"), info.get("summary"), json.dumps(info.get("lead", {}), ensure_ascii=False), conv["id"]))
    if handoff:
        lead = (info or {}).get("lead", {})
        tag = "URGENTE " if (info or {}).get("urgent") else ""
        notify(cfg, f"{tag}Lead pronto ({sender}) | {lead.get('nome')} - {lead.get('cidade')} | "
                    f"{(info or {}).get('area')} | {(info or {}).get('summary')}")
    return new_status


COMMENT_TRIGGER = re.compile(r"\b(como|posso|tenho direito|e se|meu caso|me ajuda|quero saber|duvida|\?)")


def handle_comment(cfg: Config, client: InstagramClient, comment_id: str, text: str, commenter: str) -> str:
    """Comentário com dúvida -> resposta privada única (Meta permite 1 por comentário, em até 7 dias)."""
    if commenter == cfg.ig_user_id or not COMMENT_TRIGGER.search(_norm(text)):
        return "ignored"
    msg = (f"Olá! Aqui é o assistente automático de {cfg.nome}. Vi sua dúvida no post e posso te explicar o caminho "
           "geral por aqui. Quem avalia o seu caso é o advogado. Pode me contar, em uma frase, o que aconteceu? "
           "(Digite PARAR para não receber mensagens.)")
    try:
        client.private_reply(comment_id, msg)
    except InstagramError as e:
        notify(cfg, f"Falha na resposta privada ao comentário {comment_id}: {e}")
        return "send-failed"
    return "replied"
