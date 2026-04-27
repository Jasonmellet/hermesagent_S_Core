from __future__ import annotations

import re
import sqlite3
from typing import Any

from .db import dump_json, load_json, row_to_dict


class MemoryStore:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(
        self,
        content: str,
        *,
        category: str = "note",
        session_id: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        relevance: float = 0.5,
    ) -> int:
        tags = tags or []
        metadata = metadata or {}
        cursor = self.conn.execute(
            """
            INSERT INTO memory(session_id, category, content, tags, metadata, relevance)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (session_id, category, content, dump_json(tags), dump_json(metadata), relevance),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def search(self, query: str, *, limit: int = 8) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            rows = self.conn.execute(
                """
                SELECT * FROM memory
                ORDER BY datetime(created_at) DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [self._deserialize(row_to_dict(r) or {}) for r in rows]

        fts_query = self._to_fts_query(query)
        if not fts_query:
            return []

        rows = self.conn.execute(
            """
            SELECT m.*, bm25(memory_fts) AS score
            FROM memory_fts
            JOIN memory m ON m.id = memory_fts.rowid
            WHERE memory_fts MATCH ?
            ORDER BY score ASC, datetime(m.created_at) DESC
            LIMIT ?
            """,
            (fts_query, limit),
        ).fetchall()
        return [self._deserialize(row_to_dict(r) or {}) for r in rows]

    def recent(self, *, limit: int = 10, category: str | None = None) -> list[dict[str, Any]]:
        if category:
            rows = self.conn.execute(
                """
                SELECT * FROM memory
                WHERE category = ?
                ORDER BY datetime(created_at) DESC
                LIMIT ?
                """,
                (category, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT * FROM memory
                ORDER BY datetime(created_at) DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [self._deserialize(row_to_dict(r) or {}) for r in rows]

    def _to_fts_query(self, raw: str) -> str:
        tokens = re.findall(r"[a-zA-Z0-9_]{2,}", raw.lower())
        return " OR ".join(tokens)

    def _deserialize(self, item: dict[str, Any]) -> dict[str, Any]:
        item["tags"] = load_json(item.get("tags"), [])
        item["metadata"] = load_json(item.get("metadata"), {})
        return item

