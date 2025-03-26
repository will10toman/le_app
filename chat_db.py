import sqlite3

DB_PATH = "leapp_chat.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                msg TEXT,
                timestamp TEXT
            )
        """)

def add_message(user, msg, timestamp):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO chat_messages (user, msg, timestamp) VALUES (?, ?, ?)", (user, msg, timestamp))

def get_messages(limit=50):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user, msg, timestamp FROM chat_messages ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
    return [{"user": r[0], "msg": r[1], "timestamp": r[2]} for r in rows]

def clear_chat():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM chat_messages")
