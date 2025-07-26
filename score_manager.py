import sqlite3

def init_db():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_score(score):
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (value) VALUES (?)", (score,))
    conn.commit()
    conn.close()

def get_best_score():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(value) FROM scores")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] is not None else 0