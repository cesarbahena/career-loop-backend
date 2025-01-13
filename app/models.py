import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .database import Base

class ApplicationStatus(enum.Enum):
    saved = "saved"
    applied = "applied"
    interviewing = "interviewing"
    offer_received = "offer_received"
    rejected = "rejected"
    archived = "archived"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

    job_applications = relationship("JobApplication", back_populates="owner")

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    job_url = Column(Text, nullable=True)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.saved)
    notes = Column(Text, nullable=True)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="job_applications")
