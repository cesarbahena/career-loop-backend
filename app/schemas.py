from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr

from .models import ApplicationStatus

# Pydantic model for User
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Pydantic models for JobApplication
class JobApplicationBase(BaseModel):
    job_title: str
    company_name: str
    job_url: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.saved
    notes: Optional[str] = None
    applied_at: Optional[datetime] = None

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationUpdate(JobApplicationBase):
    pass

class JobApplication(JobApplicationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
