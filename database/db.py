import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "news.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        url TEXT UNIQUE,

        source TEXT,

        published_date TEXT,

        content TEXT,

        status TEXT DEFAULT 'NEW',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()

    print("Database initialized successfully.")