"""
EduNLP-X Main Application Tests
Tests for main application endpoints and health checks.
"""

import pytest
from httpx import AsyncClient


class TestMainEndpoints:
    """Test main application endpoints."""

    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to EduNLP-X API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"

    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint."""
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data

    async def test_api_documentation_accessible(self, client: AsyncClient):
        """Test that API documentation is accessible."""
        response = await client.get("/docs")
        assert response.status_code == 200

    async def test_nonexistent_endpoint(self, client: AsyncClient):
        """Test accessing nonexistent endpoint."""
        response = await client.get("/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert data["message"] == "Resource not found"
