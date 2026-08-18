"""
Admin handlers for managing applications and users
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..config import settings
from ..database import get_db
from ..database.models import User, Application, ServiceType, ApplicationStatus, ApplicationStatusEnum, UserRole
from ..states.admin import AdminState
from ..utils.translations import get_translation
from ..utils.keyboards import (
    get_admin_keyboard, get_status_keyboard, 
    get_confirmation_keyboard, get_pagination_keyboard
)
from sqlalchemy import select, desc
import logging

logger = logging.getLogger(__name__)

router = Router()


async def check_admin(user_id: int) -> bool:
    """Check if user is admin"""
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = result.scalar_one_or_none()
        
        if user and user.role == UserRole.ADMIN:
            return True
        break
    return False


@router.message(Command("admin"))
async def admin_panel_command(message: Message):
    """Handle /admin command"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user is admin
    is_admin = await check_admin(user.id)
    if not is_admin:
        await message.answer(get_translation(lang, "admin_only"))
        return
    
    keyboard = get_admin_keyboard(lang)
    await message.answer(
        get_translation(lang, "admin_panel"),
        reply_markup=keyboard
    )


@router.message(Command("applications"))
async def view_all_applications_command(message: Message):
    """Handle /applications command - view all applications"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user is admin
    is_admin = await check_admin(user.id)
    if not is_admin:
        await message.answer(get_translation(lang, "admin_only"))
        return
    
    # Get all applications
    applications = []
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(Application)
                .order_by(desc(Application.created_at))
                .limit(10)
            )
            applications = result.scalars().all()
        else:
            result = await db.execute(
                select(Application)
                .order_by(desc(Application.created_at))
                .limit(10)
            )
            applications = result.scalars().all()
        break
    
    if not applications:
        await message.answer(get_translation(lang, "no_applications"))
        return
    
    # Format applications list
    text = get_translation(lang, "all_applications")
    
    for i, app in enumerate(applications, 1):
        status_text = get_translation(lang, f"status_{app.status.value}")
        text += f"{i}. #{app.id} - {app.title} ({status_text})\n"
    
    keyboard = get_admin_keyboard(lang)
    await message.answer(text, reply_markup=keyboard)


@router.message(Command("users"))
async def view_all_users_command(message: Message):
    """Handle /users command - view all users"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user is admin
    is_admin = await check_admin(user.id)
    if not is_admin:
        await message.answer(get_translation(lang, "admin_only"))
        return
    
    # Get all users
    users = []
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(User)
                .order_by(desc(User.created_at))
                .limit(10)
            )
            users = result.scalars().all()
        else:
            result = await db.execute(
                select(User)
                .order_by(desc(User.created_at))
                .limit(10)
            )
            users = result.scalars().all()
        break
    
    if not users:
        await message.answer(get_translation(lang, "no_applications"))
        return
    
    # Format users list
    text = get_translation(lang, "all_users")
    
    for i, user_obj in enumerate(users, 1):
        name = f"{user_obj.first_name or ''} {user_obj.last_name or ''}".strip()
        if not name:
            name = f"@{user_obj.username or 'unknown'}"
        text += f"{i}. {name} (@{user_obj.username or 'no_username'}) - {user_obj.role.value}\n"
    
    keyboard = get_admin_keyboard(lang)
    await message.answer(text, reply_markup=keyboard)


@router.message(Command("set_status"))
async def set_status_command(message: Message, state: FSMContext):
    """Handle /set_status command - change application status"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user is admin
    is_admin = await check_admin(user.id)
    if not is_admin:
        await message.answer(get_translation(lang, "admin_only"))
        return
    
    await state.set_state(AdminState.waiting_for_application_id)
    await message.answer(get_translation(lang, "enter_application_id"))


@router.message(AdminState.waiting_for_application_id)
async def process_application_id(message: Message, state: FSMContext):
    """Process application ID input"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    try:
        application_id = int(message.text.strip())
    except ValueError:
        await message.answer(get_translation(lang, "application_not_found"))
        return
    
    # Check if application exists
    app = None
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(Application).where(Application.id == application_id)
            )
            app = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(Application).where(Application.id == application_id)
            )
            app = result.scalar_one_or_none()
        break
    
    if not app:
        await message.answer(get_translation(lang, "application_not_found"))
        return
    
    # Store application ID in state
    await state.update_data(application_id=application_id)
    
    # Ask for new status
    await state.set_state(AdminState.waiting_for_new_status)
    keyboard = get_status_keyboard(lang)
    await message.answer(
        get_translation(lang, "enter_new_status"),
        reply_markup=keyboard
    )


@router.callback_query(AdminState.waiting_for_new_status, F.data.startswith("status:"))
async def select_new_status(callback: CallbackQuery, state: FSMContext):
    """Handle new status selection"""
    user = callback.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    new_status_value = callback.data.split(":")[1]
    
    # Validate status
    try:
        new_status = ApplicationStatusEnum(new_status_value)
    except ValueError:
        await callback.answer("Invalid status")
        return
    
    # Store new status in state
    await state.update_data(new_status=new_status)
    
    # Ask for notes
    await state.set_state(AdminState.waiting_for_status_notes)
    await callback.message.edit_text(get_translation(lang, "enter_status_notes"))
    await callback.answer()


