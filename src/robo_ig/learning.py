"""Aprendizado: quais horários, estilos de gancho, áreas e formatos geram mais engajamento neste perfil.

Pontuação do post = (salvamentos*3 + compartilhamentos*4 + comentários*2 + curtidas) / alcance, com a última coleta de métricas.
Estimativas são encolhidas para a média geral (poucos dados não decidem sozinhos) e uma fração dos horários/estilos é
sorteada (EXPLORE) para continuar descobrindo o que ainda não foi testado.
"""
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from .config import Config
from .generator import HOOK_STYLES

DEFAULT_HOUR_ORDER = [12, 19, 20, 18, 21, 8, 7, 13, 17, 22, 11, 14, 15, 16, 9, 10]
SHRINK = 2.0
FEED, STORY = ("carousel", "single", "reel"), ("story",)


def kind_of(fmt: str) -> str:
    return "story" if fmt == "story" else "feed"


def post_scores(conn) -> list[dict]:
    rows = conn.execute("""
        SELECT p.id, p.area, p.hook, p.hook_style, p.format, p.published_at, p.topic,
               m.reach, m.likes, m.comments, m.saved, m.shares
        FROM posts p JOIN metrics m ON m.id = (SELECT MAX(id) FROM metrics WHERE post_id = p.id)
        WHERE p.status='published' AND m.reach > 0 AND p.topic NOT LIKE 'teaser:%'""").fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["score"] = ((d["saved"] or 0) * 3 + (d["shares"] or 0) * 4 + (d["comments"] or 0) * 2 + (d["likes"] or 0)) / d["reach"]
        out.append(d)
    return out


def _shrunk(scores: list[float], prior: float) -> float:
    return (sum(scores) + SHRINK * prior) / (len(scores) + SHRINK)


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def window(cfg: Config) -> list[int]:
    return list(range(cfg.window_start, cfg.window_end + 1))


def hour_table(cfg: Config, conn, kind: str) -> dict[int, tuple[float, int]]:
    """hora local -> (pontuação encolhida, nº de posts) para o tipo 'feed' ou 'story'."""
    tz = ZoneInfo(cfg.timezone)
    rows = [r for r in post_scores(conn) if kind_of(r["format"]) == kind and r["published_at"]]
    prior = _mean([r["score"] for r in rows])
    by_hour = defaultdict(list)
    for r in rows:
        h = datetime.fromisoformat(r["published_at"]).astimezone(tz).hour
        by_hour[h].append(r["score"])
    return {h: (_shrunk(by_hour[h], prior) if by_hour[h] else prior, len(by_hour[h])) for h in window(cfg)}


def rank_hours(cfg: Config, conn, kind: str) -> list[int]:
    table = hour_table(cfg, conn, kind)
    order = {h: i for i, h in enumerate(DEFAULT_HOUR_ORDER)}
    return sorted(table, key=lambda h: (-table[h][0], order.get(h, 99)))


def pick_slots(cfg: Config, conn, n: int, kind: str, rng: random.Random | None = None, min_gap: int = 3) -> list[str]:
    """Próximos n horários (UTC ISO) nos melhores horários locais, respeitando o limite diário e o intervalo mínimo."""
    rng = rng or random.Random()
    tz = ZoneInfo(cfg.timezone)
    now = datetime.now(tz) + timedelta(minutes=10)
    taken = defaultdict(list)
    for sched, fmt in conn.execute("SELECT scheduled_at, format FROM posts WHERE scheduled_at IS NOT NULL "
                                   "AND status NOT IN ('rejected','blocked','failed')"):
        t = datetime.fromisoformat(sched).astimezone(tz)
        if kind_of(fmt) == kind:
            taken[t.date()].append(t.hour)
    ranked, per_day = rank_hours(cfg, conn, kind), (cfg.stories_per_day if kind == "story" else cfg.feed_per_day)
    slots, day = [], now.date()
    for _ in range(90):
        while len(taken[day]) < per_day and len(slots) < n:
            hours = rng.sample(window(cfg), k=len(window(cfg))) if rng.random() < cfg.explore else ranked
            pick = next((h for h in hours if datetime(day.year, day.month, day.day, h, tzinfo=tz) > now
                         and all(abs(h - u) >= min_gap for u in taken[day])), None)
            if pick is None:
                break
            taken[day].append(pick)
            slots.append(datetime(day.year, day.month, day.day, pick, tzinfo=tz).astimezone(timezone.utc)
                         .isoformat(timespec="seconds"))
        if len(slots) >= n:
            break
        day += timedelta(days=1)
    return sorted(slots)


def choose_assignments(cfg: Config, conn, n: int, rng: random.Random | None = None) -> list[tuple[str, str]]:
    """(área, estilo de gancho) para cada item: favorece o que performa, sem abandonar o resto."""
    rng = rng or random.Random()
    rows = post_scores(conn)
    prior = _mean([r["score"] for r in rows])

    def weights(options, field):
        out = []
        for o in options:
            sc = [r["score"] for r in rows if r[field] == o]
            out.append(max(_shrunk(sc, prior), 1e-6) + (0.25 * prior if prior else 1.0) if rows else 1.0)
        return out

    areas = rng.choices(cfg.areas, weights=weights(cfg.areas, "area"), k=n)
    styles = rng.choices(HOOK_STYLES, weights=weights(HOOK_STYLES, "hook_style"), k=n)
    return list(zip(areas, styles))


def adaptive_mix(cfg: Config, conn) -> dict[str, int]:
    """Move 1 vaga semanal do formato de feed que menos engaja para o que mais engaja (>=5 posts de cada, >30% de diferença)."""
    mix = dict(cfg.mix)
    rows = post_scores(conn)
    avg = {f: _mean([r["score"] for r in rows if r["format"] == f]) for f in ("carousel", "reel")}
    cnt = {f: sum(1 for r in rows if r["format"] == f) for f in avg}
    if min(cnt.values()) >= 5 and mix.get("carousel", 0) and mix.get("reel", 0):
        best, worst = sorted(avg, key=avg.get, reverse=True)
        if avg[worst] > 0 and avg[best] > 1.3 * avg[worst] and mix[worst] > 1:
            mix[best] += 1
            mix[worst] -= 1
    return mix
