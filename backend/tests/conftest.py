"""
EduNLP-X Test Configuration
Pytest configuration and fixtures for testing.
"""

import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_async_db
from app.models.base import Base
from app.models import User, UserProfile
from app.core.security import get_password_hash

# Test database URL (SQLite in memory for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Clean up
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with test database."""
    
    async def override_get_async_db():
        yield test_db
    
    app.dependency_overrides[get_async_db] = override_get_async_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(test_db: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        first_name="Test",
        last_name="User",
        role="student",
        is_active=True,
        is_verified=True
    )
    
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    # Create profile
    profile = UserProfile(
        user_id=user.id,
        learning_level="intermediate",
        preferred_subjects=["python", "mathematics"]
    )
    
    test_db.add(profile)
    await test_db.commit()
    
    return user


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, test_user: User) -> dict:
    """Get authentication headers for test user."""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    token_data = response.json()
    
    return {"Authorization": f"Bearer {token_data['access_token']}"}


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "newuser@example.com",
        "password": "NewPassword123",
        "first_name": "New",
        "last_name": "User",
        "role": "student"
    }


@pytest.fixture
def sample_profile_data():
    """Sample profile data for testing."""
    return {
        "learning_level": "advanced",
        "learning_style": "visual", 
        "preferred_subjects": ["python", "database"],
        "bio": "Passionate about learning"
    }
