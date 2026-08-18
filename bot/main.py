#!/usr/bin/env python3
"""
Main entry point for the Application Bot
"""
import asyncio
import logging
from typing import Optional
from aiogram import Bot, Dispatcher
from .config import settings, storage
from .database import database
from .handlers import (
    start_router, registration_router, application_router,
    admin_router, language_router, common_router
)
from .utils.translations import load_translations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create bot and dispatcher instances
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=storage)


async def setup_database():
    """Initialize database connection and tables"""
    try:
        await database.init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def setup_routers():
    """Setup all routers"""
    # Include all routers
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(application_router)
    dp.include_router(admin_router)
    dp.include_router(language_router)
    dp.include_router(common_router)
    
    logger.info("All routers included")


async def on_startup():
    """Startup handler"""
    logger.info("Starting Application Bot...")
    
    # Load translations
    load_translations()
    logger.info("Translations loaded")
    
    # Setup database
    await setup_database()
    
    # Setup routers
    await setup_routers()
    
    logger.info("Bot started successfully")


async def on_shutdown():
    """Shutdown handler"""
    logger.info("Shutting down Application Bot...")
    
    # Close database connection
    await database.close()
    
    logger.info("Bot shutdown complete")


async def main():
    """Main function to run the bot"""
    try:
        # Set startup and shutdown handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Start the bot
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        raise
    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
