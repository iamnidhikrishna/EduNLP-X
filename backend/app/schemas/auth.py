"""
EduNLP-X Authentication Schemas
Pydantic schemas for authentication-related API requests and responses.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from app.models.user import UserRole


class UserRegister(BaseModel):
    """User registration schema."""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.STUDENT
    phone_number: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        """Validate name fields."""
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip().title()


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str
    user: 'UserResponse'


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    phone_number: Optional[str]
    avatar_url: Optional[str]
    is_verified: bool
    is_active: bool
    created_at: str
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Password reset schema."""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class PasswordChange(BaseModel):
    """Password change schema."""
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
