from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    VECTOR_STORE_MODE: str = "sync"
    DB_CONN: PostgresDsn


settings = Settings()
