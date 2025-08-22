"""
EduNLP-X User Schemas
Pydantic schemas for user management and profiles.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime

from app.models.user import UserRole, LearningLevel, LearningStyle


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str
    role: UserRole = UserRole.STUDENT
    
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


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        """Validate name fields."""
        if v and len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip().title() if v else v


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    learning_level: Optional[LearningLevel] = None
    learning_style: Optional[LearningStyle] = None
    preferred_subjects: Optional[List[str]] = None
    grade_level: Optional[str] = None
    institution: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    timezone: Optional[str] = None
    notification_preferences: Optional[Dict[str, Any]] = None
    ui_preferences: Optional[Dict[str, Any]] = None


class UserProfileResponse(BaseModel):
    """Schema for user profile response."""
    learning_level: Optional[LearningLevel]
    learning_style: Optional[LearningStyle]
    preferred_subjects: Optional[List[str]]
    grade_level: Optional[str]
    institution: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    timezone: Optional[str]
    progress_data: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    phone_number: Optional[str]
    avatar_url: Optional[str]
    is_verified: bool
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    class Config:
        from_attributes = True


class UserDashboard(BaseModel):
    """Schema for user dashboard data."""
    user: UserResponse
    profile: UserProfileResponse
    stats: Dict[str, Any]
    recent_activity: List[Dict[str, Any]]
    progress_summary: Dict[str, Any]
    recommendations: List[str]


class UserList(BaseModel):
    """Schema for paginated user list."""
    users: List[UserResponse]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool
