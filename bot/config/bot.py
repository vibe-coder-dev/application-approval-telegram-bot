"""
Telegram bot configuration
"""
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from .settings import settings
import os

# Use MemoryStorage for development, can be changed to RedisStorage for production
storage = MemoryStorage()

# Bot and dispatcher instances - will be created in main.py
bot = None
dp = None

__all__ = ["storage"]
