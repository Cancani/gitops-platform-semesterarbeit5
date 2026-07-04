"""SQLite Datenzugriff für die Preisdaten.
"""

import os
import sqlite3
from contextlib import contextmanager

DATABASE_PATH = os.getenv("DATABASE_PATH", "/tmp/prices.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Erstellt die Tabelle und den Index, falls noch nicht vorhanden."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT NOT NULL,
                source TEXT NOT NULL,
                image_url TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_item_time "
            "ON prices(item_name, timestamp)"
        )


def insert_prices(entries) -> None:
    """Speichert mehrere Preisdatenpunkte."""
    with get_connection() as conn:
        conn.executemany(
            "INSERT INTO prices "
            "(item_name, price, currency, source, image_url, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                (e.item_name, e.price, e.currency, e.source, e.image_url,
                 e.timestamp.isoformat())
                for e in entries
            ],
        )


def get_latest_prices() -> list[dict]:
    """Liefert den jeweils neusten Preis pro Objekt."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT p.item_name, p.price, p.currency, p.source, p.image_url, p.timestamp
            FROM prices p
            INNER JOIN (
                SELECT item_name, MAX(timestamp) AS max_ts
                FROM prices
                GROUP BY item_name
            ) latest
            ON p.item_name = latest.item_name AND p.timestamp = latest.max_ts
            ORDER BY p.item_name
            """
        ).fetchall()
        return [dict(r) for r in rows]


def get_price_history(item_name: str | None = None) -> list[dict]:
    """Liefert die Preishistorie, optional gefiltert nach Objekt."""
    with get_connection() as conn:
        if item_name:
            rows = conn.execute(
                "SELECT item_name, price, currency, source, image_url, timestamp "
                "FROM prices WHERE item_name = ? ORDER BY timestamp",
                (item_name,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT item_name, price, currency, source, image_url, timestamp "
                "FROM prices ORDER BY timestamp"
            ).fetchall()
        return [dict(r) for r in rows]


def check_connection() -> None:
    """Prüft, ob die Datenbank erreichbar ist (für Readiness Probe)."""
    with get_connection() as conn:
        conn.execute("SELECT 1")
