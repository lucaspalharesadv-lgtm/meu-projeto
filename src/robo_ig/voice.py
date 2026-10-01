import base64

import requests

from .config import Config


def synthesize(cfg: Config, text: str, mp3_path: str) -> list[dict]:
    """Fala o roteiro com a sua voz clonada (ElevenLabs). Devolve as palavras com início/fim em segundos."""
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{cfg.eleven_voice}/with-timestamps",
        headers={"xi-api-key": cfg.eleven_key},
        json={"text": text, "model_id": "eleven_multilingual_v2",
              "voice_settings": {"stability": 0.5, "similarity_boost": 0.85}},
        timeout=180,
    )
    r.raise_for_status()
    data = r.json()
    with open(mp3_path, "wb") as f:
        f.write(base64.b64decode(data["audio_base64"]))
    return words_from_alignment(data["alignment"])


def words_from_alignment(al: dict) -> list[dict]:
    words, cur, start, end = [], "", None, 0.0
    for ch, t0, t1 in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append({"word": cur, "start": start, "end": end})
            cur, start = "", None
            continue
        if start is None:
            start = t0
        cur += ch
        end = t1
    if cur:
        words.append({"word": cur, "start": start, "end": end})
    return words
