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

from app.models import User, UserProfile, UserToken, TokenType
from app.core.security import (
    get_password_hash,
    verify_password,
    verify_token,
    create_credentials_exception
)
from app.schemas.auth import UserRegister
from app.services.email_service import EmailService


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
    
    async def send_verification_email(self, user_id: str) -> bool:
        """
        Send email verification email to user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            True if email sent successfully
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False
            
            if user.is_verified:
                logger.warning(f"User {user.email} is already verified")
                return True
            
            # Generate verification token
            email_service = EmailService()
            token = email_service.generate_verification_token()
            
            # Create token record
            user_token = UserToken.create_verification_token(user.id, token)
            self.db.add(user_token)
            await self.db.commit()
            
            # Send verification email
            success = await email_service.send_verification_email(
                user.email, 
                user.full_name, 
                token
            )
            
            if success:
                logger.info(f"Verification email sent to: {user.email}")
            else:
                logger.error(f"Failed to send verification email to: {user.email}")
            
            return success
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error sending verification email for user {user_id}: {e}")
            return False
    
    async def verify_email(self, token: str) -> bool:
        """
        Verify user email with token.
        
        Args:
            token: Email verification token
            
        Returns:
            True if verification successful
        """
        try:
            # Find token
            result = await self.db.execute(
                select(UserToken)
                .where(UserToken.token == token)
                .where(UserToken.token_type == TokenType.EMAIL_VERIFICATION)
            )
            user_token = result.scalar_one_or_none()
            
            if not user_token:
                logger.warning(f"Invalid verification token: {token}")
                return False
            
            if not user_token.is_valid:
                logger.warning(f"Expired or used verification token: {token}")
                return False
            
            # Get user
            user = await self.get_user_by_id(str(user_token.user_id))
            if not user:
                return False
            
            # Verify user
            user.is_verified = True
            user_token.mark_as_used()
            
            await self.db.commit()
            
            logger.info(f"Email verified for user: {user.email}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error verifying email with token {token}: {e}")
            return False
    
    async def send_password_reset_email(self, email: str) -> bool:
        """
        Send password reset email.
        
        Args:
            email: User's email address
            
        Returns:
            True if email sent successfully (always returns True for security)
        """
        try:
            user = await self.get_user_by_email(email)
            if not user:
                # For security, always return True even if email doesn't exist
                logger.warning(f"Password reset requested for non-existent email: {email}")
                return True
            
            if not user.is_active:
                logger.warning(f"Password reset requested for inactive user: {email}")
                return True
            
            # Invalidate existing reset tokens
            existing_tokens_result = await self.db.execute(
                select(UserToken)
                .where(UserToken.user_id == user.id)
                .where(UserToken.token_type == TokenType.PASSWORD_RESET)
                .where(UserToken.used_at.is_(None))
            )
            existing_tokens = existing_tokens_result.scalars().all()
            
            for token in existing_tokens:
                token.mark_as_used()
            
            # Generate reset token
            email_service = EmailService()
            token = email_service.generate_reset_token()
            
            # Create token record
            user_token = UserToken.create_reset_token(user.id, token)
            self.db.add(user_token)
            await self.db.commit()
            
            # Send reset email
            success = await email_service.send_password_reset_email(
                user.email,
                user.full_name,
                token
            )
            
            if success:
                logger.info(f"Password reset email sent to: {user.email}")
            else:
                logger.error(f"Failed to send password reset email to: {user.email}")
            
            return True  # Always return True for security
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error sending password reset email for {email}: {e}")
            return True  # Always return True for security
    
    async def reset_password(self, token: str, new_password: str) -> bool:
        """
        Reset user password with token.
        
        Args:
            token: Password reset token
            new_password: New password
            
        Returns:
            True if reset successful
        """
        try:
            # Find token
            result = await self.db.execute(
                select(UserToken)
                .where(UserToken.token == token)
                .where(UserToken.token_type == TokenType.PASSWORD_RESET)
            )
            user_token = result.scalar_one_or_none()
            
            if not user_token:
                logger.warning(f"Invalid reset token: {token}")
                return False
            
            if not user_token.is_valid:
                logger.warning(f"Expired or used reset token: {token}")
                return False
            
            # Get user
            user = await self.get_user_by_id(str(user_token.user_id))
            if not user:
                return False
            
            # Update password
            user.hashed_password = get_password_hash(new_password)
            user_token.mark_as_used()
            
            await self.db.commit()
            
            logger.info(f"Password reset for user: {user.email}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error resetting password with token {token}: {e}")
            return False
