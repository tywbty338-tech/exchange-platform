from __future__ import annotations
from pathlib import Path
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    bot_token: str = ""
    database_url: str = "sqlite+aiosqlite:///./exchange.db"
    admin_ids_raw: str = ""
    webhook_secret: str = ""
    webapp_url: str = ""
    ton_api_key: str = ""
    usdt_api_key: str = ""
    wallet_secret: str = ""
    test_mode: bool = True
    payment_provider: str = "mock"
    jwt_secret: str = "change-this"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    @field_validator("admin_ids_raw", mode="before")
    @classmethod
    def _parse_admin(cls, v):
        return str(v) if v else ""

    @property
    def admin_ids(self) -> list[int]:
        if not self.admin_ids_raw:
            return []
        return [int(x.strip()) for x in self.admin_ids_raw.split(",") if x.strip().isdigit()]

    @property
    def admin_id_set(self) -> set[int]:
        return set(self.admin_ids)


@lru_cache
def get_settings() -> Settings:
    return Settings()
