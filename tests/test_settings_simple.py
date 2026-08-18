"""
Simple tests for application settings without environment dependencies
"""
import pytest


class TestSettingsStructure:
    """Test settings structure and defaults"""
    
    def test_settings_class_exists(self):
        """Test that Settings class exists"""
        from bot.config.settings import Settings
        assert Settings is not None
    
    def test_settings_defaults(self):
        """Test settings default values"""
        import os
        # Clear environment variables that might affect defaults
        env_backup = os.environ.copy()
        for key in ['DB_TYPE', 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB', 
                   'POSTGRES_USER', 'POSTGRES_PASSWORD', 'SQLite_DB_PATH',
                   'UPLOAD_DIR', 'DEFAULT_LANGUAGE', 'AVAILABLE_LANGUAGES']:
            if key in os.environ:
                del os.environ[key]
        
        try:
            from bot.config.settings import Settings
            
            # Create settings with minimal required fields
            settings = Settings(
                BOT_TOKEN="test_token",
                ADMIN_ID=12345
            )
            
            # Test default values
            assert settings.DB_TYPE == "postgresql"
        finally:
            # Restore environment
            os.environ.clear()
            os.environ.update(env_backup)
        assert settings.POSTGRES_HOST == "localhost"
        assert settings.POSTGRES_PORT == 5432
        assert settings.POSTGRES_DB == "application_bot"
        assert settings.POSTGRES_USER == "postgres"
        assert settings.POSTGRES_PASSWORD == "postgres"
        assert settings.SQLite_DB_PATH == "data/bot.db"
        assert settings.UPLOAD_DIR == "uploads"
        assert settings.DEFAULT_LANGUAGE == "en"
        assert settings.AVAILABLE_LANGUAGES == ["en", "ru"]
    
    def test_database_url_postgresql(self):
        """Test PostgreSQL database URL generation"""
        from bot.config.settings import Settings
        
        settings = Settings(
            BOT_TOKEN="test_token",
            ADMIN_ID=12345,
            DB_TYPE="postgresql",
            POSTGRES_HOST="localhost",
            POSTGRES_PORT=5432,
            POSTGRES_DB="test_db",
            POSTGRES_USER="test_user",
            POSTGRES_PASSWORD="test_pass"
        )
        
        db_url = settings.DATABASE_URL
        assert db_url.startswith("postgresql+asyncpg://")
        assert "test_user" in db_url
        assert "test_pass" in db_url
        assert "localhost" in db_url
        assert "test_db" in db_url
    
    def test_database_url_sqlite(self):
        """Test SQLite database URL generation"""
        from bot.config.settings import Settings
        
        settings = Settings(
            BOT_TOKEN="test_token",
            ADMIN_ID=12345,
            DB_TYPE="sqlite",
            SQLite_DB_PATH="data/test.db"
        )
        
        db_url = settings.DATABASE_URL
        assert db_url.startswith("sqlite+aiosqlite:///")
        assert "data/test.db" in db_url
    
    def test_is_sqlite_property(self):
        """Test is_sqlite property"""
        from bot.config.settings import Settings
        
        # Test with SQLite
        settings_sqlite = Settings(
            BOT_TOKEN="test_token",
            ADMIN_ID=12345,
            DB_TYPE="sqlite"
        )
        assert settings_sqlite.is_sqlite is True
        
        # Test with PostgreSQL
        settings_postgres = Settings(
            BOT_TOKEN="test_token",
            ADMIN_ID=12345,
            DB_TYPE="postgresql"
        )
        assert settings_postgres.is_sqlite is False
    
    def test_service_types(self):
        """Test service types configuration"""
        from bot.config.settings import Settings
        
        settings = Settings(
            BOT_TOKEN="test_token",
            ADMIN_ID=12345
        )
        
        assert hasattr(settings, 'SERVICE_TYPES')
        assert 'en' in settings.SERVICE_TYPES
        assert 'ru' in settings.SERVICE_TYPES
        
        # Check English service types
        en_types = settings.SERVICE_TYPES['en']
        assert 'Consultation' in en_types
        assert 'Development' in en_types
        assert 'Support' in en_types
        assert 'Training' in en_types
        
        # Check Russian service types
        ru_types = settings.SERVICE_TYPES['ru']
        assert 'Консультация' in ru_types
        assert 'Разработка' in ru_types
        assert 'Поддержка' in ru_types
        assert 'Обучение' in ru_types
    
    def test_application_statuses(self):
        """Test application statuses configuration"""
        from bot.config.settings import Settings
        
        settings = Settings(
            BOT_TOKEN="test_token",
            ADMIN_ID=12345
        )
        
        assert hasattr(settings, 'APPLICATION_STATUSES')
        assert 'en' in settings.APPLICATION_STATUSES
        assert 'ru' in settings.APPLICATION_STATUSES
        
        # Check English statuses
        en_statuses = settings.APPLICATION_STATUSES['en']
        assert 'New' in en_statuses
        assert 'In Progress' in en_statuses
        assert 'Completed' in en_statuses
        assert 'Rejected' in en_statuses
        
        # Check Russian statuses
        ru_statuses = settings.APPLICATION_STATUSES['ru']
        assert 'Новая' in ru_statuses
        assert 'В обработке' in ru_statuses
        assert 'Завершена' in ru_statuses
        assert 'Отклонена' in ru_statuses
