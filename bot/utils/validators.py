"""
Validation utilities for user input
"""
import re
from typing import Optional
from .translations import get_translation


def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate email format
    
    Args:
        email: Email address to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    # More strict email regex pattern
    # Local part: letters, numbers, dots, underscores, percent, plus, hyphen
    # @ symbol
    # Domain: letters, numbers, dots, hyphens
    # TLD: at least 2 letters
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Additional checks for consecutive dots
    if '..' in email:
        return False, "Invalid email format"
    
    if re.match(pattern, email):
        return True, ""
    else:
        return False, "Invalid email format"


def validate_phone(phone: str) -> tuple[bool, str]:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return False, "Phone is required"
    
    # Remove spaces, dashes, and parentheses
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check if it contains only digits
    if not cleaned.isdigit():
        return False, "Phone must contain only digits"
    
    # Check minimum length (7 digits) and maximum length (15 digits)
    if len(cleaned) < 7 or len(cleaned) > 15:
        return False, "Phone must be between 7 and 15 digits"
    
    return True, ""


def validate_text(text: str, min_length: int = 1, max_length: int = 1000) -> tuple[bool, str]:
    """
    Validate text input
    
    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Text is required"
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"Text must be at least {min_length} characters"
    
    if len(text) > max_length:
        return False, f"Text must be less than {max_length} characters"
    
    return True, ""


def validate_title(title: str) -> tuple[bool, str]:
    """Validate application title"""
    return validate_text(title, min_length=3, max_length=255)


def validate_description(description: str) -> tuple[bool, str]:
    """Validate application description"""
    if not description or not description.strip():
        return True, ""  # Description is optional
    
    return validate_text(description, min_length=1, max_length=2000)


def validate_service_type(service_type: str, available_types: list) -> tuple[bool, str]:
    """Validate service type selection"""
    if not service_type:
        return False, "Service type is required"
    
    if service_type not in available_types:
        return False, f"Invalid service type. Available: {', '.join(available_types)}"
    
    return True, ""


def validate_application_id(application_id: str) -> tuple[bool, str]:
    """Validate application ID"""
    if not application_id:
        return False, "Application ID is required"
    
    try:
        app_id = int(application_id)
        if app_id <= 0:
            return False, "Application ID must be positive"
        return True, ""
    except ValueError:
        return False, "Application ID must be a number"
