"""
Start command handler
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ..config import settings
from ..database import get_db
from ..database.models import User, UserRole
from ..utils.translations import get_translation
from ..utils.keyboards import get_main_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    """Handle /start command"""
    user = message.from_user
    logger.info(f"Received /start from user_id={user.id}, username={user.username}")
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user exists in database
    async for db in get_db():
        if settings.is_sqlite:
            # Sync session
            result = db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        else:
            # Async session
            result = await db.execute(
                select(User).where(User.telegram_id == user.id)
            )
            existing_user = result.scalar_one_or_none()
        
        role = UserRole.ADMIN if user.id == settings.ADMIN_ID else UserRole.USER
        
        if not existing_user:
            # Create new user
            new_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language=lang,
                role=role
            )
            
            if settings.is_sqlite:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
            else:
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)
            
            logger.info(f"New user registered: {user.id}")
        else:
            # Update user info
            existing_user.username = user.username
            existing_user.first_name = user.first_name
            existing_user.last_name = user.last_name
            if existing_user.role != role:
                existing_user.role = role
            
            if settings.is_sqlite:
                db.commit()
            else:
                await db.commit()
        
        break  # Exit async loop after first iteration
    
    welcome_text = get_translation(lang, "welcome")
    keyboard = get_main_keyboard(lang)
    
    await message.answer(welcome_text, reply_markup=keyboard)


@router.message(F.text.lower() == "start")
async def start_text_handler(message: Message):
    """Handle 'start' text message"""
    await start_handler(message)
