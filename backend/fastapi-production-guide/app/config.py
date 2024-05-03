from pydantic_settings import BaseSettings, SettingsConfigDict


# Use settings class instead of os.environ
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ROOT_PATH: str = ""
    LOGGING_LEVEL: str = "INFO"
    MONGO_URI: str
    GITHUB_OAUTH_CLIENT_ID: str
    GITHUB_OAUTH_CLIENT_SECRET: str
    TESTING: bool = False


settings = Settings()
