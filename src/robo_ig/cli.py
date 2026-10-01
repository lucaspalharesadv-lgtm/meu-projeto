import argparse

from . import db, pipeline
from .config import Config


def main() -> None:
    p = argparse.ArgumentParser(prog="robo-ig")
    sub = p.add_subparsers(dest="cmd", required=True)
    plan = sub.add_parser("plan", help="gera N posts, aplica filtro OAB, renderiza e agenda")
    plan.add_argument("-n", type=int, default=7)
    sub.add_parser("publish", help="publica os aprovados cujo horário chegou (rodar no cron a cada 15 min)")
    sub.add_parser("insights", help="coleta métricas dos posts publicados")
    sub.add_parser("serve", help="sobe o webhook de DMs e comentários (porta 8000)")
    sub.add_parser("list", help="lista a fila")
    for name, help_ in (("approve", "aprova post em revisão"), ("reject", "descarta post"), ("show", "mostra post")):
        sub.add_parser(name, help=help_).add_argument("id", type=int)
    sub.add_parser("reprocess", help="reaplica filtro e arte a um post").add_argument("id", type=int)
    a = p.parse_args()
    cfg = Config()

    if a.cmd == "serve":
        import uvicorn
        uvicorn.run("robo_ig.server:app", host="0.0.0.0", port=8000)
    elif a.cmd == "plan":
        for pid in pipeline.plan(cfg, a.n):
            print("criado", pid)
    elif a.cmd == "publish":
        print("publicados:", pipeline.publish_due(cfg))
    elif a.cmd == "insights":
        print("métricas coletadas:", pipeline.collect_insights(cfg))
    elif a.cmd == "list":
        with db.connect(cfg.db_path) as conn:
            for r in conn.execute("SELECT id, status, scheduled_at, area, topic FROM posts ORDER BY scheduled_at"):
                print(f"#{r['id']:<4} {r['status']:<13} {r['scheduled_at']}  [{r['area']}] {r['topic']}")
    elif a.cmd == "approve":
        pipeline.set_status(cfg, a.id, "approved")
    elif a.cmd == "reject":
        pipeline.set_status(cfg, a.id, "rejected")
    elif a.cmd == "show":
        print(pipeline.show(cfg, a.id))
    elif a.cmd == "reprocess":
        print(pipeline.process(cfg, a.id))


if __name__ == "__main__":
    main()
