"""
Keyboard utilities for creating inline and reply keyboards
"""
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from typing import List, Dict, Any, Optional
from ..config.settings import settings
from ..database.models import ApplicationStatusEnum
from .translations import get_translation


def get_main_keyboard(lang: str = "en") -> ReplyKeyboardMarkup:
    """Get main menu keyboard"""
    builder = ReplyKeyboardBuilder()
    
    # Add buttons based on translations
    btn_new = get_translation(lang, "btn_new_application")
    btn_my_apps = get_translation(lang, "btn_view_applications")
    btn_help = get_translation(lang, "btn_help")
    btn_lang = get_translation(lang, "btn_language")
    
    builder.add(KeyboardButton(text=btn_new))
    builder.add(KeyboardButton(text=btn_my_apps))
    builder.add(KeyboardButton(text=btn_help))
    builder.add(KeyboardButton(text=btn_lang))
    
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_admin_keyboard(lang: str = "en") -> ReplyKeyboardMarkup:
    """Get admin menu keyboard"""
    builder = ReplyKeyboardBuilder()
    
    btn_applications = get_translation(lang, "btn_view_applications")
    btn_users = "Users"
    btn_set_status = "Set Status"
    btn_broadcast = "Broadcast"
    btn_back = get_translation(lang, "btn_back")
    
    builder.add(KeyboardButton(text=btn_applications))
    builder.add(KeyboardButton(text=btn_users))
    builder.add(KeyboardButton(text=btn_set_status))
    builder.add(KeyboardButton(text=btn_broadcast))
    builder.add(KeyboardButton(text=btn_back))
    
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_service_type_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Get keyboard with service types"""
    builder = InlineKeyboardBuilder()
    
    service_types = settings.SERVICE_TYPES.get(lang, settings.SERVICE_TYPES["en"])
    
    for service_type in service_types:
        builder.add(InlineKeyboardButton(
            text=service_type,
            callback_data=f"service_type:{service_type}"
        ))
    
    # Add cancel button
    btn_cancel = get_translation(lang, "btn_cancel")
    builder.add(InlineKeyboardButton(
        text=btn_cancel,
        callback_data="cancel"
    ))
    
    builder.adjust(2)
    return builder.as_markup()


def get_status_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Get keyboard with application statuses"""
    builder = InlineKeyboardBuilder()
    
    statuses = settings.APPLICATION_STATUSES.get(lang, settings.APPLICATION_STATUSES["en"])
    
    for status in statuses:
        # Map display name to enum value
        status_enum_map = {
            "New": ApplicationStatusEnum.NEW,
            "In Progress": ApplicationStatusEnum.IN_PROGRESS,
            "Completed": ApplicationStatusEnum.COMPLETED,
            "Rejected": ApplicationStatusEnum.REJECTED,
            "Новая": ApplicationStatusEnum.NEW,
            "В обработке": ApplicationStatusEnum.IN_PROGRESS,
            "Завершена": ApplicationStatusEnum.COMPLETED,
            "Отклонена": ApplicationStatusEnum.REJECTED,
        }
        
        enum_value = status_enum_map.get(status, ApplicationStatusEnum.NEW)
        
        builder.add(InlineKeyboardButton(
            text=status,
            callback_data=f"status:{enum_value.value}"
        ))
    
    # Add cancel button
    btn_cancel = get_translation(lang, "btn_cancel")
    builder.add(InlineKeyboardButton(
        text=btn_cancel,
        callback_data="cancel"
    ))
    
    builder.adjust(2)
    return builder.as_markup()


def get_language_keyboard(current_lang: str = "en") -> InlineKeyboardMarkup:
    """Get keyboard for language selection"""
    builder = InlineKeyboardBuilder()
    
    for lang in settings.AVAILABLE_LANGUAGES:
        lang_name = {"en": "English", "ru": "Русский"}.get(lang, lang)
        
        # Add checkmark for current language
        if lang == current_lang:
            lang_name = f"✅ {lang_name}"
        
        builder.add(InlineKeyboardButton(
            text=lang_name,
            callback_data=f"lang:{lang}"
        ))
    
    builder.adjust(2)
    return builder.as_markup()


def get_confirmation_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Get yes/no confirmation keyboard"""
    builder = InlineKeyboardBuilder()
    
    btn_yes = get_translation(lang, "btn_yes")
    btn_no = get_translation(lang, "btn_no")
    
    builder.add(InlineKeyboardButton(
        text=btn_yes,
        callback_data="confirm:yes"
    ))
    builder.add(InlineKeyboardButton(
        text=btn_no,
        callback_data="confirm:no"
    ))
    
    return builder.as_markup()


def get_file_type_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Get keyboard for file type selection"""
    builder = InlineKeyboardBuilder()
    
    btn_photo = get_translation(lang, "btn_upload_photo")
    btn_document = get_translation(lang, "btn_upload_document")
    btn_skip = get_translation(lang, "btn_skip")
    
    builder.add(InlineKeyboardButton(
        text=btn_photo,
        callback_data="file_type:photo"
    ))
    builder.add(InlineKeyboardButton(
        text=btn_document,
        callback_data="file_type:document"
    ))
    builder.add(InlineKeyboardButton(
        text=btn_skip,
        callback_data="file_type:skip"
    ))
    
    builder.adjust(2)
    return builder.as_markup()


def get_application_actions_keyboard(application_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    """Get keyboard with actions for an application"""
    builder = InlineKeyboardBuilder()
    
    btn_view = get_translation(lang, "btn_next")
    btn_back = get_translation(lang, "btn_back")
    
    builder.add(InlineKeyboardButton(
        text=btn_view,
        callback_data=f"view_application:{application_id}"
    ))
    builder.add(InlineKeyboardButton(
        text=btn_back,
        callback_data="back_to_applications"
    ))
    
    return builder.as_markup()


def get_pagination_keyboard(
    page: int,
    total_pages: int,
    prefix: str = "",
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Get pagination keyboard"""
    builder = InlineKeyboardBuilder()
    
    btn_back = get_translation(lang, "btn_back")
    btn_next = get_translation(lang, "btn_next")
    
    # Previous button
    if page > 1:
        builder.add(InlineKeyboardButton(
            text=btn_back,
            callback_data=f"{prefix}:{page - 1}"
        ))
    
    # Page indicator
    builder.add(InlineKeyboardButton(
        text=f"{page}/{total_pages}",
        callback_data="no_action"
    ))
    
    # Next button
    if page < total_pages:
        builder.add(InlineKeyboardButton(
            text=btn_next,
            callback_data=f"{prefix}:{page + 1}"
        ))
    
    builder.adjust(3)
    return builder.as_markup()
