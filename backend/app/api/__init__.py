"""
EduNLP-X API Package
Main API router and endpoint definitions.
"""

from fastapi import APIRouter

from app.api.endpoints import auth, users, content, chat, quiz

# Create main API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(content.router, prefix="/content", tags=["Content"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])

__all__ = ["api_router"]
