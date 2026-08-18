"""
Pytest configuration and fixtures for Application Bot tests
"""
import pytest
import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment variables
os.environ['BOT_TOKEN'] = 'test_token_for_testing'
os.environ['ADMIN_ID'] = '123456789'
os.environ['DB_TYPE'] = 'sqlite'
os.environ['SQLite_DB_PATH'] = 'data/test_bot.db'
os.environ['UPLOAD_DIR'] = 'uploads_test'
# Remove AVAILABLE_LANGUAGES from env to use default
if 'AVAILABLE_LANGUAGES' in os.environ:
    del os.environ['AVAILABLE_LANGUAGES']


@pytest.fixture
def test_env():
    """Ensure test environment variables are set"""
    os.environ['BOT_TOKEN'] = 'test_token_for_testing'
    os.environ['ADMIN_ID'] = '123456789'
    os.environ['DB_TYPE'] = 'sqlite'
    os.environ['SQLite_DB_PATH'] = 'data/test_bot.db'
    os.environ['UPLOAD_DIR'] = 'uploads_test'
    return os.environ


@pytest.fixture(scope="session", autouse=True)
def setup_test_directories():
    """Create test directories"""
    # Create test directories
    Path('data').mkdir(exist_ok=True)
    Path('uploads_test').mkdir(exist_ok=True)
    Path('uploads_test/photos').mkdir(exist_ok=True)
    Path('uploads_test/documents').mkdir(exist_ok=True)
    Path('uploads_test/files').mkdir(exist_ok=True)
    
    yield
    
    # Cleanup test files
    import shutil
    if Path('data/test_bot.db').exists():
        Path('data/test_bot.db').unlink()
    if Path('uploads_test').exists():
        shutil.rmtree('uploads_test')


@pytest.fixture
def mock_bot():
    """Mock bot for testing"""
    from unittest.mock import Mock
    bot = Mock()
    bot.token = 'test_token_for_testing'
    return bot


@pytest.fixture
def mock_message():
    """Mock Telegram message"""
    from unittest.mock import Mock
    from aiogram.types import Message, User, Chat
    
    user = User(id=123456789, first_name="Test", last_name="User", username="testuser")
    chat = Chat(id=123456789, type="private")
    
    message = Mock(spec=Message)
    message.from_user = user
    message.chat = chat
    message.text = "/start"
    message.message_id = 1
    
    return message


@pytest.fixture
def mock_callback_query():
    """Mock Telegram callback query"""
    from unittest.mock import Mock
    from aiogram.types import CallbackQuery, User, Message
    
    user = User(id=123456789, first_name="Test", last_name="User", username="testuser")
    message = Message(message_id=1, text="Test message")
    
    callback = Mock(spec=CallbackQuery)
    callback.from_user = user
    callback.message = message
    callback.data = "test_callback"
    callback.id = "test_callback_id"
    
    return callback


@pytest.fixture
def mock_state():
    """Mock FSM state"""
    from unittest.mock import AsyncMock
    state = AsyncMock()
    state.set_state = AsyncMock()
    state.get_data = AsyncMock(return_value={})
    state.update_data = AsyncMock()
    state.clear = AsyncMock()
    return state
