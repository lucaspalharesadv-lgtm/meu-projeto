import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from . import compliance, db
from .config import Config
from .generator import generate_posts, generate_reels
from .instagram import InstagramClient, InstagramError
from .llm import LLM
from .notify import notify
from .render import render_post
from .video import produce_reel


def top_performers(conn, limit: int = 5) -> list[dict]:
    rows = conn.execute("""
        SELECT p.area, p.topic, p.hook,
               MAX(m.saved) * 3.0 + MAX(m.shares) * 4.0 + MAX(m.comments) * 2.0 + MAX(m.likes) AS score
        FROM posts p JOIN metrics m ON m.post_id = p.id
        GROUP BY p.id ORDER BY score DESC LIMIT ?""", (limit,)).fetchall()
    return [dict(r) for r in rows]


def next_slots(cfg: Config, conn, n: int) -> list[str]:
    tz = ZoneInfo(cfg.timezone)
    last = conn.execute("SELECT MAX(scheduled_at) FROM posts").fetchone()[0]
    cursor = max(datetime.now(tz), datetime.fromisoformat(last).astimezone(tz) if last else datetime.now(tz))
    slots = []
    day = cursor.date()
    while len(slots) < n:
        for h in sorted(cfg.post_hours):
            slot = datetime(day.year, day.month, day.day, h, 0, tzinfo=tz)
            if slot > cursor and len(slots) < n:
                slots.append(slot.astimezone(timezone.utc).isoformat(timespec="seconds"))
        day += timedelta(days=1)
    return slots


def plan(cfg: Config, n: int) -> list[int]:
    llm = LLM(cfg)
    with db.connect(cfg.db_path) as conn:
        recent = [r[0] for r in conn.execute("SELECT topic FROM posts ORDER BY id DESC LIMIT 40")]
        drafts = generate_posts(cfg, llm, n, recent, top_performers(conn))
        slots = next_slots(cfg, conn, len(drafts))
        ids = []
        for d, slot in zip(drafts, slots):
            ids.append(db.insert_post(
                conn, topic=d["topic"], area=d.get("area"), format=d["format"], hook=d["hook"],
                slides_json=d["slides"], caption=d["caption"], hashtags=" ".join(f"#{h.lstrip('#')}" for h in d["hashtags"]),
                alt_text=d.get("alt_text", ""), scheduled_at=slot))
    for pid in ids:
        process(cfg, pid, llm)
    return ids


def plan_reels(cfg: Config, n: int) -> list[int]:
    llm = LLM(cfg)
    with db.connect(cfg.db_path) as conn:
        recent = [r[0] for r in conn.execute("SELECT topic FROM posts ORDER BY id DESC LIMIT 40")]
        drafts = generate_reels(cfg, llm, n, recent, top_performers(conn))
        slots = next_slots(cfg, conn, len(drafts))
        ids = [db.insert_post(conn, topic=d["topic"], area=d.get("area"), format="reel", hook=d["hook"],
                              slides_json=[{"title": d["hook"], "body": d["script"]}], caption=d["caption"],
                              hashtags=" ".join(f"#{h.lstrip('#')}" for h in d["hashtags"]), scheduled_at=slot)
               for d, slot in zip(drafts, slots)]
    for pid in ids:
        process(cfg, pid, llm)
    return ids


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
        findings = compliance.check_post(post["caption"], post["slides_json"], cfg.oab)
        if not any(f.severity == compliance.BLOCK for f in findings):
            findings += compliance.judge_with_llm(llm, post["caption"], post["slides_json"])
        decision = compliance.decide(findings)
        status = {"auto": "approved", "review": "needs_review", "block": "blocked"}[decision]
        if post["format"] == "reel":
            # vídeo custa dinheiro: só é gerado quando o roteiro está liberado
            db.update_post(conn, post_id, status="needs_review" if decision == "auto" else status,
                           compliance_json=compliance.to_dicts(findings))
            if decision == "auto":
                status = "approved" if _make_video(cfg, conn, post) else "failed"
        else:
            paths = render_post(cfg, post_id, post["hook"], post["slides_json"], post["format"])
            db.update_post(conn, post_id, status=status, compliance_json=compliance.to_dicts(findings),
                           image_paths_json=paths)
    if decision != "auto":
        motivos = "; ".join(f"{f.rule}: {f.excerpt or f.message}" for f in findings[:4])
        notify(cfg, f"Post #{post_id} ({post['topic']}) -> {status}. {motivos}")
    return status


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
                else:
                    media_id = client.publish_images(post["image_paths_json"], caption, post["alt_text"] or "")
            except (InstagramError, OSError) as e:
                db.update_post(conn, pid, status="failed", error=str(e))
                notify(cfg, f"Falha ao publicar post #{pid}: {e}")
                continue
            db.update_post(conn, pid, status="published", ig_media_id=media_id, published_at=db.now_iso())
            published.append(pid)
    return published


def collect_insights(cfg: Config) -> int:
    client = InstagramClient(cfg)
    count = 0
    with db.connect(cfg.db_path) as conn:
        rows = conn.execute("""SELECT id, ig_media_id FROM posts WHERE status='published'
                               AND published_at >= datetime('now','-30 days')""").fetchall()
        for pid, media_id in rows:
            try:
                m = client.insights(media_id)
            except InstagramError:
                continue
            conn.execute("INSERT INTO metrics (post_id, fetched_at, reach, likes, comments, saved, shares) "
                         "VALUES (?,?,?,?,?,?,?)", (pid, db.now_iso(), m.get("reach"), m.get("likes"),
                                                    m.get("comments"), m.get("saved"), m.get("shares")))
            count += 1
    return count


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
