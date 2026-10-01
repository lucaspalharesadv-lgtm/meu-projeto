import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from . import compliance, db, learning
from .config import Config
from .generator import generate_posts, generate_reels, generate_stories
from .instagram import InstagramClient, InstagramError
from .llm import LLM
from .notify import notify
from .render import render_post, render_story
from .video import produce_reel

TEASER_PREFIX = "teaser:"


def top_performers(conn, limit: int = 5) -> list[dict]:
    rows = sorted(learning.post_scores(conn), key=lambda r: r["score"], reverse=True)[:limit]
    return [{"area": r["area"], "topic": r["topic"], "hook": r["hook"] or "", "style": r["hook_style"] or ""} for r in rows]


def _tags(d: dict) -> str:
    return " ".join(f"#{h.lstrip('#')}" for h in d.get("hashtags", []))


def _plan_format(cfg: Config, fmt: str, n: int, llm: LLM) -> list[int]:
    """Gera n itens do formato (carousel | reel | story), escolhe horários pelo aprendizado e passa pelo filtro."""
    with db.connect(cfg.db_path) as conn:
        recent = [r[0] for r in conn.execute("SELECT topic FROM posts ORDER BY id DESC LIMIT 40")]
        winners, asg = top_performers(conn), learning.choose_assignments(cfg, conn, n)
        gen = {"story": generate_stories, "reel": generate_reels}.get(fmt, generate_posts)
        drafts = gen(cfg, llm, n, recent, winners, asg)
        slots = learning.pick_slots(cfg, conn, len(drafts), "story" if fmt == "story" else "feed")
        ids = []
        for d, slot in zip(drafts, slots):
            common = dict(topic=d["topic"], area=d.get("area"), hook_style=d.get("hook_style"), scheduled_at=slot)
            if fmt == "story":
                ids.append(db.insert_post(conn, format="story", hook=d["frames"][0]["title"], slides_json=d["frames"],
                                          caption="", hashtags="", **common))
            elif fmt == "reel":
                ids.append(db.insert_post(conn, format="reel", hook=d["hook"], caption=d["caption"], hashtags=_tags(d),
                                          slides_json=[{"title": d["hook"], "body": d["script"]}], **common))
            else:
                ids.append(db.insert_post(conn, format=d["format"], hook=d["hook"], slides_json=d["slides"],
                                          caption=d["caption"], hashtags=_tags(d), alt_text=d.get("alt_text", ""),
                                          **common))
    for pid in ids:
        process(cfg, pid, llm)
    return ids


def plan(cfg: Config, n: int) -> list[int]:
    return _plan_format(cfg, "carousel", n, LLM(cfg))


def plan_reels(cfg: Config, n: int) -> list[int]:
    return _plan_format(cfg, "reel", n, LLM(cfg))


def plan_stories(cfg: Config, n: int) -> list[int]:
    return _plan_format(cfg, "story", n, LLM(cfg))


def plan_week(cfg: Config) -> dict[str, list[int]]:
    """Mantém a fila dos próximos 7 dias cheia, conforme WEEK_MIX (ajustado pelo que performa)."""
    llm = LLM(cfg)
    with db.connect(cfg.db_path) as conn:
        mix = learning.adaptive_mix(cfg, conn)
        now = datetime.now(timezone.utc)
        queued: dict[str, int] = {}
        for fmt, c in conn.execute(
                "SELECT format, COUNT(*) FROM posts WHERE scheduled_at > ? AND scheduled_at <= ? AND topic NOT LIKE ? "
                "AND status NOT IN ('rejected','blocked','failed') GROUP BY format",
                (now.isoformat(timespec="seconds"), (now + timedelta(days=7)).isoformat(timespec="seconds"),
                 TEASER_PREFIX + "%")):
            key = "carousel" if fmt == "single" else fmt
            queued[key] = queued.get(key, 0) + c
    created = {}
    for fmt, target in mix.items():
        need = target - queued.get(fmt, 0)
        if need <= 0:
            continue
        if fmt == "reel" and not (cfg.eleven_key and cfg.heygen_key):
            continue
        created[fmt] = _plan_format(cfg, fmt, need, llm)
    return created


