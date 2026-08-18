"""
User registration handlers
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..config import settings
from ..database import get_db
from ..database.models import User
from ..states.registration import RegistrationState
from ..utils.translations import get_translation
from ..utils.keyboards import get_confirmation_keyboard
from ..utils.validators import validate_email, validate_phone
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("register"))
async def register_command(message: Message, state: FSMContext):
    """Handle /register command"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user is already registered
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
        
        if existing_user and existing_user.email:
            # User is already registered
            await message.answer(get_translation(lang, "not_registered"))
            return
        break
    
    # Start registration process
    await state.set_state(RegistrationState.waiting_for_email)
    await message.answer(get_translation(lang, "registration_start"))


@router.message(RegistrationState.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    """Process email input"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    email = message.text.strip()
    
    # Validate email
    is_valid, error = validate_email(email)
    if not is_valid:
        await message.answer(get_translation(lang, "registration_email_invalid"))
        return
    
    # Store email in state
    await state.update_data(email=email)
    
    # Ask for phone
    await state.set_state(RegistrationState.waiting_for_phone)
    await message.answer(get_translation(lang, "registration_phone"))


@router.message(RegistrationState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Process phone input"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    phone = message.text.strip()
    
    # Validate phone
    is_valid, error = validate_phone(phone)
    if not is_valid:
        await message.answer(get_translation(lang, "registration_phone_invalid"))
        return
    
    # Get stored email
    data = await state.get_data()
    email = data.get("email", "")
    
    # Store phone in state
    await state.update_data(phone=phone)
    
    # Show confirmation
    await state.set_state(RegistrationState.waiting_for_confirmation)
    
    confirm_text = get_translation(lang, "registration_confirm", email=email, phone=phone)
    keyboard = get_confirmation_keyboard(lang)
    
    await message.answer(confirm_text, reply_markup=keyboard)


@router.callback_query(RegistrationState.waiting_for_confirmation, F.data.startswith("confirm:"))
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    """Process registration confirmation"""
    user = callback.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    action = callback.data.split(":")[1]
    
    if action == "yes":
        # Get stored data
        data = await state.get_data()
        email = data.get("email", "")
        phone = data.get("phone", "")
        
        # Update user in database
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
                existing_user.email = email
                existing_user.phone = phone
                
                if settings.is_sqlite:
                    db.commit()
                else:
                    await db.commit()
            break
        
        await callback.message.edit_text(
            get_translation(lang, "registration_success"),
            reply_markup=None
        )
    else:
        await callback.message.edit_text(
            get_translation(lang, "registration_cancelled"),
            reply_markup=None
        )
    
    # Clear state
    await state.clear()
    await callback.answer()
