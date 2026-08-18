"""
Application handlers for creating and managing applications
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..config import settings
from ..database import get_db
from ..database.models import User, Application, ServiceType, ApplicationStatus, ApplicationStatusEnum
from ..states.application import ApplicationState
from ..utils.translations import get_translation, get_button_texts
from ..utils.keyboards import (
    get_service_type_keyboard, get_confirmation_keyboard, 
    get_file_type_keyboard, get_main_keyboard, get_pagination_keyboard
)
from ..utils.file_handler import save_file, delete_file
from ..utils.validators import validate_title, validate_description
from sqlalchemy import select, desc, or_
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("new"))
async def new_application_command(message: Message, state: FSMContext):
    """Handle /new command - start new application"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Check if user is registered
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
        
        if not existing_user or not existing_user.email:
            await message.answer(get_translation(lang, "not_registered"))
            return
        break
    
    # Start application creation
    await state.clear()
    await state.set_state(ApplicationState.waiting_for_service_type)
    
    keyboard = get_service_type_keyboard(lang)
    await message.answer(
        get_translation(lang, "application_start"),
        reply_markup=keyboard
    )


@router.message(F.text.lower().in_(get_button_texts("btn_new_application")))
async def new_application_text(message: Message, state: FSMContext):
    """Handle 'New Application' button press from main menu"""
    await new_application_command(message, state)


@router.callback_query(ApplicationState.waiting_for_service_type, F.data.startswith("service_type:"))
async def select_service_type(callback: CallbackQuery, state: FSMContext):
    """Handle service type selection"""
    user = callback.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    service_type_name = callback.data.split(":")[1]
    
    # Store service type in state
    await state.update_data(service_type_name=service_type_name)
    
    # Ask for title
    await state.set_state(ApplicationState.waiting_for_title)
    await callback.message.edit_text(get_translation(lang, "application_title"))
    await callback.answer()


