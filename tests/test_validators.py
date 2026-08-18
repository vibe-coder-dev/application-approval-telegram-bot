"""
Tests for input validators
"""
import pytest
from bot.utils.validators import (
    validate_email, validate_phone, validate_text,
    validate_title, validate_description, validate_service_type,
    validate_application_id
)


class TestEmailValidator:
    """Test email validation"""
    
    def test_valid_email(self):
        """Test valid email addresses"""
        valid, error = validate_email("test@example.com")
        assert valid is True
        assert error == ""
    
    def test_invalid_email_format(self):
        """Test invalid email formats"""
        invalid_emails = [
            "not-an-email",
            "test@",
            "@example.com",
            "test example@com",
            "test@example..com"
        ]
        
        for email in invalid_emails:
            valid, error = validate_email(email)
            assert valid is False, f"Email '{email}' should be invalid but was validated as valid"
            assert error != ""
    
    def test_empty_email(self):
        """Test empty email"""
        valid, error = validate_email("")
        assert valid is False


class TestPhoneValidator:
    """Test phone validation"""
    
    def test_valid_phone(self):
        """Test valid phone numbers"""
        valid_phones = [
            "1234567890",
            "+1234567890",
            "123-456-7890",
            "(123) 456-7890",
            "123 456 7890"
        ]
        
        for phone in valid_phones:
            valid, error = validate_phone(phone)
            assert valid is True
    
    def test_invalid_phone(self):
        """Test invalid phone numbers"""
        invalid_phones = [
            "abc",
            "123",  # Too short
            "12345678901234567890",  # Too long
            "",
            "phone"
        ]
        
        for phone in invalid_phones:
            valid, error = validate_phone(phone)
            assert valid is False


class TestTextValidator:
    """Test text validation"""
    
    def test_valid_text(self):
        """Test valid text"""
        valid, error = validate_text("Hello World")
        assert valid is True
    
    def test_empty_text(self):
        """Test empty text"""
        valid, error = validate_text("")
        assert valid is False
    
    def test_too_short_text(self):
        """Test text that's too short"""
        valid, error = validate_text("ab", min_length=5)
        assert valid is False
    
    def test_too_long_text(self):
        """Test text that's too long"""
        valid, error = validate_text("a" * 100, max_length=50)
        assert valid is False


class TestTitleValidator:
    """Test title validation"""
    
    def test_valid_title(self):
        """Test valid title"""
        valid, error = validate_title("My Application")
        assert valid is True
    
    def test_too_short_title(self):
        """Test title that's too short"""
        valid, error = validate_title("ab")
        assert valid is False


class TestDescriptionValidator:
    """Test description validation"""
    
    def test_valid_description(self):
        """Test valid description"""
        valid, error = validate_description("This is a description")
        assert valid is True
    
    def test_empty_description(self):
        """Test empty description (should be valid as it's optional)"""
        valid, error = validate_description("")
        assert valid is True


class TestServiceTypeValidator:
    """Test service type validation"""
    
    def test_valid_service_type(self):
        """Test valid service type"""
        service_types = ["Consultation", "Development", "Support", "Training"]
        for service_type in service_types:
            valid, error = validate_service_type(service_type, service_types)
            assert valid is True
    
    def test_invalid_service_type(self):
        """Test invalid service type"""
        service_types = ["Consultation", "Development", "Support", "Training"]
        valid, error = validate_service_type("Invalid", service_types)
        assert valid is False


class TestApplicationIdValidator:
    """Test application ID validation"""
    
    def test_valid_application_id(self):
        """Test valid application ID"""
        valid, error = validate_application_id("123")
        assert valid is True
    
    def test_invalid_application_id(self):
        """Test invalid application ID"""
        invalid_ids = ["abc", "-1", "0", ""]
        for app_id in invalid_ids:
            valid, error = validate_application_id(app_id)
            assert valid is False
