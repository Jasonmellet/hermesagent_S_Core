from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str = Field(default="default")


class ChatResponse(BaseModel):
    run_id: str
    session_id: str
    output: str
    tool_calls: int


class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=1)
    kind: str = Field(default="generic")
    priority: int = Field(default=3, ge=1, le=5)
    payload: dict[str, Any] = Field(default_factory=dict)


class SubmitFeedbackRequest(BaseModel):
    run_id: str | None = None
    score: float = Field(ge=0.0, le=1.0)
    notes: str = ""


class ManualTaskResultRequest(BaseModel):
    result: dict[str, Any] = Field(default_factory=dict)

