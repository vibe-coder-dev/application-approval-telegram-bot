"""
Application settings and configuration
"""
try:
    # For pydantic 2.0+
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pydantic import Field
    from typing import Optional
    import os
except ImportError:
    # Fallback for older versions
    from pydantic import BaseSettings, Field
    from typing import Optional
    import os
    
    # Create SettingsConfigDict for older pydantic
    class SettingsConfigDict:
        def __init__(self, **kwargs):
            self.kwargs = kwargs


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Bot settings
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token")
    ADMIN_ID: int = Field(..., description="Admin user ID")
    
    # Database settings
    DB_TYPE: str = Field("postgresql", description="Database type: sqlite or postgresql")
    POSTGRES_HOST: str = Field("localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(5432, description="PostgreSQL port")
    POSTGRES_DB: str = Field("application_bot", description="PostgreSQL database name")
    POSTGRES_USER: str = Field("postgres", description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field("postgres", description="PostgreSQL password")
    SQLite_DB_PATH: str = Field("data/bot.db", description="SQLite database path")
    
    # Application settings
    UPLOAD_DIR: str = Field("uploads", description="Directory for uploaded files")
    DEFAULT_LANGUAGE: str = Field("en", description="Default language")
    
    # Available languages
    AVAILABLE_LANGUAGES: list = Field(default_factory=lambda: ["en", "ru"], description="Available languages")
    
    # Service types
    SERVICE_TYPES: dict = Field({
        "en": ["Consultation", "Development", "Support", "Training"],
        "ru": ["Консультация", "Разработка", "Поддержка", "Обучение"]
    }, description="Available service types by language")
    
    # Application statuses
    APPLICATION_STATUSES: dict = Field({
        "en": ["New", "In Progress", "Completed", "Rejected"],
        "ru": ["Новая", "В обработке", "Завершена", "Отклонена"]
    }, description="Application statuses by language")
    
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "sqlite":
            return f"sqlite+aiosqlite:///{self.SQLite_DB_PATH}"
        else:
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def is_sqlite(self) -> bool:
        return self.DB_TYPE == "sqlite"


settings = Settings()
