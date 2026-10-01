import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic TEXT NOT NULL,
  area TEXT,
  format TEXT NOT NULL DEFAULT 'carousel',
  status TEXT NOT NULL DEFAULT 'draft',
  hook TEXT,
  slides_json TEXT,
  caption TEXT,
  hashtags TEXT,
  alt_text TEXT,
  compliance_json TEXT,
  image_paths_json TEXT,
  scheduled_at TEXT,
  published_at TEXT,
  ig_media_id TEXT,
  error TEXT,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS metrics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL REFERENCES posts(id),
  fetched_at TEXT NOT NULL,
  reach INTEGER, likes INTEGER, comments INTEGER, saved INTEGER, shares INTEGER
);
CREATE TABLE IF NOT EXISTS conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ig_user TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'bot',
  area TEXT, summary TEXT, lead_json TEXT,
  bot_replies INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conv_id INTEGER NOT NULL REFERENCES conversations(id),
  direction TEXT NOT NULL, text TEXT NOT NULL,
  mid TEXT UNIQUE, at TEXT NOT NULL
);
"""

JSON_COLS = {"slides_json", "compliance_json", "image_paths_json"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def connect(path: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_post(conn, **fields) -> int:
    fields.setdefault("created_at", now_iso())
    for k in JSON_COLS & fields.keys():
        fields[k] = json.dumps(fields[k], ensure_ascii=False)
    cols = ", ".join(fields)
    marks = ", ".join("?" for _ in fields)
    return conn.execute(f"INSERT INTO posts ({cols}) VALUES ({marks})", list(fields.values())).lastrowid


def update_post(conn, post_id: int, **fields) -> None:
    for k in JSON_COLS & fields.keys():
        fields[k] = json.dumps(fields[k], ensure_ascii=False)
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE posts SET {sets} WHERE id=?", [*fields.values(), post_id])


def get_post(conn, post_id: int) -> dict:
    row = conn.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
    if row is None:
        raise KeyError(f"post {post_id} não existe")
    post = dict(row)
    for k in JSON_COLS:
        post[k] = json.loads(post[k]) if post[k] else None
    return post
