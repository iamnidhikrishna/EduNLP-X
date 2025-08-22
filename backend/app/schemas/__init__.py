"""
EduNLP-X Schemas Package
Pydantic schemas for API request/response validation.
"""

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    Token,
    RefreshTokenRequest,
    UserResponse as AuthUserResponse,
    PasswordResetRequest,
    PasswordReset,
    PasswordChange
)

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserProfileUpdate,
    UserProfileResponse,
    UserResponse,
    UserDashboard,
    UserList
)

__all__ = [
    # Auth schemas
    "UserRegister",
    "UserLogin",
    "Token",
    "RefreshTokenRequest", 
    "AuthUserResponse",
    "PasswordResetRequest",
    "PasswordReset",
    "PasswordChange",
    
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate", 
    "UserProfileUpdate",
    "UserProfileResponse",
    "UserResponse",
    "UserDashboard",
    "UserList"
]