def _make_video(cfg: Config, conn, post: dict) -> bool:
    try:
        path = produce_reel(cfg, post["id"], post["slides_json"][0]["body"])
    except Exception as e:
        db.update_post(conn, post["id"], status="failed", error=f"vídeo: {e}")
        notify(cfg, f"Falha ao gerar vídeo do post #{post['id']}: {e}")
        return False
    db.update_post(conn, post["id"], status="approved", image_paths_json=[path])
    return True


def process(cfg: Config, post_id: int, llm: LLM | None = None) -> str:
    llm = llm or LLM(cfg)
    with db.connect(cfg.db_path) as conn:
        post = db.get_post(conn, post_id)
        story = post["format"] == "story"
        findings = compliance.check_post(post["caption"], post["slides_json"], cfg.oab, post["hook"] or "",
                                         require_id=not story)
        if not any(f.severity == compliance.BLOCK for f in findings):
            findings += compliance.judge_with_llm(llm, post["caption"], post["slides_json"], post["hook"] or "")
        decision = compliance.decide(findings)
        if decision == "auto" and cfg.review_all:
            decision = "review"
        status = {"auto": "approved", "review": "needs_review", "block": "blocked"}[decision]
        if post["format"] == "reel":
            # vídeo custa dinheiro: só é gerado quando o roteiro está liberado
            db.update_post(conn, post_id, status="needs_review" if decision == "auto" else status,
                           compliance_json=compliance.to_dicts(findings))
            if decision == "auto":
                status = "approved" if _make_video(cfg, conn, post) else "failed"
        else:
            paths = (render_story(cfg, post_id, post["slides_json"]) if story else
                     render_post(cfg, post_id, post["hook"], post["slides_json"], post["format"]))
            db.update_post(conn, post_id, status=status, compliance_json=compliance.to_dicts(findings),
                           image_paths_json=paths)
    if decision != "auto":
        motivos = "; ".join(f"{f.rule}: {f.excerpt or f.message}" for f in findings[:4]) or "aguardando sua aprovação (REVIEW_ALL)"
        notify(cfg, f"Post #{post_id} ({post['topic']}) -> {status}. {motivos}")
    return status


def _queue_teaser(cfg: Config, conn, post: dict) -> None:
    """Story avisando que saiu post novo no feed (promoção do próprio conteúdo, sem apelo comercial)."""
    frames = [{"title": post["hook"], "body": "Acabou de sair no feed. Salve para consultar depois."}]
    if compliance.check_post("", frames, "", post["hook"] or "", require_id=False):
        return
    when = (datetime.now(timezone.utc) + timedelta(minutes=20)).isoformat(timespec="seconds")
    pid = db.insert_post(conn, topic=f"{TEASER_PREFIX}{post['id']}", area=post["area"], format="story",
                         hook=post["hook"], slides_json=frames, caption="", hashtags="", scheduled_at=when,
                         status="approved", compliance_json=[], hook_style=post["hook_style"])
    db.update_post(conn, pid, image_paths_json=render_story(cfg, pid, frames))


def publish_due(cfg: Config) -> list[int]:
    client = InstagramClient(cfg)
    published = []
    with db.connect(cfg.db_path) as conn:
        due = conn.execute("SELECT id FROM posts WHERE status='approved' AND scheduled_at <= ? ORDER BY scheduled_at",
                           (db.now_iso(),)).fetchall()
        for (pid,) in due:
            post = db.get_post(conn, pid)
            caption = f"{post['caption']}\n\n{post['hashtags']}"
            try:
                if post["format"] == "reel":
                    media_id = client.publish_reel(post["image_paths_json"][0], caption)
                elif post["format"] == "story":
                    media_id = [client.publish_story(p) for p in post["image_paths_json"]][0]
                else:
                    media_id = client.publish_images(post["image_paths_json"], caption, post["alt_text"] or "")
            except (InstagramError, OSError) as e:
                db.update_post(conn, pid, status="failed", error=str(e))
                notify(cfg, f"Falha ao publicar post #{pid}: {e}")
                continue
            db.update_post(conn, pid, status="published", ig_media_id=media_id, published_at=db.now_iso())
            published.append(pid)
            if post["format"] != "story":
                _queue_teaser(cfg, conn, post)
    return published


