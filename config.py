from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: str
    ADMIN_CHAT_ID: int
    OPERATOR_USERNAME: str = "@topkassa_pomoshnik"
    MIN_TOPUP: int = 100
    MAX_TOPUP: int = 100_000


settings = Settings()
