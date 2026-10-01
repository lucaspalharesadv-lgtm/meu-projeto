import random
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from robo_ig import db, learning, pipeline, report
from robo_ig.config import Config


@pytest.fixture
def cfg(tmp_path):
    return replace(Config(), review_all=False, db_path=str(tmp_path / "t.db"), media_dir=str(tmp_path / "pub"),
                   logo_path=str(tmp_path / "x.png"), explore=0.0)


class OkLLM:
    def json(self, *a, **k): return {"approved": True, "issues": []}


def add_published(conn, cfg, hour, fmt="carousel", area="saúde", style="pergunta direta", reach=1000, saved=0, shares=0,
                  days_ago=2, topic="t"):
    tz = ZoneInfo(cfg.timezone)
    day = datetime.now(tz) - timedelta(days=days_ago)
    pub = day.replace(hour=hour, minute=0, second=0, microsecond=0).astimezone(timezone.utc).isoformat(timespec="seconds")
    pid = db.insert_post(conn, topic=topic, area=area, format=fmt, status="published", hook_style=style,
                         published_at=pub, ig_media_id="m", slides_json=[], scheduled_at=pub)
    conn.execute("INSERT INTO metrics (post_id, fetched_at, reach, likes, comments, saved, shares) VALUES (?,?,?,?,?,?,?)",
                 (pid, db.now_iso(), reach, 0, 0, saved, shares))
    return pid


def test_best_hour_wins_after_data(cfg):
    with db.connect(cfg.db_path) as c:
        for d in range(3):
            add_published(c, cfg, 21, saved=50, days_ago=d + 1)
            add_published(c, cfg, 12, saved=1, days_ago=d + 1)
        ranked = learning.rank_hours(cfg, c, "feed")
    assert ranked[0] == 21 and ranked.index(21) < ranked.index(12)


def test_no_data_uses_default_order(cfg):
    with db.connect(cfg.db_path) as c:
        assert learning.rank_hours(cfg, c, "feed")[:3] == [12, 19, 20]


def test_pick_slots_respects_daily_limit_and_gap(cfg):
    cfg = replace(cfg, stories_per_day=2)
    with db.connect(cfg.db_path) as c:
        slots = learning.pick_slots(cfg, c, 6, "story", rng=random.Random(1))
    tz = ZoneInfo(cfg.timezone)
    local = [datetime.fromisoformat(s).astimezone(tz) for s in slots]
    assert len(local) == 6 and all(t > datetime.now(tz) for t in local)
    for d in {t.date() for t in local}:
        hrs = sorted(t.hour for t in local if t.date() == d)
        assert len(hrs) <= 2 and (len(hrs) < 2 or hrs[1] - hrs[0] >= 3)


def test_pick_slots_skips_already_taken(cfg):
    with db.connect(cfg.db_path) as c:
        first = learning.pick_slots(cfg, c, 1, "feed")
        db.insert_post(c, topic="x", format="carousel", scheduled_at=first[0], status="approved")
        second = learning.pick_slots(cfg, c, 1, "feed")
    assert first != second


def test_assignments_favor_winners(cfg):
    with db.connect(cfg.db_path) as c:
        for i in range(6):
            add_published(c, cfg, 12, area="saúde", style="mito vs verdade", saved=80, days_ago=i + 1)
            add_published(c, cfg, 12, area="trabalhista", style="erro comum", saved=1, days_ago=i + 1)
        asg = learning.choose_assignments(cfg, c, 400, random.Random(3))
    assert sum(a == "saúde" for a, _ in asg) > sum(a == "trabalhista" for a, _ in asg)
    assert sum(s == "mito vs verdade" for _, s in asg) > sum(s == "erro comum" for _, s in asg)


def test_adaptive_mix_moves_slot_to_better_format(cfg):
    with db.connect(cfg.db_path) as c:
        for i in range(5):
            add_published(c, cfg, 12, fmt="reel", saved=100, days_ago=i + 1)
            add_published(c, cfg, 12, fmt="carousel", saved=10, days_ago=i + 1)
        mix = learning.adaptive_mix(cfg, c)
    assert mix["reel"] == 3 and mix["carousel"] == 2


def _story(cfg, frames, hook="Dica"):
    with db.connect(cfg.db_path) as c:
        return db.insert_post(c, topic="s", area="saúde", format="story", hook=hook, slides_json=frames, caption="",
                              hashtags="", scheduled_at="2020-01-01T00:00:00+00:00")


def get(cfg, pid):
    with db.connect(cfg.db_path) as c:
        return db.get_post(c, pid)


def test_story_without_caption_is_approved_and_rendered(cfg):
    pid = _story(cfg, [{"title": "Você sabia?", "body": "Negativa de plano deve ser por escrito."}])
    assert pipeline.process(cfg, pid, OkLLM()) == "approved"
    assert get(cfg, pid)["image_paths_json"][0].endswith("story_01.jpg")


def test_story_with_promise_is_blocked(cfg):
    pid = _story(cfg, [{"title": "Resultado garantido", "body": "x"}])
    assert pipeline.process(cfg, pid, OkLLM()) == "blocked"


def test_hook_is_now_checked(cfg):
    pid = _story(cfg, [{"title": "ok", "body": "ok"}], hook="Sou o melhor advogado")
    assert pipeline.process(cfg, pid, OkLLM()) == "blocked"


