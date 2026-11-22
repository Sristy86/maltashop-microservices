import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional

DB_PATH = Path("/tmp/orders.db")


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                idempotency_key TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                customer_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                amount REAL NOT NULL,
                correlation_id TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def get_order_by_idempotency_key(key: str) -> Optional[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM orders WHERE idempotency_key = ?",
            (key,),
        ).fetchone()
        return dict(row) if row else None


def save_order(order: Dict[str, Any]) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO orders (
                idempotency_key, order_id, customer_id, item_id,
                quantity, amount, correlation_id, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order["idempotency_key"],
                order["order_id"],
                order["customer_id"],
                order["item_id"],
                order["quantity"],
                order["amount"],
                order["correlation_id"],
                order["status"],
                order["created_at"],
            ),
        )
        conn.commit()
