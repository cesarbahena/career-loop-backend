from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid

from . import models, schemas
from .database import engine, get_db

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Career Loop API")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency to get the current user (placeholder for now)
# In a real app, this would involve token verification and fetching user from DB
def get_current_user_placeholder(db: Session = Depends(get_db)):
    # For now, just return a dummy user.
    # TODO: Implement proper user authentication
    first_user = db.query(models.User).first()
    if not first_user:
        # Create a dummy user if none exists
        dummy_user = models.User(email="test@example.com", hashed_password="dummyhashedpassword", full_name="Test User")
        db.add(dummy_user)
        db.commit()
        db.refresh(dummy_user)
        return dummy_user
    return first_user


@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Career Loop API"}


@app.get("/health")
def read_health():
    """A health check endpoint."""
    return {"status": "ok"}


# --- Job Application Endpoints ---

@app.post("/job-applications/", response_model=schemas.JobApplication, status_code=status.HTTP_201_CREATED)
def create_job_application(
    application: schemas.JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_placeholder)
):
    db_application = models.JobApplication(**application.model_dump(), user_id=current_user.id)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@app.get("/job-applications/", response_model=List[schemas.JobApplication])
def read_job_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_placeholder)
):
    applications = db.query(models.JobApplication).filter(models.JobApplication.user_id == current_user.id).offset(skip).limit(limit).all()
    return applications

@app.get("/job-applications/{application_id}", response_model=schemas.JobApplication)
def read_job_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_placeholder)
):
    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id,
        models.JobApplication.user_id == current_user.id
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    return application

@app.put("/job-applications/{application_id}", response_model=schemas.JobApplication)
def update_job_application(
    application_id: uuid.UUID,
    application: schemas.JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_placeholder)
):
    db_application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id,
        models.JobApplication.user_id == current_user.id
    ).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")

    for key, value in application.model_dump(exclude_unset=True).items():
        setattr(db_application, key, value)

    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@app.delete("/job-applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_placeholder)
):
    db_application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id,
        models.JobApplication.user_id == current_user.id
    ).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")

    db.delete(db_application)
    db.commit()
    return {"message": "Job application deleted successfully"}
