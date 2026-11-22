import sqlite3
from pathlib import Path
from typing import Any, Dict

DB_PATH = Path("/tmp/notifications.db")


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                order_id TEXT NOT NULL,
                customer_id TEXT NOT NULL,
                correlation_id TEXT NOT NULL,
                processed_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def is_event_processed(event_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT 1 FROM processed_events WHERE event_id = ?",
            (event_id,),
        ).fetchone()
        return row is not None


def record_processed_event(record: Dict[str, Any]) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO processed_events (
                event_id, event_type, order_id, customer_id,
                correlation_id, processed_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                record["event_id"],
                record["event_type"],
                record["order_id"],
                record["customer_id"],
                record["correlation_id"],
                record["processed_at"],
            ),
        )
        conn.commit()
      
