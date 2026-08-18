"""
Tests for database models and operations
"""
import pytest
import asyncio
import os
from pathlib import Path
from sqlalchemy import select


@pytest.mark.asyncio
class TestDatabaseModels:
    """Test database model definitions"""
    
    async def test_user_model(self):
        """Test User model"""
        from bot.database.models import User, UserRole
        
        # Test model attributes
        assert hasattr(User, 'id')
        assert hasattr(User, 'telegram_id')
        assert hasattr(User, 'username')
        assert hasattr(User, 'first_name')
        assert hasattr(User, 'last_name')
        assert hasattr(User, 'email')
        assert hasattr(User, 'phone')
        assert hasattr(User, 'language')
        assert hasattr(User, 'role')
        assert hasattr(User, 'created_at')
        assert hasattr(User, 'updated_at')
        assert hasattr(User, 'applications')
    
    async def test_application_model(self):
        """Test Application model"""
        from bot.database.models import Application, ApplicationStatusEnum
        
        # Test model attributes
        assert hasattr(Application, 'id')
        assert hasattr(Application, 'user_id')
        assert hasattr(Application, 'service_type_id')
        assert hasattr(Application, 'title')
        assert hasattr(Application, 'description')
        assert hasattr(Application, 'status')
        assert hasattr(Application, 'file_path')
        assert hasattr(Application, 'file_type')
        assert hasattr(Application, 'file_name')
        assert hasattr(Application, 'created_at')
        assert hasattr(Application, 'updated_at')
        assert hasattr(Application, 'user')
        assert hasattr(Application, 'service_type')
        assert hasattr(Application, 'status_history')
    
    async def test_service_type_model(self):
        """Test ServiceType model"""
        from bot.database.models import ServiceType
        
        # Test model attributes
        assert hasattr(ServiceType, 'id')
        assert hasattr(ServiceType, 'name_en')
        assert hasattr(ServiceType, 'name_ru')
        assert hasattr(ServiceType, 'description_en')
        assert hasattr(ServiceType, 'description_ru')
        assert hasattr(ServiceType, 'get_name')
        assert hasattr(ServiceType, 'get_description')
    
    async def test_application_status_model(self):
        """Test ApplicationStatus model"""
        from bot.database.models import ApplicationStatus
        
        # Test model attributes
        assert hasattr(ApplicationStatus, 'id')
        assert hasattr(ApplicationStatus, 'application_id')
        assert hasattr(ApplicationStatus, 'status')
        assert hasattr(ApplicationStatus, 'changed_by')
        assert hasattr(ApplicationStatus, 'notes')
        assert hasattr(ApplicationStatus, 'created_at')
    
    async def test_user_role_enum(self):
        """Test UserRole enum"""
        from bot.database.models import UserRole
        
        assert UserRole.USER.value == "user"
        assert UserRole.ADMIN.value == "admin"
    
    async def test_application_status_enum(self):
        """Test ApplicationStatusEnum enum"""
        from bot.database.models import ApplicationStatusEnum
        
        assert ApplicationStatusEnum.NEW.value == "new"
        assert ApplicationStatusEnum.IN_PROGRESS.value == "in_progress"
        assert ApplicationStatusEnum.COMPLETED.value == "completed"
        assert ApplicationStatusEnum.REJECTED.value == "rejected"


class TestDatabaseOperations:
    """Test database operations - using sync for simplicity in tests"""
    
    def test_database_creation(self):
        """Test database and tables creation"""
        from bot.database.models import Base
        
        # Tables should be created
        assert len(Base.metadata.tables) > 0
    
    def test_service_type_get_name(self):
        """Test ServiceType get_name method"""
        from bot.database.models import ServiceType
        
        service_type = ServiceType(
            name_en="Consultation",
            name_ru="Консультация",
            description_en="Professional consultation",
            description_ru="Профессиональная консультация"
        )
        
        assert service_type.get_name("en") == "Consultation"
        assert service_type.get_name("ru") == "Консультация"
        assert service_type.get_name("fr") == "Consultation"  # Fallback to English
    
    async def test_service_type_get_name(self):
        """Test ServiceType get_name method"""
        from bot.database.models import ServiceType
        
        service_type = ServiceType(
            name_en="Consultation",
            name_ru="Консультация",
            description_en="Professional consultation",
            description_ru="Профессиональная консультация"
        )
        
        assert service_type.get_name("en") == "Consultation"
        assert service_type.get_name("ru") == "Консультация"
        assert service_type.get_name("fr") == "Consultation"  # Fallback to English
