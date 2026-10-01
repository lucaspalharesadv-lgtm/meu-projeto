import os
import subprocess

from . import avatar, voice
from .config import Config


def srt_from_words(words: list[dict], per_line: int = 3) -> str:
    def ts(t: float) -> str:
        ms = int(round(t * 1000))
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"

    out = []
    for i in range(0, len(words), per_line):
        chunk = words[i:i + per_line]
        out.append(f"{i // per_line + 1}\n{ts(chunk[0]['start'])} --> {ts(chunk[-1]['end'])}\n"
                   + " ".join(w["word"] for w in chunk).upper() + "\n")
    return "\n".join(out)


def ffmpeg_args(cfg: Config, src: str, srt: str, dst: str) -> list[str]:
    style = ("FontName=DejaVu Sans,Bold=1,FontSize=16,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,"
             "BorderStyle=1,Outline=3,Alignment=2,MarginV=260")
    sub = f"subtitles={srt}:force_style='{style}'"
    if os.path.exists(cfg.logo_path):
        return ["ffmpeg", "-y", "-i", src, "-i", cfg.logo_path, "-filter_complex",
                f"[1:v]scale=220:-1[lg];[0:v][lg]overlay=W-w-60:80[v];[v]{sub}[out]",
                "-map", "[out]", "-map", "0:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                "-movflags", "+faststart", dst]
    return ["ffmpeg", "-y", "-i", src, "-vf", sub, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            "-movflags", "+faststart", dst]


def finish_video(cfg: Config, src: str, words: list[dict], out_dir: str) -> str:
    srt_path = os.path.join(out_dir, "legenda.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_from_words(words))
    dst = os.path.join(out_dir, "reel.mp4")
    subprocess.run(ffmpeg_args(cfg, src, srt_path, dst), check=True, capture_output=True)
    return dst


def produce_reel(cfg: Config, post_id: int, script: str) -> str:
    """roteiro -> voz clonada -> avatar -> legenda + logo -> MP4 pronto para Reels."""
    out_dir = os.path.join(cfg.media_dir, f"post_{post_id}")
    os.makedirs(out_dir, exist_ok=True)
    mp3 = os.path.join(out_dir, "voz.mp3")
    words = voice.synthesize(cfg, script, mp3)
    raw = avatar.render_avatar_video(cfg, mp3, os.path.join(out_dir, "avatar.mp4"))
    return finish_video(cfg, raw, words, out_dir)
