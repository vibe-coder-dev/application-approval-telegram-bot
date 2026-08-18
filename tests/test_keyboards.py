"""
Tests for keyboard utilities
"""
import pytest
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


class TestMainKeyboard:
    """Test main menu keyboard"""
    
    def test_get_main_keyboard_english(self):
        """Test main keyboard in English"""
        from bot.utils.keyboards import get_main_keyboard
        
        keyboard = get_main_keyboard("en")
        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert keyboard.resize_keyboard is True
    
    def test_get_main_keyboard_russian(self):
        """Test main keyboard in Russian"""
        from bot.utils.keyboards import get_main_keyboard
        
        keyboard = get_main_keyboard("ru")
        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert keyboard.resize_keyboard is True


class TestAdminKeyboard:
    """Test admin keyboard"""
    
    def test_get_admin_keyboard(self):
        """Test admin keyboard"""
        from bot.utils.keyboards import get_admin_keyboard
        
        keyboard = get_admin_keyboard("en")
        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert keyboard.resize_keyboard is True


class TestServiceTypeKeyboard:
    """Test service type keyboard"""
    
    def test_get_service_type_keyboard_english(self):
        """Test service type keyboard in English"""
        from bot.utils.keyboards import get_service_type_keyboard
        
        keyboard = get_service_type_keyboard("en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
    
    def test_get_service_type_keyboard_russian(self):
        """Test service type keyboard in Russian"""
        from bot.utils.keyboards import get_service_type_keyboard
        
        keyboard = get_service_type_keyboard("ru")
        assert isinstance(keyboard, InlineKeyboardMarkup)


class TestStatusKeyboard:
    """Test status keyboard"""
    
    def test_get_status_keyboard_english(self):
        """Test status keyboard in English"""
        from bot.utils.keyboards import get_status_keyboard
        
        keyboard = get_status_keyboard("en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
    
    def test_get_status_keyboard_russian(self):
        """Test status keyboard in Russian"""
        from bot.utils.keyboards import get_status_keyboard
        
        keyboard = get_status_keyboard("ru")
        assert isinstance(keyboard, InlineKeyboardMarkup)


class TestLanguageKeyboard:
    """Test language keyboard"""
    
    def test_get_language_keyboard_english(self):
        """Test language keyboard with English selected"""
        from bot.utils.keyboards import get_language_keyboard
        
        keyboard = get_language_keyboard("en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
    
    def test_get_language_keyboard_russian(self):
        """Test language keyboard with Russian selected"""
        from bot.utils.keyboards import get_language_keyboard
        
        keyboard = get_language_keyboard("ru")
        assert isinstance(keyboard, InlineKeyboardMarkup)


class TestConfirmationKeyboard:
    """Test confirmation keyboard"""
    
    def test_get_confirmation_keyboard_english(self):
        """Test confirmation keyboard in English"""
        from bot.utils.keyboards import get_confirmation_keyboard
        
        keyboard = get_confirmation_keyboard("en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
    
    def test_get_confirmation_keyboard_russian(self):
        """Test confirmation keyboard in Russian"""
        from bot.utils.keyboards import get_confirmation_keyboard
        
        keyboard = get_confirmation_keyboard("ru")
        assert isinstance(keyboard, InlineKeyboardMarkup)


class TestFileTypeKeyboard:
    """Test file type keyboard"""
    
    def test_get_file_type_keyboard(self):
        """Test file type keyboard"""
        from bot.utils.keyboards import get_file_type_keyboard
        
        keyboard = get_file_type_keyboard("en")
        assert isinstance(keyboard, InlineKeyboardMarkup)


class TestPaginationKeyboard:
    """Test pagination keyboard"""
    
    def test_get_pagination_keyboard_first_page(self):
        """Test pagination keyboard on first page"""
        from bot.utils.keyboards import get_pagination_keyboard
        
        keyboard = get_pagination_keyboard(page=1, total_pages=5, lang="en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
    
    def test_get_pagination_keyboard_middle_page(self):
        """Test pagination keyboard on middle page"""
        from bot.utils.keyboards import get_pagination_keyboard
        
        keyboard = get_pagination_keyboard(page=3, total_pages=5, lang="en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
    
    def test_get_pagination_keyboard_last_page(self):
        """Test pagination keyboard on last page"""
        from bot.utils.keyboards import get_pagination_keyboard
        
        keyboard = get_pagination_keyboard(page=5, total_pages=5, lang="en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
    
    def test_get_pagination_keyboard_single_page(self):
        """Test pagination keyboard with single page"""
        from bot.utils.keyboards import get_pagination_keyboard
        
        keyboard = get_pagination_keyboard(page=1, total_pages=1, lang="en")
        assert isinstance(keyboard, InlineKeyboardMarkup)
