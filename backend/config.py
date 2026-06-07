from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    wb_base_url: str = "https://api.worldbank.org/v2"
    wb_timeout_seconds: int = 15
    cache_ttl_seconds: int = 604800
    cors_origins: str = "http://localhost:8501"
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
