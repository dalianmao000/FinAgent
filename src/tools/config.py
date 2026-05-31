"""Configuration management for FinAgent Unified.

All sensitive values (passwords, API keys) must be set in .env file.
This module reads from .env via pydantic-settings.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings - values loaded from .env file."""

    # ==================
    # Model Configuration
    # ==================
    model_name: str = "qwen-turbo"
    model_type: str = "qwen_dashscope"
    model_temperature: float = 0.7
    model_max_tokens: int = 2000
    model_timeout: int = 30

    # ==================
    # API Keys
    # ==================
    dashscope_api_key: str = ""

    # ==================
    # Redis
    # ==================
    redis_url: str = "redis://localhost:6379/0"

    # ==================
    # MySQL - FinAgent Database (main database)
    # ==================
    finagent_db_host: str = "localhost"
    finagent_db_port: int = 3306
    finagent_db_user: str = "root"
    finagent_db_password: str = ""
    finagent_db_name: str = "finagent"
    finagent_db_charset: str = "utf8mb4"

    # ==================
    # MySQL - Stock Database (for investment tools)
    # ==================
    stock_db_host: str = "localhost"
    stock_db_port: int = 3306
    stock_db_user: str = "root"
    stock_db_password: str = ""
    stock_db_name: str = "stock"
    stock_db_charset: str = "utf8mb4"

    # ==================
    # MySQL - Customer Database (for customer tools)
    # ==================
    customer_db_host: str = "localhost"
    customer_db_port: int = 3306
    customer_db_user: str = "root"
    customer_db_password: str = ""
    customer_db_name: str = "enterprise_credit_clients"
    customer_db_charset: str = "utf8mb4"

    # ==================
    # Elasticsearch (for insurance tools)
    # ==================
    es_host: str = "localhost"
    es_port: int = 9200
    es_username: str = "elastic"
    es_password: str = ""
    es_index_name: str = "qwen_agent_docs_vector"

    # ==================
    # Tavily API (for news search)
    # ==================
    tavily_api_key: str = ""

    # ==================
    # API Server
    # ==================
    api_host: str = "0.0.0.0"
    api_port: int = 5000

    # ==================
    # URL Properties
    # ==================
    @property
    def finagent_db_url(self) -> str:
        return (f"mysql+mysqlconnector://{self.finagent_db_user}:{self.finagent_db_password}"
                f"@{self.finagent_db_host}:{self.finagent_db_port}/{self.finagent_db_name}"
                f"?charset={self.finagent_db_charset}")

    @property
    def stock_db_url(self) -> str:
        return (f"mysql+mysqlconnector://{self.stock_db_user}:{self.stock_db_password}"
                f"@{self.stock_db_host}:{self.stock_db_port}/{self.stock_db_name}"
                f"?charset={self.stock_db_charset}")

    @property
    def customer_db_url(self) -> str:
        return (f"mysql+mysqlconnector://{self.customer_db_user}:{self.customer_db_password}"
                f"@{self.customer_db_host}:{self.customer_db_port}/{self.customer_db_name}"
                f"?charset={self.customer_db_charset}")

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
