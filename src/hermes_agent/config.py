from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    openai_base_url: str = Field(
        default="https://api.openai.com/v1", alias="OPENAI_BASE_URL"
    )

    db_path: str = Field(default="./hermes.db", alias="HERMES_DB_PATH")
    max_tool_steps: int = Field(default=8, alias="HERMES_MAX_TOOL_STEPS")
    log_level: str = Field(default="INFO", alias="HERMES_LOG_LEVEL")

    search_provider: Literal["duckduckgo", "tavily"] = Field(
        default="duckduckgo", alias="HERMES_SEARCH_PROVIDER"
    )
    tavily_api_key: str = Field(default="", alias="TAVILY_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def resolved_db_path(self) -> str:
        return str(Path(self.db_path).expanduser().resolve())

    @property
    def llm_enabled(self) -> bool:
        return bool(self.openai_api_key.strip())


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

