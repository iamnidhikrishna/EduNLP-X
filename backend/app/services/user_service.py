"""
EduNLP-X User Service
Business logic for user management, profiles, and dashboard operations.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from loguru import logger

from app.models import User, UserProfile, StudentProgress
from app.schemas.user import UserUpdate, UserProfileUpdate, UserDashboard
from app.core.security import get_password_hash, verify_password


class UserService:
    """Service for user management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID with profile loaded.
        
        Args:
            user_id: User's UUID
            
        Returns:
            User object with profile or None if not found
        """
        try:
            result = await self.db.execute(
                select(User)
                .options(selectinload(User.profile))
                .where(User.id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            return None
    
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
                select(User)
                .options(selectinload(User.profile))
                .where(User.email == email.lower())
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            return None
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """
        Update user information.
        
        Args:
            user_id: User's UUID
            user_data: Updated user data
            
        Returns:
            Updated User object or None if not found
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            
            update_data = user_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info(f"Updated user: {user.email}")
            return user
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            return None
    
    async def update_user_profile(self, user_id: str, profile_data: UserProfileUpdate) -> Optional[UserProfile]:
        """
        Update user profile information.
        
        Args:
            user_id: User's UUID
            profile_data: Updated profile data
            
        Returns:
            Updated UserProfile object or None if not found
        """
        try:
            result = await self.db.execute(
                select(UserProfile).where(UserProfile.user_id == user_id)
            )
            profile = result.scalar_one_or_none()
            
            if not profile:
                # Create new profile if doesn't exist
                profile = UserProfile(user_id=user_id)
                self.db.add(profile)
            
            update_data = profile_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(profile, field, value)
            
            await self.db.commit()
            await self.db.refresh(profile)
            
            logger.info(f"Updated profile for user: {user_id}")
            return profile
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating user profile {user_id}: {e}")
            return None
    
    async def get_user_dashboard(self, user_id: str) -> Optional[UserDashboard]:
        """
        Get comprehensive dashboard data for user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            UserDashboard object with stats and progress
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            
            # Get user stats
            stats = await self._get_user_stats(user_id)
            
            # Get recent activity (placeholder for now)
            recent_activity = []
            
            # Get progress summary
            progress_summary = await self._get_progress_summary(user_id)
            
            # Get recommendations (placeholder for now)
            recommendations = await self._get_recommendations(user_id)
            
            return UserDashboard(
                user=user,
                profile=user.profile,
                stats=stats,
                recent_activity=recent_activity,
                progress_summary=progress_summary,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error getting dashboard for user {user_id}: {e}")
            return None
    
    async def _get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics."""
        try:
            # Quiz attempts count
            quiz_attempts_result = await self.db.execute(
                select(func.count()).where(User.id == user_id)
            )
            quiz_attempts = quiz_attempts_result.scalar() or 0
            
            # Study progress
            progress_result = await self.db.execute(
                select(StudentProgress).where(StudentProgress.student_id == user_id)
            )
            progress_records = progress_result.scalars().all()
            
            total_time = sum(record.time_spent_minutes for record in progress_records)
            subjects_count = len(set(record.subject for record in progress_records))
            avg_completion = sum(record.completion_percentage for record in progress_records) / len(progress_records) if progress_records else 0
            
            return {
                "total_quiz_attempts": quiz_attempts,
                "total_study_time_hours": round(total_time / 60, 1),
                "subjects_studied": subjects_count,
                "average_completion": round(avg_completion, 1),
                "last_activity": datetime.utcnow().isoformat()  # Placeholder
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats for {user_id}: {e}")
            return {}
    
    async def _get_progress_summary(self, user_id: str) -> Dict[str, Any]:
        """Get progress summary by subject."""
        try:
            result = await self.db.execute(
                select(StudentProgress).where(StudentProgress.student_id == user_id)
            )
            progress_records = result.scalars().all()
            
            summary = {}
            for record in progress_records:
                summary[record.subject] = {
                    "completion_percentage": record.completion_percentage,
                    "time_spent_hours": round(record.time_spent_minutes / 60, 1),
                    "competency_level": record.competency_level,
                    "mastery_achieved": record.mastery_achieved
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting progress summary for {user_id}: {e}")
            return {}
    
    async def _get_recommendations(self, user_id: str) -> List[str]:
        """Get personalized recommendations for the user."""
        try:
            # Placeholder implementation - in a real system, this would use AI/ML
            # to analyze user progress and provide intelligent recommendations
            recommendations = [
                "Complete the Python Basics quiz to test your knowledge",
                "Review the Database Design concepts you studied last week",
                "Try the intermediate level problems in your weak areas"
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations for {user_id}: {e}")
            return []
    
    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User's UUID
            current_password: Current password
            new_password: New password
            
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
            if not user:
                return False
            
            user.is_active = False
            await self.db.commit()
            
            logger.info(f"Deactivated user: {user.email}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deactivating user {user_id}: {e}")
            return False
    
    async def get_users_paginated(
        self, 
        page: int = 1, 
        limit: int = 10,
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get paginated list of users with filtering.
        
        Args:
            page: Page number (1-based)
            limit: Items per page
            search: Search term for name/email
            role: Filter by role
            is_active: Filter by active status
            
        Returns:
            Paginated user list with metadata
        """
        try:
            offset = (page - 1) * limit
            
            # Build base query
            query = select(User).options(selectinload(User.profile))
            filters = []
            
            if search:
                search_term = f"%{search.lower()}%"
                filters.append(
                    or_(
                        func.lower(User.first_name).like(search_term),
                        func.lower(User.last_name).like(search_term),
                        func.lower(User.email).like(search_term)
                    )
                )
            
            if role:
                filters.append(User.role == role)
            
            if is_active is not None:
                filters.append(User.is_active == is_active)
            
            if filters:
                query = query.where(and_(*filters))
            
            # Get total count
            count_query = select(func.count()).select_from(User)
            if filters:
                count_query = count_query.where(and_(*filters))
            
            total_result = await self.db.execute(count_query)
            total = total_result.scalar()
            
            # Get paginated results
            users_result = await self.db.execute(
                query.offset(offset).limit(limit).order_by(User.created_at.desc())
            )
            users = users_result.scalars().all()
            
            pages = (total + limit - 1) // limit
            
            return {
                "users": users,
                "total": total,
                "page": page,
                "limit": limit,
                "pages": pages,
                "has_next": page < pages,
                "has_prev": page > 1
            }
            
        except Exception as e:
            logger.error(f"Error getting paginated users: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch users"
            )
