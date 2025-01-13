import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base, get_db
from app.main import app # Import the main app to override dependencies
from httpx import AsyncClient

# Use a test database URL
# For testing, we use SQLite in memory or a file, which is faster and easier to set up than a full PostgreSQL instance.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a test engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session", scope="function")
def session_fixture():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client", scope="function")
async def client_fixture(session: Session):
    # Override the get_db dependency for tests
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Clean up overrides after tests
    app.dependency_overrides.clear()
