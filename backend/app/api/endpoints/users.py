"""
EduNLP-X User Management Endpoints
User profile management, settings, and administration.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models import User
from app.api.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current user's profile."""
    return {"message": "User profile endpoint - to be implemented"}


@router.put("/profile")
async def update_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Update current user's profile."""
    return {"message": "Update user profile endpoint - to be implemented"}


@router.get("/dashboard")
async def get_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get user dashboard data."""
    return {"message": "User dashboard endpoint - to be implemented"}
