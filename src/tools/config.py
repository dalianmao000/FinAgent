"""Configuration management for FinAgent Unified."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    dashscope_api_key: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # MySQL
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "password"
    mysql_database: str = "finagent"

    # Elasticsearch
    es_host: str = "localhost"
    es_port: int = 9200
    es_username: str = "elastic"
    es_password: str = ""

    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 5000

    @property
    def mysql_url(self) -> str:
        return f"mysql+mysqlconnector://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()