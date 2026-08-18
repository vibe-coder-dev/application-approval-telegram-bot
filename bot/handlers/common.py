"""
Common handlers for the bot
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from ..config import settings
from ..database import get_db
from ..database.models import User
from ..utils.translations import get_translation, get_button_texts
from ..utils.keyboards import get_main_keyboard
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("help"))
async def help_command(message: Message):
    """Handle /help command"""
    lang = message.from_user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    help_text = get_translation(lang, "help")
    await message.answer(help_text)


@router.message(F.text.lower().in_(get_button_texts("btn_help")))
async def help_text(message: Message):
    """Handle 'Help' button press from main menu"""
    await help_command(message)


@router.message(Command("start"))
async def start_command(message: Message):
    """Handle /start command - redirect to main start handler"""
    # This is here to ensure /start is always available
    lang = message.from_user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    welcome_text = get_translation(lang, "welcome")
    keyboard = get_main_keyboard(lang)
    
    await message.answer(welcome_text, reply_markup=keyboard)


@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery):
    """Handle cancel button press"""
    lang = callback.from_user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    await callback.message.edit_text(
        get_translation(lang, "application_cancelled"),
        reply_markup=None
    )
    await callback.answer()


@router.callback_query(F.data == "no_action")
async def no_action(callback: CallbackQuery):
    """Handle no action callback (for pagination indicators)"""
    await callback.answer()


@router.message(F.text.lower() == "cancel")
async def cancel_text(message: Message):
    """Handle cancel text command"""
    lang = message.from_user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    await message.answer(get_translation(lang, "application_cancelled"))
