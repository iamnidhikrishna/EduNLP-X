"""
EduNLP-X Core Package
Core configuration, database, and security components.
"""

from app.core.config import settings
from app.core.database import get_async_db, get_sync_db, DatabaseManager
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_hash,
    verify_password,
    oauth2_scheme,
    create_credentials_exception,
    create_permission_exception
)

__all__ = [
    "settings",
    "get_async_db",
    "get_sync_db", 
    "DatabaseManager",
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "get_password_hash",
    "verify_password",
    "oauth2_scheme",
    "create_credentials_exception",
    "create_permission_exception"
]