@router.message(AdminState.waiting_for_status_notes)
async def process_status_notes(message: Message, state: FSMContext):
    """Process status change notes"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    notes = message.text.strip()
    
    # Get data from state
    data = await state.get_data()
    application_id = data.get("application_id")
    new_status = data.get("new_status")
    
    if not application_id or not new_status:
        await message.answer(get_translation(lang, "error", error="Missing data"))
        await state.clear()
        return
    
    # Update application status
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(Application).where(Application.id == application_id)
            )
            app = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(Application).where(Application.id == application_id)
            )
            app = result.scalar_one_or_none()
        
        if app:
            old_status = app.status
            app.status = new_status
            
            if settings.is_sqlite:
                db.commit()
            else:
                await db.commit()
            
            # Create status history record
            new_status_history = ApplicationStatus(
                application_id=application_id,
                status=new_status,
                changed_by=user.id,
                notes=notes if notes else None
            )
            
            if settings.is_sqlite:
                db.add(new_status_history)
                db.commit()
            else:
                db.add(new_status_history)
                await db.commit()
        break
    
    # Show confirmation
    status_text = get_translation(lang, f"status_{new_status.value}")
    await message.answer(
        get_translation(lang, "status_changed", status=status_text)
    )
    
    # Notify user if status changed
    if app:
        # Get user info
        async for db in get_db():
            if settings.is_sqlite:
                result = db.execute(
                    select(User).where(User.id == app.user_id)
                )
                user_obj = result.scalar_one_or_none()
            else:
                result = await db.execute(
                    select(User).where(User.id == app.user_id)
                )
                user_obj = result.scalar_one_or_none()
            
            if user_obj:
                try:
                    user_lang = user_obj.language or "en"
                    status_text_user = get_translation(user_lang, f"status_{new_status.value}")
                    notification = get_translation(
                        user_lang, "status_changed", 
                        status=status_text_user
                    ) + f"\n\nApplication ID: {application_id}"
                    
                    if notes:
                        notification += f"\nNotes: {notes}"
                    
                    await message.bot.send_message(
                        user_obj.telegram_id,
                        notification
                    )
                except Exception as e:
                    logger.error(f"Error notifying user: {e}")
            break
    
    # Clear state
    await state.clear()


@router.message(Command("broadcast"))
async def broadcast_command(message: Message, state: FSMContext):
    """Handle /broadcast command"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user is admin
    is_admin = await check_admin(user.id)
    if not is_admin:
        await message.answer(get_translation(lang, "admin_only"))
        return
    
    await state.set_state(AdminState.waiting_for_broadcast_message)
    await message.answer(get_translation(lang, "broadcast_start"))


@router.message(AdminState.waiting_for_broadcast_message)
async def process_broadcast_message(message: Message, state: FSMContext):
    """Process broadcast message"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    broadcast_message = message.text
    
    # Get all users
    users = []
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(select(User))
            users = result.scalars().all()
        else:
            result = await db.execute(select(User))
            users = result.scalars().all()
        break
    
    if not users:
        await message.answer(get_translation(lang, "no_applications"))
        await state.clear()
        return
    
    # Store message in state
    await state.update_data(broadcast_message=broadcast_message)
    
    # Show confirmation
    confirm_text = get_translation(
        lang, "broadcast_confirm",
        count=len(users),
        message=broadcast_message
    )
    keyboard = get_confirmation_keyboard(lang)
    
    await state.set_state(AdminState.waiting_for_broadcast_message)
    await message.answer(confirm_text, reply_markup=keyboard)


@router.callback_query(AdminState.waiting_for_broadcast_message, F.data.startswith("confirm:"))
async def process_broadcast_confirmation(callback: CallbackQuery, state: FSMContext):
    """Process broadcast confirmation"""
    user = callback.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    action = callback.data.split(":")[1]
    
    if action == "yes":
        # Get message from state
        data = await state.get_data()
        broadcast_message = data.get("broadcast_message", "")
        
        # Get all users
        users = []
        async for db in get_db():
            if settings.is_sqlite:
                result = db.execute(select(User))
                users = result.scalars().all()
            else:
                result = await db.execute(select(User))
                users = result.scalars().all()
            break
        
        # Send message to all users
        sent_count = 0
        for user_obj in users:
            try:
                await callback.message.bot.send_message(
                    user_obj.telegram_id,
                    broadcast_message
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Error sending broadcast to {user_obj.telegram_id}: {e}")
        
        await callback.message.edit_text(
            get_translation(lang, "broadcast_sent", count=sent_count),
            reply_markup=None
        )
    else:
        await callback.message.edit_text(
            get_translation(lang, "broadcast_cancelled"),
            reply_markup=None
        )
    
    # Clear state
    await state.clear()
    await callback.answer()
