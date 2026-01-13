from sqlalchemy import Column, Float, Integer, String, Text, JSON, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from . import Base
import enum


class JobType(str, enum.Enum):
    FRONTEND_GENERATION = "frontend_generation"
    DESIGN_GENERATION = "design_generation"
    BACKEND_GENERATION = "backend_generation"
    IMAGE_GENERATION = "image_generation"
    CODE_REVIEW = "code_review"
    BUILD_ZIP = "build_zip"
    DEPLOY = "deploy"
    GITHUB_CREATE = "github_create"


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    job_type = Column(Enum(JobType), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)

    # Input/Output
    input_data = Column(JSON, nullable=True)  # Входные данные для AI
    output_data = Column(JSON, nullable=True)  # Результаты генерации
    error_message = Column(Text, nullable=True)

    # AI Metadata
    ai_model = Column(String(100), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    generation_time = Column(Float, nullable=True)  # В секундах

    # Relationships
    # project = relationship("Project", back_populates="jobs")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