@router.message(ApplicationState.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    """Process application title"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    title = message.text.strip()
    
    # Validate title
    is_valid, error = validate_title(title)
    if not is_valid:
        await message.answer(error)
        return
    
    # Store title in state
    await state.update_data(title=title)
    
    # Ask for description
    await state.set_state(ApplicationState.waiting_for_description)
    await message.answer(get_translation(lang, "application_description"))


@router.message(ApplicationState.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    """Process application description"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    description = message.text.strip()
    
    # Validate description (optional)
    is_valid, error = validate_description(description)
    if not is_valid:
        await message.answer(error)
        return
    
    # Store description in state
    await state.update_data(description=description)
    
    # Ask if user wants to add file
    await state.set_state(ApplicationState.waiting_for_file)
    await message.answer(get_translation(lang, "application_file"))


@router.message(ApplicationState.waiting_for_file)
async def process_file_choice(message: Message, state: FSMContext):
    """Process file attachment choice"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    answer = message.text.strip().lower()
    
    if answer in [get_translation(lang, "btn_yes").lower(), "yes", "да", "y", "д"]:
        # User wants to add file
        await state.set_state(ApplicationState.waiting_for_file_type)
        keyboard = get_file_type_keyboard(lang)
        await message.answer(
            get_translation(lang, "application_file_type"),
            reply_markup=keyboard
        )
    elif answer in [get_translation(lang, "btn_no").lower(), "no", "нет", "n", "н"]:
        # User doesn't want to add file
        await state.update_data(file_path=None, file_name=None, file_type=None)
        await show_confirmation(message, state)
    else:
        # Invalid answer
        await message.answer(get_translation(lang, "application_file"))


@router.callback_query(ApplicationState.waiting_for_file_type, F.data.startswith("file_type:"))
async def select_file_type(callback: CallbackQuery, state: FSMContext):
    """Handle file type selection"""
    user = callback.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    file_type = callback.data.split(":")[1]
    
    if file_type == "skip":
        # User wants to skip file upload
        await state.update_data(file_path=None, file_name=None, file_type=None)
        await callback.message.edit_text(get_translation(lang, "application_file"))
        await show_confirmation(callback.message, state)
    else:
        # Store file type in state
        await state.update_data(file_type=file_type)
        
        # Ask user to upload file
        file_type_display = get_translation(lang, f"file_type_{file_type}")
        await callback.message.edit_text(
            get_translation(lang, "application_file_upload", file_type=file_type_display)
        )
        
        # Set appropriate state based on file type
        if file_type == "photo":
            await state.set_state(ApplicationState.waiting_for_photo)
        else:
            await state.set_state(ApplicationState.waiting_for_document)
    
    await callback.answer()


@router.message(ApplicationState.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Process uploaded photo"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Get the largest photo
    photo = message.photo[-1]
    
    # Download photo
    file_data = await message.bot.download_photo(photo.file_id)
    
    # Save file
    file_path, file_name = save_file(
        file_data.read(),
        photo.file_name or f"photo_{photo.file_id}.jpg",
        "photo"
    )
    
    # Store file info in state
    await state.update_data(
        file_path=file_path,
        file_name=file_name,
        file_type="photo"
    )
    
    # Confirm file received
    await message.answer(
        get_translation(lang, "file_received", file_name=file_name, file_type="photo")
    )
    
    # Show confirmation
    await show_confirmation(message, state)


@router.message(ApplicationState.waiting_for_document, F.document)
async def process_document(message: Message, state: FSMContext):
    """Process uploaded document"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    document = message.document
    
    # Check file size
    if document.file_size > 10 * 1024 * 1024:  # 10MB
        await message.answer(get_translation(lang, "file_too_large"))
        return
    
    # Download document
    file_data = await message.bot.download_document(document.file_id)
    
    # Save file
    file_path, file_name = save_file(
        file_data.read(),
        document.file_name,
        "document"
    )
    
    # Store file info in state
    await state.update_data(
        file_path=file_path,
        file_name=file_name,
        file_type="document"
    )
    
    # Confirm file received
    await message.answer(
        get_translation(lang, "file_received", file_name=file_name, file_type="document")
    )
    
    # Show confirmation
    await show_confirmation(message, state)


async def show_confirmation(message: Message, state: FSMContext):
    """Show application confirmation"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Get all data from state
    data = await state.get_data()
    service_type_name = data.get("service_type_name", "")
    title = data.get("title", "")
    description = data.get("description", "")
    file_info = data.get("file_name", "No file")
    
    # Get service type ID from database
    service_type_id = None
    async for db in get_db():
        service_type_filter = or_(
            ServiceType.name_en == service_type_name,
            ServiceType.name_ru == service_type_name
        )
        if settings.is_sqlite:
            result = db.execute(
                select(ServiceType).where(service_type_filter)
            )
            service_type = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(ServiceType).where(service_type_filter)
            )
            service_type = result.scalar_one_or_none()
        
        if service_type:
            service_type_id = service_type.id
        break
    
    # Store service type ID in state
    await state.update_data(service_type_id=service_type_id)
    
    # Format confirmation text
    confirm_text = get_translation(
        lang, "application_confirm",
        service_type=service_type_name,
        title=title,
        description=description or "None",
        file_info=file_info
    )
    
    keyboard = get_confirmation_keyboard(lang)
    
    await state.set_state(ApplicationState.waiting_for_confirmation)
    await message.answer(confirm_text, reply_markup=keyboard)


@router.callback_query(ApplicationState.waiting_for_confirmation, F.data.startswith("confirm:"))
async def process_application_confirmation(callback: CallbackQuery, state: FSMContext):
    """Process application submission confirmation"""
    user = callback.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    action = callback.data.split(":")[1]
    
    if action == "yes":
        # Get all data from state
        data = await state.get_data()
        service_type_id = data.get("service_type_id")
        title = data.get("title", "")
        description = data.get("description", "")
        file_path = data.get("file_path")
        file_name = data.get("file_name")
        file_type = data.get("file_type")
        
        # Get user from database
        user_id = None
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
                user_id = existing_user.id
                
                # Create new application
                new_application = Application(
                    user_id=user_id,
                    service_type_id=service_type_id,
                    title=title,
                    description=description,
                    file_path=file_path,
                    file_name=file_name,
                    file_type=file_type,
                    status=ApplicationStatusEnum.NEW
                )
                
                if settings.is_sqlite:
                    db.add(new_application)
                    db.commit()
                    db.refresh(new_application)
                else:
                    db.add(new_application)
                    await db.commit()
                    await db.refresh(new_application)
                
                # Create status history
                new_status = ApplicationStatus(
                    application_id=new_application.id,
                    status=ApplicationStatusEnum.NEW,
                    changed_by=user.id
                )
                
                if settings.is_sqlite:
                    db.add(new_status)
                    db.commit()
                else:
                    db.add(new_status)
                    await db.commit()
                
                application_id = new_application.id
            break
        
        # Send confirmation
        await callback.message.edit_text(
            get_translation(lang, "application_submitted", application_id=application_id),
            reply_markup=None
        )
        
        # Notify admin
        admin_text = f"📄 New Application #{application_id}\n\n" + \
                     f"User: @{user.username} ({user.id})\n" + \
                     f"Title: {title}\n" + \
                     f"Service Type: {data.get('service_type_name', 'Unknown')}"
        
        try:
            await callback.message.bot.send_message(
                settings.ADMIN_ID,
                admin_text
            )
        except Exception as e:
            logger.error(f"Error notifying admin: {e}")
    else:
        # Cancel application
        await callback.message.edit_text(
            get_translation(lang, "application_cancelled"),
            reply_markup=None
        )
        
        # Clean up uploaded file if any
        data = await state.get_data()
        file_path = data.get("file_path")
        if file_path:
            delete_file(file_path)
    
    # Clear state
    await state.clear()
    await callback.answer()


@router.message(Command("my_applications"))
async def my_applications_command(message: Message):
    """Handle /my_applications command"""
    user = message.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    # Get user's applications
    applications = []
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
            if settings.is_sqlite:
                result = db.execute(
                    select(Application)
                    .where(Application.user_id == existing_user.id)
                    .order_by(desc(Application.created_at))
                )
                applications = result.scalars().all()
            else:
                result = await db.execute(
                    select(Application)
                    .where(Application.user_id == existing_user.id)
                    .order_by(desc(Application.created_at))
                )
                applications = result.scalars().all()
        break
    
    if not applications:
        await message.answer(get_translation(lang, "no_applications"))
        return
    
    # Format applications list
    text = get_translation(lang, "your_applications")
    
    for i, app in enumerate(applications[:10], 1):  # Show first 10
        status_text = get_translation(lang, f"status_{app.status.value}")
        text += f"{i}. #{app.id} - {app.title} ({status_text})\n"
    
    keyboard = get_main_keyboard(lang)
    await message.answer(text, reply_markup=keyboard)


@router.message(F.text.lower().in_(get_button_texts("btn_view_applications")))
async def my_applications_text(message: Message):
    """Handle 'My Applications' button press from main menu"""
    await my_applications_command(message)


@router.callback_query(F.data.startswith("view_application:"))
async def view_application_detail(callback: CallbackQuery):
    """View application details"""
    user = callback.from_user
    lang = user.language_code or settings.DEFAULT_LANGUAGE
    if lang not in settings.AVAILABLE_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE
    
    application_id = int(callback.data.split(":")[1])
    
    # Get application details
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
        await callback.answer(get_translation(lang, "application_not_found"))
        return
    
    # Get service type
    service_type_name = "Unknown"
    async for db in get_db():
        if settings.is_sqlite:
            result = db.execute(
                select(ServiceType).where(ServiceType.id == app.service_type_id)
            )
            service_type = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(ServiceType).where(ServiceType.id == app.service_type_id)
            )
            service_type = result.scalar_one_or_none()
        
        if service_type:
            service_type_name = service_type.get_name(lang)
        break
    
    # Format application details
    status_text = get_translation(lang, f"status_{app.status.value}")
    file_info = app.file_name or "No file"
    
    detail_text = get_translation(
        lang, "application_detail",
        id=app.id,
        service_type=service_type_name,
        title=app.title,
        description=app.description or "No description",
        status=status_text,
        created_at=app.created_at.strftime("%Y-%m-%d %H:%M"),
        file_info=file_info
    )
    
    await callback.message.edit_text(detail_text)
    await callback.answer()
