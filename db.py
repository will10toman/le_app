import sqlite3
import hashlib

DB_PATH = "data/users.db"

# === INIT ===
def init_user_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

# === PASSWORD ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# === AUTH ===
def save_user(email, username, password_hash):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                (email, username, password_hash)
            )
            conn.commit()
        return "Success"
    except sqlite3.IntegrityError as e:
        if "username" in str(e).lower():
            return "Username already exists"
        elif "email" in str(e).lower():
            return "Email already registered"
        else:
            return "Unknown error occurred"


def authenticate_user(username, password):
    password_hash = hash_password(password)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password_hash)
        )
        return cursor.fetchone() is not None
