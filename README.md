# Application Bot

> **🌐 [Русская версия ниже](#русский)**

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Quick Start](#quick-start)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [User Commands](#user-commands)
  - [Web Admin Panel](#web-admin-panel)
- [Project Structure](#project-structure)
- [Docker](#docker)
- [Development](#development)
- [License](#license)

---

## 🔍 About

**Application Bot** is a Telegram bot designed for managing client applications. It provides a complete workflow for users to submit applications for various services, with support for file attachments, status tracking, and multilingual interface.

The bot is built with modern Python technologies and supports both SQLite (for development) and PostgreSQL (for production) databases.

---

## ✨ Features

### User Features
- **User Registration**: Clients can register with email and phone
- **Step-by-Step Form**: Guided application creation using FSM (Finite State Machine)
- **Service Type Selection**: Choose from predefined service types
- **File/Photo Upload**: Attach files or photos to applications
- **Application Submission**: Submit applications to administrators
- **Status Tracking**: View application status and history
- **Multilingual Support**: Switch between English and Russian with `/lang` command

### Admin Features
- **Web Admin Panel**: Flask-based admin panel at `http://localhost:10000`
- **Application Management**: View all applications and change their status
- **User Management**: View registered users
- **Status Updates**: Change application status with optional notes
- **Broadcast Messages**: Send messages to all registered users
- **Notifications**: Receive notifications for new applications

### Technical Features
- **FSM (Finite State Machine)**: Structured conversation flow
- **Database Support**: SQLite and PostgreSQL
- **Docker Ready**: Complete containerization support
- **Async/Await**: Fully asynchronous codebase
- **Error Handling**: Comprehensive error handling and validation

---

## 🛠️ Technologies

- **Python 3.11+**
- **Aiogram 3.4** - Modern Telegram Bot Framework
- **Flask** - Web admin panel framework
- **SQLAlchemy 2.0** - ORM for database operations
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Docker** - Containerization
- **Pydantic** - Data validation and settings management

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- PostgreSQL (optional, for production)

### Quick Start

#### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/vibe-coder-dev/application-bot.git
   cd application-bot
   ```

2. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` file with your configuration:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=your_telegram_user_id
   ADMIN_PASSWORD=your_admin_panel_password
   DB_TYPE=postgresql
   POSTGRES_PASSWORD=your_password
   ```

4. Start the services:
   ```bash
   docker-compose up -d
   ```

5. The bot should now be running and ready to use!

6. Open the web admin panel at `http://localhost:10000` and log in with `ADMIN_PASSWORD`.

#### Local Development

1. Clone the repository and navigate to the project directory

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your configuration

5. Run the bot:
   ```bash
   python -m bot.main
   ```

6. Run the web admin panel (in a separate terminal):
   ```bash
   python run_admin.py
   ```
   The admin panel is then available at `http://localhost:10000`.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram Bot Token (required) | - |
| `ADMIN_ID` | Admin Telegram User ID (required) | - |
| `ADMIN_PASSWORD` | Web admin panel password | `admin` |
| `SECRET_KEY` | Flask session secret key | `change-me` |
| `DB_TYPE` | Database type: `sqlite` or `postgresql` | `postgresql` |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | PostgreSQL database name | `application_bot` |
| `POSTGRES_USER` | PostgreSQL username | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `postgres` |
| `SQLite_DB_PATH` | SQLite database path | `data/bot.db` |
| `UPLOAD_DIR` | Directory for uploaded files | `uploads` |
| `DEFAULT_LANGUAGE` | Default language | `en` |
| `AVAILABLE_LANGUAGES` | Available languages (comma separated) | `en,ru` |

### Service Types

Service types are predefined in the configuration and can be extended by modifying the `SERVICE_TYPES` setting in `bot/config/settings.py`.

### Application Statuses

Application statuses are managed through the `ApplicationStatusEnum` and can be customized in `bot/database/models.py`.

---

## 💬 Usage

### User Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show welcome message |
| `/help` | Show available commands and help |
| `/register` | Register as a new user (email and phone required) |
| `/new` | Create a new application |
| `/my_applications` | View your submitted applications |
| `/lang` | Change language (English/Russian) |

### Web Admin Panel

The admin panel is a Flask web application that runs at `http://localhost:10000`. It is protected by a password (see `ADMIN_PASSWORD` in `.env`).

| Page | Description |
|------|-------------|
| Dashboard | User/application statistics, status counts and broadcast form |
| `/applications` | View all applications, filter by status |
| `/applications/<id>` | Application details, status history and status change |
| `/users` | View all registered users |

### Application Creation Flow

1. User starts with `/new` command
2. Select service type from available options
3. Enter application title
4. Enter description (optional)
5. Choose to add file/photo or skip
6. If adding file: select type (photo/document) and upload
7. Confirm all information
8. Application is submitted and admin is notified

### Status Management

Admins change application status through the web admin panel at `http://localhost:10000/applications/<id>`:
1. Open the application detail page
2. Select the new status from the dropdown
3. Add optional notes
4. Save; the user is notified about the status change via Telegram

---

## 📁 Project Structure

```
application/
├── bot/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py      # Configuration and settings
│   │   └── bot.py           # Bot instance configuration
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py        # Database models
│   │   └── database.py      # Database connection and session management
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py         # Start command handler
│   │   ├── registration.py  # User registration handlers
│   │   ├── application.py   # Application creation handlers
│   │   ├── language.py      # Language switching handlers
│   │   └── common.py        # Common handlers
│   ├── states/
│   │   ├── __init__.py
│   │   ├── application.py   # Application FSM states
│   │   └── registration.py  # Registration FSM states
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── translations.py  # Translation utilities
│   │   ├── keyboards.py     # Keyboard utilities
│   │   ├── file_handler.py  # File handling utilities
│   │   └── validators.py    # Input validation utilities
│   └── main.py              # Main entry point
├── webadmin/
│   ├── __init__.py
│   ├── app.py               # Flask web admin panel
│   ├── templates/           # HTML templates
│   └── static/              # Static assets (CSS)
├── run_admin.py             # Web admin panel entry point
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🐳 Docker

### Building the Image

```bash
docker build -t application-bot .
```

### Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f bot webadmin

# Restart bot
docker-compose restart bot
```

### Using SQLite (Development)

To use SQLite instead of PostgreSQL:

1. Edit `.env` file:
   ```env
   DB_TYPE=sqlite
   ```

2. Start only the bot and web admin services:
   ```bash
   docker-compose up -d bot webadmin
   ```

---

## 👨‍💻 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Code Style

```bash
# Format code with black
black bot/

# Lint with flake8
flake8 bot/
```

### Adding New Features

1. Create new handler files in `bot/handlers/`
2. Add new states in `bot/states/` if needed
3. Update routers in `bot/main.py`
4. Add translations in `bot/utils/translations.py`
5. Update database models if needed

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# Русский

## 📋 Оглавление

- [О проекте](#о-проекте)
- [Возможности](#возможности)
- [Технологии](#технологии-1)
- [Установка](#установка)
  - [Требования](#требования)
  - [Быстрый старт](#быстрый-старт)
  - [Конфигурация](#конфигурация-1)
- [Использование](#использование)
  - [Команды пользователя](#команды-пользователя)
  - [Веб-панель администратора](#веб-панель-администратора)
- [Структура проекта](#структура-проекта)
- [Docker](#docker-1)
- [Разработка](#разработка)
- [Лицензия](#лицензия)

---

## 🔍 О проекте

**Application Bot** - это Telegram бот для управления заявками от клиентов. Он предоставляет полный рабочий процесс для подачи заявок на различные услуги, с поддержкой прикрепления файлов, отслеживания статуса и многоязычного интерфейса.

Бот разработан на современных Python технологиях и поддерживает как SQLite (для разработки), так и PostgreSQL (для продакшена) базы данных.

---

## ✨ Возможности

### Возможности для пользователей
- **Регистрация пользователей**: Клиенты могут зарегистрироваться, указав email и телефон
- **Пошаговая форма**: Создание заявки с помощью FSM (Конечный автомат)
- **Выбор типа услуги**: Выбор из предопределенных типов услуг
- **Загрузка файлов/фото**: Прикрепление файлов или фото к заявкам
- **Отправка заявки**: Отправка заявок администраторам
- **Отслеживание статуса**: Просмотр статуса и истории заявки
- **Многоязычная поддержка**: Переключение между английским и русским языками с помощью команды `/lang`

### Возможности для администраторов
- **Веб-панель администратора**: Flask-панель по адресу `http://localhost:10000`
- **Управление заявками**: Просмотр всех заявок и изменение их статуса
- **Управление пользователями**: Просмотр зарегистрированных пользователей
- **Обновление статуса**: Изменение статуса заявки с добавлением комментариев
- **Рассылка сообщений**: Отправка сообщений всем зарегистрированным пользователям
- **Уведомления**: Получение уведомлений о новых заявках

### Технические возможности
- **FSM (Конечный автомат)**: Структурированный поток диалога
- **Поддержка баз данных**: SQLite и PostgreSQL
- **Готовность к Docker**: Полная поддержка контейнеризации
- **Асинхронность**: Полностью асинхронный код
- **Обработка ошибок**: Всесторонняя обработка ошибок и валидация

---

## 🛠️ Технологии

- **Python 3.11+**
- **Aiogram 3.4** - Современный фреймворк для Telegram ботов
- **Flask** - Фреймворк веб-панели администратора
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **PostgreSQL** - Продакшен база данных
- **SQLite** - База данных для разработки
- **Docker** - Контейнеризация
- **Pydantic** - Валидация данных и управление настройками

---

## 🚀 Установка

### Требования

- Python 3.11 или выше
- Docker и Docker Compose (для контейнеризованного развертывания)
- Токен Telegram бота (получить у [@BotFather](https://t.me/BotFather))
- PostgreSQL (опционально, для продакшена)

### Быстрый старт

#### С использованием Docker (Рекомендуется)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/vibe-coder-dev/application-bot.git
   cd application-bot
   ```

2. Создайте файл `.env` из шаблона:
   ```bash
   cp .env.example .env
   ```

3. Отредактируйте файл `.env` с вашей конфигурацией:
   ```env
   BOT_TOKEN=ваш_токен_телеграм_бота
   ADMIN_ID=ваш_telegram_id
   ADMIN_PASSWORD=пароль_для_панели_администратора
   DB_TYPE=postgresql
   POSTGRES_PASSWORD=ваш_пароль
   ```

4. Запустите сервисы:
   ```bash
   docker-compose up -d
   ```

5. Бот должен быть запущен и готов к использованию!

6. Откройте веб-панель администратора по адресу `http://localhost:10000` и войдите, используя `ADMIN_PASSWORD`.

#### Локальная разработка

1. Клонируйте репозиторий и перейдите в директорию проекта

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # На Windows: .venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` с вашей конфигурацией

5. Запустите бота:
   ```bash
   python -m bot.main
   ```

6. Запустите веб-панель администратора (в отдельном терминале):
   ```bash
   python run_admin.py
   ```
   Панель администратора будет доступна по адресу `http://localhost:10000`.

---

## ⚙️ Конфигурация

### Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `BOT_TOKEN` | Токен Telegram бота (обязательно) | - |
| `ADMIN_ID` | Telegram ID администратора (обязательно) | - |
| `ADMIN_PASSWORD` | Пароль веб-панели администратора | `admin` |
| `SECRET_KEY` | Секретный ключ сессий Flask | `change-me` |
| `DB_TYPE` | Тип базы данных: `sqlite` или `postgresql` | `postgresql` |
| `POSTGRES_HOST` | Хост PostgreSQL | `localhost` |
| `POSTGRES_PORT` | Порт PostgreSQL | `5432` |
| `POSTGRES_DB` | Имя базы данных PostgreSQL | `application_bot` |
| `POSTGRES_USER` | Имя пользователя PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `postgres` |
| `SQLite_DB_PATH` | Путь к базе данных SQLite | `data/bot.db` |
| `UPLOAD_DIR` | Директория для загруженных файлов | `uploads` |
| `DEFAULT_LANGUAGE` | Язык по умолчанию | `en` |
| `AVAILABLE_LANGUAGES` | Доступные языки (через запятую) | `en,ru` |

### Типы услуг

Типы услуг предопределены в конфигурации и могут быть расширены путем изменения настройки `SERVICE_TYPES` в файле `bot/config/settings.py`.

### Статусы заявок

Статусы заявок управляются через `ApplicationStatusEnum` и могут быть настроены в файле `bot/database/models.py`.

---

## 💬 Использование

### Команды пользователя

| Команда | Описание |
|---------|----------|
| `/start` | Начать работу с ботом и показать приветственное сообщение |
| `/help` | Показать доступные команды и справку |
| `/register` | Зарегистрироваться как новый пользователь (требуются email и телефон) |
| `/new` | Создать новую заявку |
| `/my_applications` | Просмотреть свои поданные заявки |
| `/lang` | Изменить язык (Английский/Русский) |

### Веб-панель администратора

Панель администратора - это Flask веб-приложение, которое работает по адресу `http://localhost:10000`. Она защищена паролем (см. `ADMIN_PASSWORD` в файле `.env`).

| Страница | Описание |
|----------|----------|
| Дашборд | Статистика пользователей/заявок, количество по статусам и форма рассылки |
| `/applications` | Просмотр всех заявок, фильтрация по статусу |
| `/applications/<id>` | Детали заявки, история статусов и изменение статуса |
| `/users` | Просмотр всех зарегистрированных пользователей |

### Процесс создания заявки

1. Пользователь начинает с команды `/new`
2. Выбирает тип услуги из доступных вариантов
3. Вводит заголовок заявки
4. Вводит описание (необязательно)
5. Выбирает прикрепить файл/фото или пропустить
6. Если прикрепляет файл: выбирает тип (фото/документ) и загружает
7. Подтверждает всю информацию
8. Заявка отправляется, администратор получает уведомление

### Управление статусами

Администраторы изменяют статус заявки через веб-панель по адресу `http://localhost:10000/applications/<id>`:
1. Откройте страницу деталей заявки
2. Выберите новый статус из выпадающего списка
3. Добавьте комментарий (необязательно)
4. Сохраните; пользователь получит уведомление об изменении статуса в Telegram

---

## 📁 Структура проекта

```
application/
├── bot/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py      # Конфигурация и настройки
│   │   └── bot.py           # Конфигурация экземпляра бота
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py        # Модели базы данных
│   │   └── database.py      # Подключение к базе данных и управление сессиями
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py         # Обработчик команды start
│   │   ├── registration.py  # Обработчики регистрации пользователей
│   │   ├── application.py   # Обработчики создания заявок
│   │   ├── language.py      # Обработчики смены языка
│   │   └── common.py        # Общие обработчики
│   ├── states/
│   │   ├── __init__.py
│   │   ├── application.py   # Состояния FSM для заявок
│   │   └── registration.py  # Состояния FSM для регистрации
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── translations.py  # Утилиты перевода
│   │   ├── keyboards.py     # Утилиты клавиатур
│   │   ├── file_handler.py  # Утилиты работы с файлами
│   │   └── validators.py    # Утилиты валидации ввода
│   └── main.py              # Точка входа
├── webadmin/
│   ├── __init__.py
│   ├── app.py               # Веб-панель администратора Flask
│   ├── templates/           # HTML шаблоны
│   └── static/              # Статические файлы (CSS)
├── run_admin.py             # Точка входа веб-панели администратора
├── docker-compose.yml       # Конфигурация Docker Compose
├── Dockerfile               # Конфигурация Docker
├── requirements.txt         # Зависимости Python
├── .env.example             # Шаблон переменных окружения
├── .gitignore               # Правила игнорирования Git
└── README.md                # Этот файл
```

---

## 🐳 Docker

### Сборка образа

```bash
docker build -t application-bot .
```

### Запуск с Docker Compose

```bash
# Запустить все сервисы
docker-compose up -d

# Остановить все сервисы
docker-compose down

# Просмотр логов
docker-compose logs -f bot webadmin

# Перезапуск бота
docker-compose restart bot
```

### Использование SQLite (Для разработки)

Чтобы использовать SQLite вместо PostgreSQL:

1. Отредактируйте файл `.env`:
   ```env
   DB_TYPE=sqlite
   ```

2. Запустите сервисы бота и веб-панели:
   ```bash
   docker-compose up -d bot webadmin
   ```

---

## 👨‍💻 Разработка

### Запуск тестов

```bash
# Установка зависимостей для тестов
pip install pytest pytest-asyncio

# Запуск тестов
pytest tests/
```

### Стиль кода

```bash
# Форматирование кода с помощью black
black bot/

# Проверка линтером flake8
flake8 bot/
```

### Добавление новых функций

1. Создайте новые файлы обработчиков в `bot/handlers/`
2. Добавьте новые состояния в `bot/states/` при необходимости
3. Обновите маршрутизаторы в `bot/main.py`
4. Добавьте переводы в `bot/utils/translations.py`
5. Обновите модели базы данных при необходимости

---

## 📜 Лицензия

Этот проект лицензирован по лицензии MIT - см. файл [LICENSE](LICENSE) для подробностей.
