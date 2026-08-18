# Application Bot - Automated Tests Summary

## 📊 Test Overview

This directory contains comprehensive automated tests for the Application Bot, covering all major components and functionality.

### Test Statistics
- **Total Tests**: 60
- **Test Files**: 7
- **Coverage**: Core functionality, utilities, and models
- **Status**: ✅ All tests passing

## 📁 Test Files

### 1. `conftest.py`
- **Purpose**: Pytest configuration and fixtures
- **Fixtures**:
  - `test_env()`: Test environment variables
  - `setup_test_directories()`: Create and cleanup test directories
  - `mock_bot()`: Mock Telegram bot instance
  - `mock_message()`: Mock Telegram message
  - `mock_callback_query()`: Mock Telegram callback query
  - `mock_state()`: Mock FSM state

### 2. `test_translations.py` (8 tests)
- **Purpose**: Test multilingual support
- **Tests**:
  - English and Russian translations
  - String formatting with variables
  - Fallback to default language
  - Button translations
  - Status translations
  - Translation key existence

### 3. `test_validators.py` (17 tests)
- **Purpose**: Test input validation utilities
- **Tests**:
  - Email validation (valid/invalid formats)
  - Phone validation (valid/invalid formats)
  - Text validation (length, empty)
  - Title validation
  - Description validation
  - Service type validation
  - Application ID validation

### 4. `test_database.py` (8 tests)
- **Purpose**: Test database models and operations
- **Tests**:
  - User model attributes
  - Application model attributes
  - ServiceType model attributes
  - ApplicationStatus model attributes
  - UserRole enum values
  - ApplicationStatusEnum enum values
  - Database table creation
  - ServiceType get_name method

### 5. `test_file_handler.py` (7 tests)
- **Purpose**: Test file handling utilities
- **Tests**:
  - Directory creation
  - Filename generation
  - File save and delete operations
  - Photo file handling
  - File information retrieval
  - File size validation
  - Allowed extensions checking

### 6. `test_keyboards.py` (13 tests)
- **Purpose**: Test keyboard generation utilities
- **Tests**:
  - Main keyboard (English/Russian)
  - Service type keyboard (English/Russian)
  - Language keyboard (English/Russian)
  - Confirmation keyboard (English/Russian)
  - File type keyboard
  - Pagination keyboard (first/middle/last/single page)

### 7. `test_settings_simple.py` (7 tests)
- **Purpose**: Test application settings
- **Tests**:
  - Settings class existence
  - Default values
  - PostgreSQL database URL generation
  - SQLite database URL generation
  - is_sqlite property
  - Service types configuration
  - Application statuses configuration

## 🚀 Running Tests

### Basic Test Run
```bash
# Run all tests
python -m pytest tests/ -v

# Run with minimal output
python -m pytest tests/ -q

# Run specific test file
python -m pytest tests/test_translations.py -v

# Run specific test
python -m pytest tests/test_validators.py::TestEmailValidator::test_valid_email -v
```

### Using the Test Runner Script
```bash
# Run all tests using the provided script
python tests/run_tests.py
```

### With Coverage
```bash
# Install coverage first
pip install pytest-cov

# Run tests with coverage
python -m pytest tests/ --cov=bot --cov-report=term-missing
```

## 📋 Test Categories

### Unit Tests
- **Translations**: 8 tests
- **Validators**: 17 tests
- **Keyboards**: 13 tests
- **File Handler**: 7 tests
- **Database Models**: 8 tests
- **Settings**: 10 tests

### Integration Tests
- Tests that verify interaction between components
- File handling with actual file operations
- Database model relationships

## ✅ Test Results

All 63 tests are currently passing:

```
========================= 63 passed, 2 warnings in 5.46s =========================
```

## 🛠️ Test Dependencies

- `pytest>=7.4.3`
- `pytest-asyncio>=0.21.1`
- `pytest-cov>=4.1.0` (optional, for coverage)

## 📝 Notes

- Tests use mocking to avoid actual Telegram API calls
- Database tests use SQLite for simplicity
- File operations use temporary directories that are cleaned up automatically
- Environment variables are set in `conftest.py` for consistent test environment
- Tests are designed to run independently and in any order

## 🎯 Future Test Enhancements

Potential areas for additional tests:
- End-to-end integration tests with actual Telegram bot
- Database migration tests
- Performance tests
- Security tests
- Error handling and edge cases
- Web admin panel tests (Flask routes, authentication, status changes)