def collect_insights(cfg: Config) -> int:
    """Feed: 1x/dia por 30 dias. Stories: a cada 3h enquanto estiverem no ar (métricas somem depois)."""
    client = InstagramClient(cfg)
    now = datetime.now(timezone.utc)
    count = 0
    with db.connect(cfg.db_path) as conn:
        rows = conn.execute("""SELECT p.id, p.ig_media_id, p.format,
                   (SELECT MAX(fetched_at) FROM metrics WHERE post_id = p.id) AS last
                   FROM posts p WHERE p.status='published' AND p.ig_media_id IS NOT NULL AND p.published_at >= ?""",
                            ((now - timedelta(days=30)).isoformat(timespec="seconds"),)).fetchall()
        for pid, media_id, fmt, last in rows:
            story = fmt == "story"
            age_h = (now - datetime.fromisoformat(last)).total_seconds() / 3600 if last else float("inf")
            pub = datetime.fromisoformat(conn.execute("SELECT published_at FROM posts WHERE id=?", (pid,)).fetchone()[0])
            if (story and ((now - pub).total_seconds() > 23 * 3600 or age_h < 3)) or (not story and age_h < 20):
                continue
            try:
                m = client.insights(media_id, story=story)
            except InstagramError:
                continue
            conn.execute("INSERT INTO metrics (post_id, fetched_at, reach, likes, comments, saved, shares) "
                         "VALUES (?,?,?,?,?,?,?)", (pid, db.now_iso(), m.get("reach"), m.get("likes"),
                                                    m.get("comments"), m.get("saved"), m.get("shares")))
            count += 1
    return count


def tick(cfg: Config) -> dict:
    """Um ciclo do piloto automático. Rode no cron a cada 15 minutos."""
    from . import report
    result = {"published": publish_due(cfg), "metrics": 0, "planned": {}, "report": False}
    try:
        result["metrics"] = collect_insights(cfg)
    except Exception as e:
        notify(cfg, f"Falha ao coletar métricas: {e}")
    with db.connect(cfg.db_path) as conn:
        plan_due = db.kv_age_hours(conn, "plan") > 12
        if plan_due:
            db.kv_touch(conn, "plan")
    if plan_due:
        try:
            result["planned"] = plan_week(cfg)
        except Exception as e:
            notify(cfg, f"Falha ao planejar a semana: {e}")
    local = datetime.now(ZoneInfo(cfg.timezone))
    with db.connect(cfg.db_path) as conn:
        report_due = local.weekday() == 6 and local.hour >= 20 and db.kv_age_hours(conn, "report") > 100
        if report_due:
            db.kv_touch(conn, "report")
    if report_due:
        notify(cfg, report.weekly(cfg)[:3500])
        result["report"] = True
    return result


def set_status(cfg: Config, post_id: int, status: str) -> None:
    with db.connect(cfg.db_path) as conn:
        post = db.get_post(conn, post_id)
        if status == "approved" and post["format"] == "reel" and not post["image_paths_json"]:
            _make_video(cfg, conn, post)
        else:
            db.update_post(conn, post_id, status=status)


def show(cfg: Config, post_id: int) -> str:
    with db.connect(cfg.db_path) as conn:
        post = db.get_post(conn, post_id)
    return json.dumps(post, ensure_ascii=False, indent=2)
