"""
EduNLP-X Chat Endpoints
AI-powered chat and conversation management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models import User
from app.api.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/sessions")
async def create_chat_session(
    subject: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create new chat session."""
    return {"message": "Create chat session endpoint - to be implemented"}


@router.get("/sessions")
async def list_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """List user's chat sessions."""
    return {"message": "List chat sessions endpoint - to be implemented"}


@router.post("/sessions/{session_id}/messages")
async def send_message(
    session_id: str,
    message: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Send message in chat session."""
    return {"message": "Send message endpoint - to be implemented"}
