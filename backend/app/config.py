from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "English Speaking Test Analyzer"
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/speak_meter")
    upload_dir: str = Field(default="uploads")
    whisper_model: str = Field(default="base")
    languagetool_language: str = Field(default="en-US")
    backend_cors_origins: str = Field(default="http://localhost:5173,http://127.0.0.1:5173")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
