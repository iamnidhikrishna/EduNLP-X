"""
EduNLP-X User Management Endpoints
User profile management, settings, and administration.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models import User, UserRole
from app.api.endpoints.auth import get_current_user
from app.services.user_service import UserService
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserProfileUpdate,
    UserProfileResponse,
    UserDashboard,
    UserList
)
from app.schemas.auth import PasswordChange

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's basic information."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Update current user's basic information."""
    user_service = UserService(db)
    updated_user = await user_service.update_user(str(current_user.id), user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current user's detailed profile."""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(str(current_user.id))
    
    if not user or not user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return user.profile


@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Update current user's profile."""
    user_service = UserService(db)
    updated_profile = await user_service.update_user_profile(
        str(current_user.id), 
        profile_data
    )
    
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
    
    return updated_profile


@router.get("/dashboard", response_model=UserDashboard)
async def get_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get user dashboard with stats and progress."""
    user_service = UserService(db)
    dashboard = await user_service.get_user_dashboard(str(current_user.id))
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard data not found"
        )
    
    return dashboard


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Change current user's password."""
    user_service = UserService(db)
    success = await user_service.change_password(
        str(current_user.id),
        password_data.current_password,
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password or password change failed"
        )
    
    return {"message": "Password changed successfully"}


@router.delete("/deactivate")
async def deactivate_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Deactivate current user's account."""
    user_service = UserService(db)
    success = await user_service.deactivate_user(str(current_user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate account"
        )
    
    return {"message": "Account deactivated successfully"}


# Admin endpoints
@router.get("/list", response_model=UserList)
async def list_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    """List users (Admin only)."""
    # Check if user has admin privileges
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.PRINCIPAL]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    user_service = UserService(db)
    result = await user_service.get_users_paginated(
        page=page,
        limit=limit,
        search=search,
        role=role,
        is_active=is_active
    )
    
    return UserList(**result)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get user by ID (Admin only)."""
    # Check if user has admin privileges or accessing own profile
    if (current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.PRINCIPAL] 
        and str(current_user.id) != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
