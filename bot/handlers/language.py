"""
Language switching handlers
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..config import settings
from ..database import get_db
from ..database.models import User
from ..states.application import ApplicationState
from ..utils.translations import get_translation, get_button_texts
from ..utils.keyboards import get_language_keyboard, get_main_keyboard
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("lang"))
async def lang_command(message: Message, state: FSMContext):
    """Handle /lang command"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Get current user language from database
    current_lang = lang
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        
        if existing_user and existing_user.language:
            current_lang = existing_user.language
        break
    
    keyboard = get_language_keyboard(current_lang)
    await message.answer(
        get_translation(lang, "select_language"),
        reply_markup=keyboard
    )
    
    # Set state for language selection
    await state.set_state(ApplicationState.waiting_for_language)


@router.message(F.text.lower().in_(get_button_texts("btn_language")))
async def lang_text(message: Message, state: FSMContext):
    """Handle 'Change Language' button press from main menu"""
    await lang_command(message, state)


@router.callback_query(ApplicationState.waiting_for_language, F.data.startswith("lang:"))
async def select_language(callback: CallbackQuery, state: FSMContext):
    """Handle language selection"""
    user = callback.from_user
    new_lang = callback.data.split(":")[1]
    
    if new_lang not in settings.AVAILABLE_LANGUAGES:
        await callback.answer("Invalid language")
        return
    
    # Update user language in database
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        
        if existing_user:
            existing_user.language = new_lang
            if settings.is_sqlite:
                db.commit()
            else:
                await db.commit()
        break
    
    # Show confirmation
    if new_lang == "en":
        confirm_text = get_translation("en", "language_changed")
    else:
        confirm_text = get_translation("ru", "language_changed")
    
    keyboard = get_main_keyboard(new_lang)
    await callback.message.edit_text(confirm_text, reply_markup=keyboard)
    
    # Clear state
    await state.clear()
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def select_language_direct(callback: CallbackQuery):
    """Handle language selection from other contexts"""
    user = callback.from_user
    new_lang = callback.data.split(":")[1]
    
    if new_lang not in settings.AVAILABLE_LANGUAGES:
        await callback.answer("Invalid language")
        return
    
    # Update user language in database
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        
        if existing_user:
            existing_user.language = new_lang
            if settings.is_sqlite:
                db.commit()
            else:
                await db.commit()
        break
    
    # Show confirmation
    if new_lang == "en":
        confirm_text = get_translation("en", "language_changed")
    else:
        confirm_text = get_translation("ru", "language_changed")
    
    keyboard = get_main_keyboard(new_lang)
    await callback.message.edit_text(confirm_text, reply_markup=keyboard)
    await callback.answer()
