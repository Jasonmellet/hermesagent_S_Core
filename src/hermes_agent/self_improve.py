from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from .db import dump_json, load_json


DEFAULT_STRATEGY: dict[str, Any] = {
    "style": "concise, high-signal, action-oriented",
    "quality_checks": [
        "ground claims in evidence",
        "state assumptions explicitly",
        "produce concrete next actions",
    ],
    "outreach_guidelines": [
        "lead with prospect outcomes, not product features",
        "personalize with role and company context",
        "include one clear CTA",
    ],
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SelfImprover:
    STRATEGY_KEY = "core"

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_strategy(self) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT value FROM strategy WHERE key = ?", (self.STRATEGY_KEY,)
        ).fetchone()
        if row is None:
            self._set_strategy(DEFAULT_STRATEGY)
            return DEFAULT_STRATEGY.copy()
        return load_json(row["value"], DEFAULT_STRATEGY.copy())

    def record_feedback(self, run_id: str | None, score: float, notes: str) -> None:
        self.conn.execute(
            """
            INSERT INTO feedback(run_id, score, notes, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (run_id, score, notes, _utc_now()),
        )
        self.conn.commit()
        self._apply_adaptive_update()

    def _apply_adaptive_update(self) -> dict[str, Any]:
        rows = self.conn.execute(
            """
            SELECT score FROM feedback
            WHERE score IS NOT NULL
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()
        if not rows:
            return self.get_strategy()

        avg_score = sum(float(r["score"]) for r in rows) / len(rows)
        strategy = self.get_strategy()
        checks = strategy.setdefault("quality_checks", [])

        low_score_check = "ask one clarifying question if uncertainty is high"
        high_score_note = "lean into stronger differentiation in outreach hooks"

        if avg_score < 0.6 and low_score_check not in checks:
            checks.append(low_score_check)

        strategy["last_feedback_avg"] = round(avg_score, 3)
        strategy["recent_feedback_count"] = len(rows)
        strategy["adaptive_note"] = high_score_note if avg_score >= 0.85 else ""
        self._set_strategy(strategy)
        return strategy

    def _set_strategy(self, strategy: dict[str, Any]) -> None:
        self.conn.execute(
            """
            INSERT INTO strategy(key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
              value = excluded.value,
              updated_at = excluded.updated_at
            """,
            (self.STRATEGY_KEY, dump_json(strategy), _utc_now()),
        )
        self.conn.commit()

