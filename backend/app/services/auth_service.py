"""
EduNLP-X Authentication Service
Business logic for user authentication, registration, and token management.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from loguru import logger

from app.models import User, UserProfile
from app.core.security import (
    get_password_hash,
    verify_password,
    verify_token,
    create_credentials_exception
)
from app.schemas.auth import UserRegister


class AuthService:
    """Authentication service for user management."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User's email address
            
        Returns:
            User object or None if not found
        """
        try:
            result = await self.db.execute(
                select(User).where(User.email == email.lower())
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User's UUID
            
        Returns:
            User object or None if not found
        """
        try:
            result = await self.db.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            return None
    
    async def create_user(self, user_data: UserRegister) -> User:
        """
        Create a new user account.
        
        Args:
            user_data: User registration data
            
        Returns:
            Created User object
            
        Raises:
            HTTPException: If user creation fails
        """
        try:
            # Hash the password
            hashed_password = get_password_hash(user_data.password)
            
            # Create user object
            db_user = User(
                email=user_data.email.lower(),
                hashed_password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                role=user_data.role,
                phone_number=user_data.phone_number,
                is_verified=False,
                is_active=True
            )
            
            # Add to database
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            
            # Create user profile
            user_profile = UserProfile(
                user_id=db_user.id,
                progress_data={},
                performance_metrics={},
                study_goals={},
                notification_preferences={
                    "email_notifications": True,
                    "push_notifications": True,
                    "quiz_reminders": True
                },
                ui_preferences={
                    "theme": "light",
                    "language": "en"
                }
            )
            
            self.db.add(user_profile)
            await self.db.commit()
            
            logger.info(f"Created new user: {db_user.email}")
            return db_user
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user account"
            )
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = await self.get_user_by_email(email)
        
        if not user:
            logger.warning(f"Login attempt with non-existent email: {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"Login attempt with inactive account: {email}")
            return None
        
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Failed login attempt for user: {email}")
            return None
        
        logger.info(f"Successful login for user: {email}")
        return user
    
    async def update_last_login(self, user_id: str) -> None:
        """
        Update user's last login timestamp.
        
        Args:
            user_id: User's UUID
        """
        try:
            user = await self.get_user_by_id(user_id)
            if user:
                user.last_login = datetime.utcnow()
                await self.db.commit()
        except Exception as e:
            logger.error(f"Error updating last login for user {user_id}: {e}")
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Get current user from JWT token.
        
        Args:
            token: JWT access token
            
        Returns:
            User object or None if token invalid
        """
        # Verify token
        payload = verify_token(token, "access_token")
        if not payload:
            return None
        
        # Get user from token payload
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        # Fetch user from database
        user = await self.get_user_by_id(user_id)
        if not user or not user.is_active:
            return None
        
        return user
    
    async def verify_refresh_token(self, refresh_token: str) -> Optional[User]:
        """
        Verify refresh token and return user.
        
        Args:
            refresh_token: JWT refresh token
            
        Returns:
            User object or None if token invalid
        """
        # Verify token
        payload = verify_token(refresh_token, "refresh_token")
        if not payload:
            return None
        
        # Get user from token payload
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        # Fetch user from database
        user = await self.get_user_by_id(user_id)
        if not user or not user.is_active:
            return None
        
        return user
    
    async def deactivate_user(self, user_id: str) -> bool:
        """
        Deactivate user account.
        
        Args:
            user_id: User's UUID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_user_by_id(user_id)
            if user:
                user.is_active = False
                await self.db.commit()
                logger.info(f"Deactivated user account: {user.email}")
                return True
            return False
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deactivating user {user_id}: {e}")
            return False
    
    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User's UUID
            current_password: Current plain text password
            new_password: New plain text password
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False
            
            # Verify current password
            if not verify_password(current_password, user.hashed_password):
                logger.warning(f"Invalid current password for user: {user.email}")
                return False
            
            # Update password
            user.hashed_password = get_password_hash(new_password)
            await self.db.commit()
            
            logger.info(f"Password changed for user: {user.email}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error changing password for user {user_id}: {e}")
            return False
