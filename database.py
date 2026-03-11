import os
import sqlite3
from config import DB_PATH


def get_connection():
    """SQLite接続を返す（DBディレクトリは自動作成）。"""
    # DB保存先ディレクトリが無ければ作る。
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """ポイント管理テーブルを初期化する。"""
    conn = get_connection()
    cursor = conn.cursor()

    # ユーザーごとのポイント保持テーブルを作成する。
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_points (
        user_id INTEGER PRIMARY KEY,
        points INTEGER NOT NULL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_points(user_id: int, amount: int):
    """指定ユーザーにポイントを加算する。"""
    conn = get_connection()
    cursor = conn.cursor()

    # 既存ユーザーは加算、未登録ユーザーは新規作成する。
    cursor.execute("""
    INSERT INTO user_points (user_id, points)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET points = points + excluded.points
    """, (user_id, amount))

    conn.commit()
    conn.close()


def get_points(user_id: int) -> int:
    """指定ユーザーの現在ポイントを取得する。"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT points FROM user_points WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    # 未登録ユーザーは0ptとして扱う。
    if row is None:
        return 0
    return row[0]


def set_points(user_id: int, points: int):
    """指定ユーザーのポイントを上書き設定する。"""
    conn = get_connection()
    cursor = conn.cursor()

    # 既存ユーザーは上書き、未登録ユーザーは新規作成する。
    cursor.execute("""
    INSERT INTO user_points (user_id, points)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET points = excluded.points
    """, (user_id, points))

    conn.commit()
    conn.close()
