import os
import psycopg
from dotenv import load_dotenv
import json
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
def get_connection():
    return psycopg.connect(DATABASE_URL)
def get_cached_stats(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT stats, updated_at
        FROM stats_cache
        WHERE username = %s;
        """,
        (username,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row
def save_cached_stats(username, stats):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO stats_cache (username, stats, updated_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (username)
        DO UPDATE SET
            stats = EXCLUDED.stats,
            updated_at = CURRENT_TIMESTAMP;
        """,
        (username, json.dumps(stats))
    )

    conn.commit()

    cursor.close()
    conn.close()