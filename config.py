from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация pydantic"""
    
    DB_URL: str = "postgresql+psycopg2://user:pass@localhost/links_db"
    REDIS_URL: str = "redis://localhost:6379"
    JWT_SECRET: str = "secret"
    DEFAULT_UNUSED_DAYS: int = 14

    class Config:
        env_file = ".env"


settings = Settings()