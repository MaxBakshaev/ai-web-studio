from sqlalchemy import Column, String, Text, JSON, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from . import Base
import enum


class ProjectStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING = "generating"
    REVIEWING = "reviewing"
    READY = "ready"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # AI Generation Fields
    prompt = Column(Text, nullable=False)  # Оригинальный промпт пользователя
    generated_structure = Column(JSON, nullable=True)  # JSON структуры сайта
    generated_html = Column(Text, nullable=True)
    generated_css = Column(Text, nullable=True)
    generated_js = Column(Text, nullable=True)
    generated_backend = Column(Text, nullable=True)  # Python код бэкенда
    color_scheme = Column(String(100), nullable=True)
    ai_model_used = Column(String(100), nullable=True)  # deepseek, gpt-4 и т.д.

    # Deployment & Storage
    zip_file_url = Column(String(500), nullable=True)  # URL до ZIP архива
    preview_url = Column(String(500), nullable=True)  # URL превью
    deployed_url = Column(String(500), nullable=True)  # Продакшен URL
    github_repo_url = Column(String(500), nullable=True)

    # Metadata
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING)
    is_public = Column(Boolean, default=False)
    tokens_used = Column(JSON, nullable=True)  # {frontend: 1000, design: 500}

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Связь с заданиями (jobs)
    # jobs = relationship("Job", back_populates="project")
