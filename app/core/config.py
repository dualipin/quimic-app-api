from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    gemini_api_key: str
    email_host: str
    email_port: int = 587
    email_from: str
    email_password: str
    database_url: str = "postgresql://user:password@localhost:5432/quimic_db"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
