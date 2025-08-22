"""
EduNLP-X Authentication Tests
Unit tests for authentication functionality.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class TestAuthEndpoints:
    """Test authentication endpoints."""

    async def test_register_user(self, client: AsyncClient, sample_user_data):
        """Test user registration."""
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["first_name"] == sample_user_data["first_name"]
        assert data["role"] == sample_user_data["role"]
        assert "id" in data
        assert "password" not in data

    async def test_login_user(self, client: AsyncClient, test_user: User):
        """Test user login."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "testpassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user.email

    async def test_login_invalid_credentials(self, client: AsyncClient, test_user: User):
        """Test login with invalid credentials."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    async def test_get_current_user(self, client: AsyncClient, auth_headers: dict, test_user: User):
        """Test getting current user info."""
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["id"] == str(test_user.id)

    async def test_get_current_user_no_token(self, client: AsyncClient):
        """Test getting current user without token."""
        response = await client.get("/api/v1/auth/me")
        
        assert response.status_code == 401

    async def test_register_duplicate_email(self, client: AsyncClient, test_user: User, sample_user_data):
        """Test registering with duplicate email."""
        sample_user_data["email"] = test_user.email
        
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    async def test_register_invalid_password(self, client: AsyncClient, sample_user_data):
        """Test registering with invalid password."""
        sample_user_data["password"] = "weak"
        
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == 422  # Validation error


class TestPasswordValidation:
    """Test password validation."""

    @pytest.mark.parametrize("password,should_pass", [
        ("ValidPass123", True),
        ("weakpass", False),  # No uppercase, no number
        ("WEAKPASS", False),  # No lowercase, no number
        ("WeakPass", False),  # No number
        ("weak123", False),   # No uppercase
        ("WEAK123", False),   # No lowercase
        ("Wk1", False),       # Too short
    ])
    async def test_password_validation(self, client: AsyncClient, sample_user_data, password, should_pass):
        """Test various password validation scenarios."""
        sample_user_data["password"] = password
        
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        
        if should_pass:
            assert response.status_code == 201
        else:
            assert response.status_code == 422
