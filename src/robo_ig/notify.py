import requests

from .config import Config


def notify(cfg: Config, text: str) -> None:
    print(text)
    if cfg.telegram_token and cfg.telegram_chat:
        requests.post(f"https://api.telegram.org/bot{cfg.telegram_token}/sendMessage",
                      data={"chat_id": cfg.telegram_chat, "text": text}, timeout=15)
