"""
Translation utilities for multilingual support
"""
from typing import Dict, Any, Optional
import json
import os
from ..config.settings import settings

# Translation dictionaries
translations: Dict[str, Dict[str, str]] = {
    "en": {},
    "ru": {}
}


def load_translations():
    """Load translations from JSON files"""
    global translations
    
    # English translations
    translations["en"] = {
        # General
        "welcome": "🌟 Welcome to Application Bot!\n\nThis bot helps you submit applications for various services.\n\nUse /start to begin or /help for available commands.",
        "help": "📋 Available Commands:\n\n" + \
               "/start - Start the bot\n" + \
               "/register - Register as a new user\n" + \
               "/new - Create a new application\n" + \
               "/my_applications - View your applications\n" + \
               "/lang - Change language\n" + \
               "/help - Show this help message\n\n" + \
               "For admins:\n" + \
               "/admin - Admin panel\n",
        "language_changed": "🌐 Language changed to English!",
        "select_language": "🌐 Please select your language:",
        
        # Registration
        "registration_start": "📝 Let's register you!\n\nPlease provide your email address:",
        "registration_email_invalid": "❌ Invalid email format. Please enter a valid email address:",
        "registration_phone": "📞 Now please provide your phone number:",
        "registration_phone_invalid": "❌ Invalid phone format. Please enter a valid phone number:",
        "registration_confirm": "📋 Please confirm your information:\n\nEmail: {email}\nPhone: {phone}\n\nIs this correct? (yes/no)",
        "registration_success": "✅ Registration successful!\n\nYou can now create applications using /new command.",
        "registration_cancelled": "❌ Registration cancelled.",
        
        # Application creation
        "application_start": "📄 Let's create a new application!\n\nPlease select the service type:",
        "application_title": "📝 Please enter a title for your application:",
        "application_description": "📄 Please describe your request (optional):",
        "application_file": "📎 Would you like to attach a file or photo to your application? (yes/no)",
        "application_file_type": "📎 What type of file would you like to upload?",
        "application_file_upload": "📤 Please upload your {file_type}:",
        "application_confirm": "📋 Please confirm your application:\n\n" + \
                            "Service Type: {service_type}\n" + \
                            "Title: {title}\n" + \
                            "Description: {description}\n" + \
                            "File: {file_info}\n\n" + \
                            "Is this correct? (yes/no)",
        "application_submitted": "✅ Application submitted successfully!\n\nYour application ID: {application_id}\nStatus: New\n\nYou can view your applications with /my_applications.",
        "application_cancelled": "❌ Application creation cancelled.",
        
        # File upload
        "file_received": "✅ File received!\n\nFile: {file_name}\nType: {file_type}",
        "file_too_large": "❌ File is too large. Maximum size: 10MB",
        "file_type_not_allowed": "❌ This file type is not allowed.",
        
        # Applications list
        "no_applications": "📭 You have no applications yet.\n\nCreate one with /new command.",
        "your_applications": "📋 Your Applications:\n\n",
        "application_detail": "📄 Application #{id}\n\n" + \
                           "Service Type: {service_type}\n" + \
                           "Title: {title}\n" + \
                           "Description: {description}\n" + \
                           "Status: {status}\n" + \
                           "Created: {created_at}\n" + \
                           "File: {file_info}",
        
        # Status messages
        "status_new": "New",
        "status_in_progress": "In Progress",
        "status_completed": "Completed",
        "status_rejected": "Rejected",
        
        # Admin
        "admin_panel": "🛠️ Admin Panel\n\n" + \
                      "Available commands:\n" + \
                      "/applications - View all applications\n" + \
                      "/users - View all users\n" + \
                      "/set_status - Change application status\n" + \
                      "/broadcast - Send message to all users",
        "admin_only": "❌ This command is only available to administrators.",
        "all_applications": "📊 All Applications:\n\n",
        "application_not_found": "❌ Application not found.",
        "enter_application_id": "🔢 Please enter the application ID:",
        "enter_new_status": "📝 Please select new status:",
        "status_changed": "✅ Application status changed to {status}!",
        "enter_status_notes": "📝 Enter notes for status change (optional):",
        
        # Users
        "all_users": "👥 All Users:\n\n",
        "user_info": "👤 User #{id}\n\n" + \
                    "Telegram ID: {telegram_id}\n" + \
                    "Username: @{username}\n" + \
                    "Name: {name}\n" + \
                    "Email: {email}\n" + \
                    "Phone: {phone}\n" + \
                    "Language: {language}\n" + \
                    "Role: {role}\n" + \
                    "Applications: {app_count}",
        
        # Broadcast
        "broadcast_start": "📢 Enter message to broadcast to all users:",
        "broadcast_confirm": "📢 Confirm broadcast to {count} users:\n\n{message}\n\nSend? (yes/no)",
        "broadcast_sent": "✅ Message sent to {count} users!",
        "broadcast_cancelled": "❌ Broadcast cancelled.",
        
        # Errors
        "error": "❌ An error occurred: {error}",
        "unknown_command": "❌ Unknown command. Use /help for available commands.",
        "not_registered": "❌ You are not registered. Please use /register command first.",
        
        # Buttons
        "btn_yes": "Yes",
        "btn_no": "No",
        "btn_back": "Back",
        "btn_cancel": "Cancel",
        "btn_confirm": "Confirm",
        "btn_next": "Next",
        "btn_skip": "Skip",
        "btn_upload_photo": "Upload Photo",
        "btn_upload_document": "Upload Document",
        "btn_view_applications": "My Applications",
        "btn_new_application": "New Application",
        "btn_help": "Help",
        "btn_language": "Change Language",
        
        # File types
        "file_type_photo": "photo",
        "file_type_document": "document",
        
        # Validation
        "validation_required": "❌ This field is required.",
        "validation_too_short": "❌ Input is too short.",
        "validation_too_long": "❌ Input is too long.",
    }
    
    # Russian translations
    translations["ru"] = {
        # General
        "welcome": "🌟 Добро пожаловать в Application Bot!\n\nЭтот бот помогает вам подавать заявки на различные услуги.\n\nИспользуйте /start для начала или /help для списка команд.",
        "help": "📋 Доступные команды:\n\n" + \
               "/start - Начать работу с ботом\n" + \
               "/register - Зарегистрироваться как новый пользователь\n" + \
               "/new - Создать новую заявку\n" + \
               "/my_applications - Просмотреть свои заявки\n" + \
               "/lang - Изменить язык\n" + \
               "/help - Показать эту справку\n\n" + \
               "Для администраторов:\n" + \
               "/admin - Панель администратора\n",
        "language_changed": "🌐 Язык изменен на русский!",
        "select_language": "🌐 Пожалуйста, выберите язык:",
        
        # Registration
        "registration_start": "📝 Давайте зарегистрируем вас!\n\nПожалуйста, введите ваш email:",
        "registration_email_invalid": "❌ Неверный формат email. Пожалуйста, введите правильный email:",
        "registration_phone": "📞 Теперь пожалуйста введите ваш номер телефона:",
        "registration_phone_invalid": "❌ Неверный формат телефона. Пожалуйста, введите правильный номер:",
        "registration_confirm": "📋 Пожалуйста подтвердите вашу информацию:\n\nEmail: {email}\nТелефон: {phone}\n\nЭто правильно? (да/нет)",
        "registration_success": "✅ Регистрация успешна!\n\nТеперь вы можете создавать заявки с помощью команды /new.",
        "registration_cancelled": "❌ Регистрация отменена.",
        
        # Application creation
        "application_start": "📄 Давайте создадим новую заявку!\n\nПожалуйста, выберите тип услуги:",
        "application_title": "📝 Пожалуйста, введите заголовок для вашей заявки:",
        "application_description": "📄 Пожалуйста, опишите ваш запрос (необязательно):",
        "application_file": "📎 Хотите прикрепить файл или фото к заявке? (да/нет)",
        "application_file_type": "📎 Какой тип файла вы хотите загрузить?",
        "application_file_upload": "📤 Пожалуйста, загрузите ваш {file_type}:",
        "application_confirm": "📋 Пожалуйста подтвердите вашу заявку:\n\n" + \
                            "Тип услуги: {service_type}\n" + \
                            "Заголовок: {title}\n" + \
                            "Описание: {description}\n" + \
                            "Файл: {file_info}\n\n" + \
                            "Это правильно? (да/нет)",
        "application_submitted": "✅ Заявка успешно отправлена!\n\nID вашей заявки: {application_id}\nСтатус: Новая\n\nВы можете просмотреть свои заявки с помощью /my_applications.",
        "application_cancelled": "❌ Создание заявки отменено.",
        
        # File upload
        "file_received": "✅ Файл получен!\n\nФайл: {file_name}\nТип: {file_type}",
        "file_too_large": "❌ Файл слишком большой. Максимальный размер: 10МБ",
        "file_type_not_allowed": "❌ Этот тип файла не разрешен.",
        
        # Applications list
        "no_applications": "📭 У вас пока нет заявок.\n\nСоздайте новую с помощью команды /new.",
        "your_applications": "📋 Ваши заявки:\n\n",
        "application_detail": "📄 Заявка #{id}\n\n" + \
                           "Тип услуги: {service_type}\n" + \
                           "Заголовок: {title}\n" + \
                           "Описание: {description}\n" + \
                           "Статус: {status}\n" + \
                           "Создана: {created_at}\n" + \
                           "Файл: {file_info}",
        
        # Status messages
        "status_new": "Новая",
        "status_in_progress": "В обработке",
        "status_completed": "Завершена",
        "status_rejected": "Отклонена",
        
        # Admin
        "admin_panel": "🛠️ Панель администратора\n\n" + \
                      "Доступные команды:\n" + \
                      "/applications - Просмотреть все заявки\n" + \
                      "/users - Просмотреть всех пользователей\n" + \
                      "/set_status - Изменить статус заявки\n" + \
                      "/broadcast - Отправить сообщение всем пользователям",
        "admin_only": "❌ Эта команда доступна только администраторам.",
        "all_applications": "📊 Все заявки:\n\n",
        "application_not_found": "❌ Заявка не найдена.",
        "enter_application_id": "🔢 Пожалуйста, введите ID заявки:",
        "enter_new_status": "📝 Пожалуйста, выберите новый статус:",
        "status_changed": "✅ Статус заявки изменен на {status}!",
        "enter_status_notes": "📝 Введите комментарий к изменению статуса (необязательно):",
        
        # Users
        "all_users": "👥 Все пользователи:\n\n",
        "user_info": "👤 Пользователь #{id}\n\n" + \
                    "Telegram ID: {telegram_id}\n" + \
                    "Имя пользователя: @{username}\n" + \
                    "Имя: {name}\n" + \
                    "Email: {email}\n" + \
                    "Телефон: {phone}\n" + \
                    "Язык: {language}\n" + \
                    "Роль: {role}\n" + \
                    "Заявок: {app_count}",
        
        # Broadcast
        "broadcast_start": "📢 Введите сообщение для рассылки всем пользователям:",
        "broadcast_confirm": "📢 Подтвердите рассылку {count} пользователям:\n\n{message}\n\nОтправить? (да/нет)",
        "broadcast_sent": "✅ Сообщение отправлено {count} пользователям!",
        "broadcast_cancelled": "❌ Рассылка отменена.",
        
        # Errors
        "error": "❌ Произошла ошибка: {error}",
        "unknown_command": "❌ Неизвестная команда. Используйте /help для списка команд.",
        "not_registered": "❌ Вы не зарегистрированы. Пожалуйста, используйте команду /register.",
        
        # Buttons
        "btn_yes": "Да",
        "btn_no": "Нет",
        "btn_back": "Назад",
        "btn_cancel": "Отмена",
        "btn_confirm": "Подтвердить",
        "btn_next": "Далее",
        "btn_skip": "Пропустить",
        "btn_upload_photo": "Загрузить фото",
        "btn_upload_document": "Загрузить документ",
        "btn_view_applications": "Мои заявки",
        "btn_new_application": "Новая заявка",
        "btn_help": "Помощь",
        "btn_language": "Изменить язык",
        
        # File types
        "file_type_photo": "фото",
        "file_type_document": "документ",
        
        # Validation
        "validation_required": "❌ Это поле обязательно для заполнения.",
        "validation_too_short": "❌ Ввод слишком короткий.",
        "validation_too_long": "❌ Ввод слишком длинный.",
    }


def get_translation(lang: str, key: str, **kwargs) -> str:
    """Get translation for a specific key in the specified language"""
    lang = lang.lower()
    if lang not in translations:
        lang = settings.DEFAULT_LANGUAGE
    
    translation = translations[lang].get(key, translations[settings.DEFAULT_LANGUAGE].get(key, key))
    
    # Format the translation with provided arguments
    if kwargs:
        try:
            return translation.format(**kwargs)
        except KeyError:
            return translation
    
    return translation


def get_text(lang: str, key: str, **kwargs) -> str:
    """Alias for get_translation"""
    return get_translation(lang, key, **kwargs)


def load_translations_from_files():
    """Load translations from JSON files if they exist"""
    global translations
    
    for lang in settings.AVAILABLE_LANGUAGES:
        file_path = f"bot/utils/translations/{lang}.json"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    translations[lang].update(json.load(f))
            except Exception as e:
                print(f"Error loading translations for {lang}: {e}")


# Load translations on module import
load_translations()
load_translations_from_files()
