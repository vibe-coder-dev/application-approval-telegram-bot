"""
Database models for the application bot
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class ApplicationStatusEnum(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class User(Base):
    """User model for storing client information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    language = Column(String(10), default="en")
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class ServiceType(Base):
    """Service type model"""
    __tablename__ = "service_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(100), nullable=False)
    name_ru = Column(String(100), nullable=False)
    description_en = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    applications = relationship("Application", back_populates="service_type")
    
    def get_name(self, language: str = "en") -> str:
        return getattr(self, f"name_{language}", self.name_en)
    
    def get_description(self, language: str = "en") -> Optional[str]:
        return getattr(self, f"description_{language}", self.description_en)


class Application(Base):
    """Application model for storing client applications"""
    __tablename__ = "applications"
    __table_args__ = (
        Index("ix_applications_status", "status"),
        Index("ix_applications_user_id", "user_id"),
        Index("ix_applications_created_at", "created_at"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_type_id = Column(Integer, ForeignKey("service_types.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ApplicationStatusEnum), default=ApplicationStatusEnum.NEW)
    
    # File attachments
    file_path = Column(String(500), nullable=True)
    file_type = Column(String(50), nullable=True)  # 'photo', 'document', etc.
    file_name = Column(String(255), nullable=True)
    
    # Additional fields
    priority = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    service_type = relationship("ServiceType", back_populates="applications")
    status_history = relationship("ApplicationStatus", back_populates="application", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Application(id={self.id}, title={self.title}, status={self.status})>"


class ApplicationStatus(Base):
    """Application status history model"""
    __tablename__ = "application_status_history"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ApplicationStatusEnum), nullable=False)
    changed_by = Column(Integer, nullable=True)  # telegram_id of user who changed status
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    application = relationship("Application", back_populates="status_history")
    
    def __repr__(self):
        return f"<ApplicationStatus(application_id={self.application_id}, status={self.status})>"
