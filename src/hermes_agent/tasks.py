from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any

from .db import dump_json, load_json, row_to_dict, transaction


PENDING = "pending"
RUNNING = "running"
DONE = "done"
FAILED = "failed"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskStore:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_task(
        self,
        title: str,
        *,
        kind: str = "generic",
        priority: int = 3,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = payload or {}
        now = utc_now()
        task_id = str(uuid.uuid4())
        self.conn.execute(
            """
            INSERT INTO tasks(id, title, kind, status, priority, payload, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (task_id, title, kind, PENDING, priority, dump_json(payload), now, now),
        )
        self.conn.commit()
        return self.get_task(task_id)

    def get_task(self, task_id: str) -> dict[str, Any]:
        row = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            raise ValueError(f"Task not found: {task_id}")
        return self._deserialize(row_to_dict(row) or {})

    def list_tasks(self, *, status: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        if status:
            rows = self.conn.execute(
                """
                SELECT * FROM tasks
                WHERE status = ?
                ORDER BY priority ASC, datetime(created_at) ASC
                LIMIT ?
                """,
                (status, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT * FROM tasks
                ORDER BY
                  CASE status
                    WHEN 'running' THEN 0
                    WHEN 'pending' THEN 1
                    WHEN 'failed' THEN 2
                    ELSE 3
                  END,
                  priority ASC,
                  datetime(created_at) ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [self._deserialize(row_to_dict(r) or {}) for r in rows]

    def claim_next_pending(self) -> dict[str, Any] | None:
        with transaction(self.conn):
            row = self.conn.execute(
                """
                SELECT id FROM tasks
                WHERE status = ?
                ORDER BY priority ASC, datetime(created_at) ASC
                LIMIT 1
                """,
                (PENDING,),
            ).fetchone()
            if row is None:
                return None

            task_id = row["id"]
            self.conn.execute(
                """
                UPDATE tasks
                SET status = ?, updated_at = ?
                WHERE id = ? AND status = ?
                """,
                (RUNNING, utc_now(), task_id, PENDING),
            )
        return self.get_task(task_id)

    def complete_task(self, task_id: str, result: dict[str, Any] | None = None) -> dict[str, Any]:
        result = result or {}
        self.conn.execute(
            """
            UPDATE tasks
            SET status = ?, result = ?, updated_at = ?
            WHERE id = ?
            """,
            (DONE, dump_json(result), utc_now(), task_id),
        )
        self.conn.commit()
        return self.get_task(task_id)

    def fail_task(self, task_id: str, error: str) -> dict[str, Any]:
        self.conn.execute(
            """
            UPDATE tasks
            SET status = ?, error = ?, updated_at = ?
            WHERE id = ?
            """,
            (FAILED, error, utc_now(), task_id),
        )
        self.conn.commit()
        return self.get_task(task_id)

    def _deserialize(self, item: dict[str, Any]) -> dict[str, Any]:
        item["payload"] = load_json(item.get("payload"), {})
        item["result"] = load_json(item.get("result"), None)
        return item

