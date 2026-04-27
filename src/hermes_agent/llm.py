from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from .config import Settings


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
    raw_arguments: str


@dataclass
class TurnResult:
    text: str
    assistant_message: dict[str, Any]
    tool_calls: list[ToolCall]


class OpenAILLM:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.enabled = settings.llm_enabled
        self.client = (
            OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)
            if self.enabled
            else None
        )

    def run_turn(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.2,
    ) -> TurnResult:
        if not self.client:
            raise RuntimeError("LLM is not configured. Set OPENAI_API_KEY.")

        kwargs: dict[str, Any] = {
            "model": self.settings.openai_model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        message = choice.message

        content = self._content_to_text(getattr(message, "content", ""))
        tool_calls: list[ToolCall] = []
        serialized_calls: list[dict[str, Any]] = []

        for index, call in enumerate(getattr(message, "tool_calls", []) or []):
            function = getattr(call, "function", None)
            name = getattr(function, "name", "")
            raw_arguments = getattr(function, "arguments", "{}") or "{}"
            try:
                args = json.loads(raw_arguments)
                if not isinstance(args, dict):
                    args = {"value": args}
            except json.JSONDecodeError:
                args = {}
            call_id = getattr(call, "id", f"tool_call_{index}")
            tool_calls.append(
                ToolCall(
                    id=call_id,
                    name=name,
                    arguments=args,
                    raw_arguments=raw_arguments,
                )
            )
            serialized_calls.append(
                {
                    "id": call_id,
                    "type": "function",
                    "function": {"name": name, "arguments": raw_arguments},
                }
            )

        assistant_message: dict[str, Any] = {"role": "assistant", "content": content}
        if serialized_calls:
            assistant_message["tool_calls"] = serialized_calls
            if not content:
                assistant_message["content"] = None

        return TurnResult(
            text=content,
            assistant_message=assistant_message,
            tool_calls=tool_calls,
        )

    def simple_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
    ) -> str:
        turn = self.run_turn(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            tools=None,
            temperature=temperature,
        )
        return turn.text.strip()

    def _content_to_text(self, content: Any) -> str:
        if isinstance(content, str):
            return content
        if not content:
            return ""
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text") or item.get("content")
                    if text:
                        parts.append(str(text))
                else:
                    text = getattr(item, "text", None)
                    if text:
                        parts.append(str(text))
            return "\n".join(parts).strip()
        return str(content)

