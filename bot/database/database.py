"""
Database connection and session management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from .models import Base
from ..config.settings import settings
from typing import AsyncGenerator
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager"""
    
    def __init__(self):
        self.engine = None
        self.async_session = None
        self.is_sqlite = settings.is_sqlite
        
    async def create_engine(self):
        """Create database engine"""
        if self.is_sqlite:
            # For SQLite, we need to ensure the directory exists
            import os
            db_path = settings.SQLite_DB_PATH
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # SQLite doesn't support async properly, so we use a sync engine with async wrapper
            from sqlalchemy import create_engine as sync_create_engine
            sync_engine = sync_create_engine(
                f"sqlite:///{db_path}",
                echo=False,
                connect_args={"check_same_thread": False}
            )
            self.engine = sync_engine
        else:
            # PostgreSQL async engine
            self.engine = create_async_engine(
                settings.DATABASE_URL,
                echo=False,
                pool_pre_ping=True,
                pool_size=20,
                max_overflow=10
            )
        
        logger.info(f"Database engine created: {settings.DATABASE_URL}")
    
    async def create_tables(self):
        """Create all database tables"""
        if self.is_sqlite:
            # For SQLite, use sync engine
            Base.metadata.create_all(self.engine)
        else:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")
    
    async def drop_tables(self):
        """Drop all database tables"""
        if self.is_sqlite:
            Base.metadata.drop_all(self.engine)
        else:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped")
    
    async def close(self):
        """Close database connection"""
        if self.engine is None:
            return
        if self.is_sqlite:
            self.engine.dispose()
        else:
            await self.engine.dispose()
        self.engine = None
        logger.info("Database connection closed")
    
    async def init_db(self):
        """Initialize database and create tables"""
        await self.create_engine()
        await self.create_tables()
        await self.seed_initial_data()
    
    async def seed_initial_data(self):
        """Seed initial data (service types)"""
        from .models import ServiceType
        
        if self.is_sqlite:
            with self.engine.connect() as conn:
                # Check if service types already exist
                result = conn.execute(text("SELECT COUNT(*) FROM service_types"))
                count = result.scalar()
                
                if count == 0:
                    # Insert default service types
                    service_types = [
                        {"name_en": "Consultation", "name_ru": "Консультация", 
                         "description_en": "Professional consultation service", 
                         "description_ru": "Профессиональная консультация"},
                        {"name_en": "Development", "name_ru": "Разработка",
                         "description_en": "Software development service",
                         "description_ru": "Услуга разработки программного обеспечения"},
                        {"name_en": "Support", "name_ru": "Поддержка",
                         "description_en": "Technical support service",
                         "description_ru": "Услуга технической поддержки"},
                        {"name_en": "Training", "name_ru": "Обучение",
                         "description_en": "Training and education service",
                         "description_ru": "Услуга обучения и образования"}
                    ]
                    
                    for st in service_types:
                        conn.execute(text(
                            "INSERT INTO service_types (name_en, name_ru, description_en, description_ru) VALUES (:name_en, :name_ru, :description_en, :description_ru)"
                        ), st)
                    conn.commit()
                    logger.info("Seeded initial service types")
        else:
            async with self.engine.begin() as conn:
                result = await conn.execute(text("SELECT COUNT(*) FROM service_types"))
                count = result.scalar()
                
                if count == 0:
                    service_types = [
                        {"name_en": "Consultation", "name_ru": "Консультация", 
                         "description_en": "Professional consultation service", 
                         "description_ru": "Профессиональная консультация"},
                        {"name_en": "Development", "name_ru": "Разработка",
                         "description_en": "Software development service",
                         "description_ru": "Услуга разработки программного обеспечения"},
                        {"name_en": "Support", "name_ru": "Поддержка",
                         "description_en": "Technical support service",
                         "description_ru": "Услуга технической поддержки"},
                        {"name_en": "Training", "name_ru": "Обучение",
                         "description_en": "Training and education service",
                         "description_ru": "Услуга обучения и образования"}
                    ]
                    
                    for st in service_types:
                        await conn.execute(text(
                            "INSERT INTO service_types (name_en, name_ru, description_en, description_ru) VALUES (:name_en, :name_ru, :description_en, :description_ru)"
                        ), st)
                    await conn.commit()
                    logger.info("Seeded initial service types")


# Create database instance
database = Database()


async def get_db() -> AsyncGenerator:
    """Dependency to get database session"""
    if database.is_sqlite:
        # For SQLite, use sync session
        from sqlalchemy.orm import Session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()
    else:
        # For PostgreSQL, use async session
        async_session = async_sessionmaker(
            database.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()


__all__ = ["Database", "get_db", "database"]
