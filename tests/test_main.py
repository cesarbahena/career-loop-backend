import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session # Import Session for type hinting

from app import models, schemas # Keep models and schemas for test data creation

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Career Loop API"}

@pytest.mark.asyncio
async def test_read_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_create_job_application(client: AsyncClient, session: Session):
    # Ensure there's a dummy user for the current_user_placeholder
    dummy_user = models.User(email="test@example.com", hashed_password="dummyhashedpassword", full_name="Test User")
    session.add(dummy_user)
    session.commit()
    session.refresh(dummy_user)

    new_application = {
        "job_title": "Software Engineer",
        "company_name": "Tech Corp",
        "job_url": "http://techcorp.com/se-job",
        "status": "applied",
        "notes": "Applied via LinkedIn"
    }
    response = await client.post("/job-applications/", json=new_application)
    assert response.status_code == 201
    data = response.json()
    assert data["job_title"] == "Software Engineer"
    assert "id" in data
    assert data["user_id"] == str(dummy_user.id) # user_id comes as str from json

@pytest.mark.asyncio
async def test_read_job_applications(client: AsyncClient, session: Session):
    # Ensure there's a dummy user
    dummy_user = session.query(models.User).first()
    if not dummy_user:
        dummy_user = models.User(email="test@example.com", hashed_password="dummyhashedpassword", full_name="Test User")
        session.add(dummy_user)
        session.commit()
        session.refresh(dummy_user)

    # Create a job application for the dummy user
    new_application_data = schemas.JobApplicationCreate(
        job_title="DevOps Engineer",
        company_name="Cloud Solutions",
        job_url="http://cloudsolutions.com/devops",
        status=schemas.ApplicationStatus.saved,
        notes="Interviewed last week"
    )
    db_application = models.JobApplication(**new_application_data.model_dump(), user_id=dummy_user.id)
    session.add(db_application)
    session.commit()
    session.refresh(db_application)

    response = await client.get("/job-applications/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["job_title"] == "DevOps Engineer"
    assert data[0]["user_id"] == str(dummy_user.id)

# TODO: Add tests for read_job_application_by_id, update_job_application, delete_job_application
