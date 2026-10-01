import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from . import db, learning
from .config import Config


def _rank(rows, field, top=3):
    groups = defaultdict(list)
    for r in rows:
        if r[field]:
            groups[r[field]].append(r["score"])
    ranked = sorted(groups.items(), key=lambda kv: sum(kv[1]) / len(kv[1]), reverse=True)[:top]
    return [f"{k}: {sum(v) / len(v):.3f} ({len(v)} posts)" for k, v in ranked] or ["sem dados ainda"]


def weekly(cfg: Config, write: bool = True) -> str:
    tz = ZoneInfo(cfg.timezone)
    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=7)).isoformat(timespec="seconds")
    with db.connect(cfg.db_path) as conn:
        scored = learning.post_scores(conn)
        week = [r for r in scored if r["published_at"] and r["published_at"] >= since]
        pubs = conn.execute("SELECT format, COUNT(*) FROM posts WHERE status='published' AND published_at >= ? "
                            "AND topic NOT LIKE 'teaser:%' GROUP BY format", (since,)).fetchall()
        tot = conn.execute("""SELECT COALESCE(SUM(m.reach),0), COALESCE(SUM(m.likes),0), COALESCE(SUM(m.comments),0),
                  COALESCE(SUM(m.saved),0), COALESCE(SUM(m.shares),0) FROM posts p JOIN metrics m
                  ON m.id=(SELECT MAX(id) FROM metrics WHERE post_id=p.id) WHERE p.published_at >= ?""", (since,)).fetchone()
        convs = conn.execute("SELECT COUNT(*), COALESCE(SUM(status='handoff'),0), COALESCE(SUM(status='optout'),0) "
                             "FROM conversations WHERE created_at >= ?", (since,)).fetchone()
        queue = conn.execute("SELECT status, COUNT(*) FROM posts WHERE status IN ('approved','needs_review','failed','blocked') "
                             "GROUP BY status").fetchall()
        review = [r[0] for r in conn.execute("SELECT id FROM posts WHERE status='needs_review'")]
        mix = learning.adaptive_mix(cfg, conn)
        hours = {k: learning.hour_table(cfg, conn, k) for k in ("feed", "story")}

    def top_hours(kind):
        tbl = {h: v for h, v in hours[kind].items() if v[1] > 0}
        best = sorted(tbl.items(), key=lambda kv: kv[1][0], reverse=True)[:3]
        return ", ".join(f"{h}h ({n} posts)" for h, (_, n) in best) or "sem dados ainda"

    best_posts = sorted(week, key=lambda r: r["score"], reverse=True)[:3]
    lines = [
        f"# Relatório semanal - {(now - timedelta(days=7)).astimezone(tz):%d/%m} a {now.astimezone(tz):%d/%m/%Y}", "",
        "## Publicado", *([f"- {fmt}: {c}" for fmt, c in pubs] or ["- nada publicado"]), "",
        "## Resultado", f"- Alcance: {tot[0]} | Curtidas: {tot[1]} | Comentários: {tot[2]} | Salvamentos: {tot[3]} | Compartilhamentos: {tot[4]}", "",
        "## Melhores posts da semana", *([f"- #{r['id']} [{r['area']}] {r['topic']} (pontuação {r['score']:.3f})" for r in best_posts] or ["- sem dados ainda"]), "",
        "## O que está funcionando",
        f"- Melhores horários (feed): {top_hours('feed')}",
        f"- Melhores horários (stories): {top_hours('story')}",
        "- Estilos de gancho: " + "; ".join(_rank(scored, "hook_style")),
        "- Áreas: " + "; ".join(_rank(scored, "area")),
        "- Formatos: " + "; ".join(_rank(scored, "format")), "",
        "## Atendimento (DMs)", f"- Conversas novas: {convs[0]} | repassadas a você: {convs[1]} | pediram para parar: {convs[2]}", "",
        "## Fila e pendências", *([f"- {s}: {c}" for s, c in queue] or ["- fila vazia"]),
        f"- Aguardando sua aprovação: {', '.join('#' + str(i) for i in review) or 'nenhum'}", "",
        "## Ajuste automático", f"- Mix semanal atual: {mix}",
    ]
    text = "\n".join(lines)
    if write:
        os.makedirs("data/reports", exist_ok=True)
        with open(f"data/reports/{now.astimezone(tz):%Y-%m-%d}.md", "w", encoding="utf-8") as f:
            f.write(text)
    return text
