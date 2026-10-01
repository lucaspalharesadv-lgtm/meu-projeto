import hashlib
import hmac

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from . import inbox
from .config import Config
from .instagram import InstagramClient
from .llm import LLM

cfg = Config()
app = FastAPI(title="robo-ig webhook")


def valid_signature(secret: str, body: bytes, header: str | None) -> bool:
    if not secret or not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header.removeprefix("sha256="))


@app.get("/webhook")
def verify(mode: str = Query(alias="hub.mode", default=""), token: str = Query(alias="hub.verify_token", default=""),
           challenge: str = Query(alias="hub.challenge", default="")):
    if mode == "subscribe" and cfg.verify_token and hmac.compare_digest(token, cfg.verify_token):
        return PlainTextResponse(challenge)
    raise HTTPException(403)


def process_payload(payload: dict, llm=None, client=None) -> list[str]:
    llm = llm or LLM(cfg)
    client = client or InstagramClient(cfg)
    results = []
    for entry in payload.get("entry", []):
        for ev in entry.get("messaging", []):
            msg = ev.get("message") or {}
            sender = (ev.get("sender") or {}).get("id")
            if not sender or sender == cfg.ig_user_id or msg.get("is_echo") or not msg.get("text"):
                continue
            results.append(inbox.handle_message(cfg, llm, client, sender, msg["text"], msg.get("mid")))
        for ch in entry.get("changes", []):
            if ch.get("field") == "comments":
                v = ch.get("value", {})
                results.append(inbox.handle_comment(cfg, client, v.get("id", ""), v.get("text", ""),
                                                    (v.get("from") or {}).get("id", "")))
    return results


@app.post("/webhook")
async def receive(request: Request, tasks: BackgroundTasks):
    body = await request.body()
    if not valid_signature(cfg.app_secret, body, request.headers.get("X-Hub-Signature-256")):
        raise HTTPException(403, "assinatura inválida")
    tasks.add_task(process_payload, await request.json())
    return {"ok": True}
