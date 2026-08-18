"""
Tests for translation utilities
"""
import pytest
from bot.utils.translations import get_translation, get_text, translations


class TestTranslations:
    """Test translation functionality"""
    
    def test_get_translation_english(self):
        """Test English translations"""
        welcome = get_translation("en", "welcome")
        assert "Welcome" in welcome
        assert "Application Bot" in welcome
    
    def test_get_translation_russian(self):
        """Test Russian translations"""
        welcome = get_translation("ru", "welcome")
        assert "Добро пожаловать" in welcome
        assert "Application Bot" in welcome
    
    def test_get_translation_with_formatting(self):
        """Test translation with string formatting"""
        text = get_translation("en", "registration_confirm", email="test@example.com", phone="123456")
        assert "test@example.com" in text
        assert "123456" in text
    
    def test_get_translation_fallback(self):
        """Test fallback to default language"""
        # Non-existent language should fall back to English
        text = get_translation("fr", "welcome")
        assert "Welcome" in text or "Добро пожаловать" in text
    
    def test_get_text_alias(self):
        """Test get_text is alias for get_translation"""
        text1 = get_text("en", "welcome")
        text2 = get_translation("en", "welcome")
        assert text1 == text2
    
    def test_translation_keys_exist(self):
        """Test that all expected translation keys exist"""
        expected_keys = [
            "welcome", "help", "language_changed", "select_language",
            "registration_start", "registration_success", "application_start",
            "application_submitted", "status_new", "status_in_progress",
            "status_completed", "status_rejected",
            "btn_yes", "btn_no", "btn_back", "btn_cancel"
        ]
        
        for key in expected_keys:
            assert key in translations["en"], f"Missing English translation: {key}"
            assert key in translations["ru"], f"Missing Russian translation: {key}"
    
    def test_button_translations(self):
        """Test button translations"""
        assert get_translation("en", "btn_yes") == "Yes"
        assert get_translation("ru", "btn_yes") == "Да"
        assert get_translation("en", "btn_no") == "No"
        assert get_translation("ru", "btn_no") == "Нет"
    
    def test_status_translations(self):
        """Test status translations"""
        assert get_translation("en", "status_new") == "New"
        assert get_translation("ru", "status_new") == "Новая"
        assert get_translation("en", "status_completed") == "Completed"
        assert get_translation("ru", "status_completed") == "Завершена"
