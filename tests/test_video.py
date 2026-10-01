import subprocess
from dataclasses import replace

import pytest

from robo_ig import db, pipeline
from robo_ig.config import Config
from robo_ig.video import ffmpeg_args, finish_video, srt_from_words
from robo_ig.voice import words_from_alignment


def test_words_from_alignment():
    al = {"characters": list("oi tudo"), "character_start_times_seconds": [i * .1 for i in range(7)],
          "character_end_times_seconds": [(i + 1) * .1 for i in range(7)]}
    w = words_from_alignment(al)
    assert [x["word"] for x in w] == ["oi", "tudo"]
    assert w[1]["start"] == pytest.approx(0.3) and w[1]["end"] == pytest.approx(0.7)


def test_srt():
    words = [{"word": f"p{i}", "start": i, "end": i + .9} for i in range(4)]
    srt = srt_from_words(words, per_line=3)
    assert "00:00:00,000 --> 00:00:02,900" in srt and "P0 P1 P2" in srt and "\n2\n" in srt


def test_finish_video_with_real_ffmpeg(tmp_path):
    src = tmp_path / "in.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=360x640:d=2", "-f", "lavfi",
                    "-i", "sine=d=2", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(src)],
                   check=True, capture_output=True)
    cfg = replace(Config(), review_all=False, logo_path=str(tmp_path / "nao_existe.png"))
    words = [{"word": "teste", "start": 0, "end": 1}, {"word": "legenda", "start": 1, "end": 1.9}]
    out = finish_video(cfg, str(src), words, str(tmp_path))
    assert (tmp_path / "reel.mp4").stat().st_size > 0 and out.endswith("reel.mp4")


def test_logo_branch_uses_overlay(tmp_path):
    logo = tmp_path / "l.png"
    logo.write_bytes(b"x")
    args = ffmpeg_args(replace(Config(), review_all=False, logo_path=str(logo)), "a.mp4", "s.srt", "o.mp4")
    assert "-filter_complex" in args


class OkLLM:
    def json(self, *a, **k): return {"approved": True, "issues": []}


def _reel(cfg, script, caption=None):
    with db.connect(cfg.db_path) as c:
        return db.insert_post(c, topic="t", area="saúde", format="reel", hook="Plano negou?",
                              slides_json=[{"title": "h", "body": script}],
                              caption=caption or f"Informativo.\n\n{cfg.footer}", hashtags="#x",
                              scheduled_at="2020-01-01T00:00:00+00:00")


def status(cfg, pid):
    with db.connect(cfg.db_path) as c:
        return db.get_post(c, pid)


def test_reel_auto_generates_video(tmp_path, monkeypatch):
    cfg = replace(Config(), review_all=False, db_path=str(tmp_path / "t.db"), media_dir=str(tmp_path / "pub"))
    monkeypatch.setattr(pipeline, "produce_reel", lambda c, pid, script: "/x/reel.mp4")
    pid = _reel(cfg, "Plano de saúde negou? Peça a negativa por escrito.")
    assert pipeline.process(cfg, pid, OkLLM()) == "approved"
    assert status(cfg, pid)["image_paths_json"] == ["/x/reel.mp4"]


def test_reel_blocked_script_costs_nothing(tmp_path, monkeypatch):
    cfg = replace(Config(), review_all=False, db_path=str(tmp_path / "t.db"))
    monkeypatch.setattr(pipeline, "produce_reel", lambda *a: pytest.fail("não deveria gerar vídeo"))
    pid = _reel(cfg, "Garantimos resultado na sua causa.")
    assert pipeline.process(cfg, pid, OkLLM()) == "blocked"


def test_reel_review_then_approve_makes_video(tmp_path, monkeypatch):
    cfg = replace(Config(), review_all=False, db_path=str(tmp_path / "t.db"))
    calls = []
    monkeypatch.setattr(pipeline, "produce_reel", lambda c, pid, script: calls.append(pid) or "/x/r.mp4")
    pid = _reel(cfg, "Sou especialista em INSS e explico o recurso.")
    assert pipeline.process(cfg, pid, OkLLM()) == "needs_review" and not calls
    pipeline.set_status(cfg, pid, "approved")
    assert calls == [pid] and status(cfg, pid)["status"] == "approved"


def test_reel_video_failure_is_recorded(tmp_path, monkeypatch):
    cfg = replace(Config(), review_all=False, db_path=str(tmp_path / "t.db"))
    def boom(*a): raise RuntimeError("heygen fora")
    monkeypatch.setattr(pipeline, "produce_reel", boom)
    pid = _reel(cfg, "Explicação geral sobre recurso.")
    assert pipeline.process(cfg, pid, OkLLM()) == "failed"
    assert "heygen fora" in status(cfg, pid)["error"]
