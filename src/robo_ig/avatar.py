"""Gera o vídeo do seu avatar (rosto) falando com o áudio da sua voz clonada (HeyGen).

Os endpoints abaixo seguem a API v2 da HeyGen; confira a documentação vigente antes do primeiro uso.
"""
import time

import requests

from .config import Config


class AvatarError(RuntimeError):
    pass


def render_avatar_video(cfg: Config, mp3_path: str, out_path: str, timeout_s: int = 900) -> str:
    h = {"X-Api-Key": cfg.heygen_key}
    with open(mp3_path, "rb") as f:
        up = requests.post("https://upload.heygen.com/v1/asset", headers={**h, "Content-Type": "audio/mpeg"},
                           data=f.read(), timeout=120)
    up.raise_for_status()
    asset_id = up.json()["data"]["id"]

    gen = requests.post("https://api.heygen.com/v2/video/generate", headers=h, timeout=60, json={
        "video_inputs": [{
            "character": {"type": "avatar", "avatar_id": cfg.heygen_avatar, "avatar_style": "normal"},
            "voice": {"type": "audio", "audio_asset_id": asset_id},
        }],
        "dimension": {"width": 1080, "height": 1920},
    })
    gen.raise_for_status()
    video_id = gen.json()["data"]["video_id"]

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        st = requests.get("https://api.heygen.com/v1/video_status.get", headers=h, params={"video_id": video_id},
                          timeout=30).json()["data"]
        if st["status"] == "completed":
            with open(out_path, "wb") as f:
                f.write(requests.get(st["video_url"], timeout=300).content)
            return out_path
        if st["status"] == "failed":
            raise AvatarError(str(st.get("error")))
        time.sleep(10)
    raise AvatarError("timeout na geração do avatar")
