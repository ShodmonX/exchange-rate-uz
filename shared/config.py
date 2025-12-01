from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TITLE: str
    API_VERSION: str
    BOT_TOKEN: str
    DATABASE_URL: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings() # type: ignore