class FakeIG:
    def __init__(self, cfg): self.calls = []
    def publish_story(self, p): self.calls.append(("story", p)); return "S1"
    def publish_images(self, paths, caption, alt=""): self.calls.append(("feed", paths)); return "F1"


def test_publish_feed_queues_teaser_story(cfg, monkeypatch):
    monkeypatch.setattr(pipeline, "InstagramClient", FakeIG)
    with db.connect(cfg.db_path) as c:
        pid = db.insert_post(c, topic="plano", area="saúde", format="carousel", status="approved", hook="Plano negou?",
                             slides_json=[], caption="c", hashtags="#x", image_paths_json=["a.jpg"], hook_style="pergunta direta",
                             scheduled_at="2020-01-01T00:00:00+00:00")
    assert pipeline.publish_due(cfg) == [pid]
    with db.connect(cfg.db_path) as c:
        teaser = c.execute("SELECT * FROM posts WHERE topic LIKE 'teaser:%'").fetchone()
    assert teaser["format"] == "story" and teaser["status"] == "approved"
    assert teaser["scheduled_at"] > db.now_iso()


def test_teasers_do_not_pollute_learning(cfg):
    with db.connect(cfg.db_path) as c:
        add_published(c, cfg, 12, fmt="story", topic="teaser:1", saved=0)
        assert learning.post_scores(c) == []


def test_plan_week_fills_only_missing(cfg, monkeypatch):
    cfg = replace(cfg, week_mix="carousel:2,story:3", eleven_key="", heygen_key="")
    calls = []

    def fake(cfg_, fmt, n, llm):
        calls.append((fmt, n))
        return []
    monkeypatch.setattr(pipeline, "LLM", lambda c: OkLLM())
    monkeypatch.setattr(pipeline, "_plan_format", fake)
    soon = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(timespec="seconds")
    with db.connect(cfg.db_path) as c:
        db.insert_post(c, topic="a", format="carousel", scheduled_at=soon, status="approved")
        for _ in range(3):
            db.insert_post(c, topic="s", format="story", scheduled_at=soon, status="approved")
    pipeline.plan_week(cfg)
    assert calls == [("carousel", 1)]


def test_plan_week_skips_reels_without_credentials(cfg, monkeypatch):
    cfg = replace(cfg, week_mix="reel:2", eleven_key="", heygen_key="")
    monkeypatch.setattr(pipeline, "LLM", lambda c: OkLLM())
    monkeypatch.setattr(pipeline, "_plan_format", lambda *a: pytest.fail("não deveria planejar reels"))
    assert pipeline.plan_week(cfg) == {}


def test_tick_plans_once_per_12h(cfg, monkeypatch):
    calls = []
    monkeypatch.setattr(pipeline, "publish_due", lambda c: [])
    monkeypatch.setattr(pipeline, "collect_insights", lambda c: 0)
    monkeypatch.setattr(pipeline, "plan_week", lambda c: calls.append(1) or {})
    pipeline.tick(cfg)
    pipeline.tick(cfg)
    assert calls == [1]


def test_report_contents(cfg, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with db.connect(cfg.db_path) as c:
        add_published(c, cfg, 19, saved=40, style="mito vs verdade", days_ago=1)
        c.execute("INSERT INTO conversations (ig_user, status, created_at) VALUES ('u','handoff',?)", (db.now_iso(),))
    text = report.weekly(cfg)
    assert "19h" in text and "mito vs verdade" in text and "repassadas a você: 1" in text
    assert list((tmp_path / "data/reports").glob("*.md"))


class SpyLLM:
    def __init__(self): self.seen = ""
    def json(self, system, user, **k):
        self.seen = user
        return {"approved": True, "issues": []}


def test_judge_receives_the_hook(cfg):
    pid = _story(cfg, [{"title": "ok", "body": "ok"}], hook="Gancho que o juiz precisa ver")
    spy = SpyLLM()
    pipeline.process(cfg, pid, spy)
    assert "Gancho que o juiz precisa ver" in spy.seen


def test_winners_carry_hook_text_and_style(cfg):
    with db.connect(cfg.db_path) as c:
        pid = add_published(c, cfg, 12, saved=50, style="mito vs verdade")
        c.execute("UPDATE posts SET hook='Mito: plano pode negar tudo' WHERE id=?", (pid,))
        winners = pipeline.top_performers(c)
    assert winners[0]["hook"] == "Mito: plano pode negar tudo" and winners[0]["style"] == "mito vs verdade"
    from robo_ig.generator import build_user_prompt
    prompt = build_user_prompt(1, [("saúde", "pergunta direta")], [], winners)
    assert "Mito: plano pode negar tudo" in prompt and "mito vs verdade" in prompt


def test_review_all_is_default_and_blocks_auto_publish(cfg):
    assert Config().review_all is True
    strict = replace(cfg, review_all=True)
    pid = _story(strict, [{"title": "Você sabia?", "body": "Negativa de plano deve ser por escrito."}])
    assert pipeline.process(strict, pid, OkLLM()) == "needs_review"
    pipeline.set_status(strict, pid, "approved")
    assert get(strict, pid)["status"] == "approved"
