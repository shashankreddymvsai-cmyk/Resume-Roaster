import sqlite3, json, os
from datetime import datetime

DB_PATH = os.getenv("RESUME_ROASTED_DB", "resume_roasted.db")

def _conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            score INTEGER NOT NULL,
            report_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_reports_user ON reports(user_id, created_at DESC)")

def save_report(user_id, role, report):
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO reports(user_id,role,score,report_json,created_at) VALUES(?,?,?,?,?)",
            (user_id, role, int(report.get("overall_score",0)), json.dumps(report,ensure_ascii=False), datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        return cur.lastrowid

def get_reports(user_id, limit=30):
    with _conn() as conn:
        rows = conn.execute("SELECT * FROM reports WHERE user_id=? ORDER BY id DESC LIMIT ?",(user_id,int(limit))).fetchall()
        return [dict(r) for r in rows]

def delete_report(user_id, report_id):
    with _conn() as conn:
        conn.execute("DELETE FROM reports WHERE user_id=? AND id=?",(user_id,int(report_id)))
