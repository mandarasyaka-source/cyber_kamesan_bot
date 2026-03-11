import os
import sqlite3
from config import DB_PATH


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_points (
        user_id INTEGER PRIMARY KEY,
        points INTEGER NOT NULL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_points(user_id: int, amount: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_points (user_id, points)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET points = points + excluded.points
    """, (user_id, amount))

    conn.commit()
    conn.close()


def get_points(user_id: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT points FROM user_points WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return 0
    return row[0]


def set_points(user_id: int, points: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_points (user_id, points)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET points = excluded.points
    """, (user_id, points))

    conn.commit()
    conn.close()