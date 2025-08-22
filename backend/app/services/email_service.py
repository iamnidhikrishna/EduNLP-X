"""
EduNLP-X Email Service
Email functionality for user verification, password resets, and notifications.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime, timedelta
import secrets
from loguru import logger
from jinja2 import Template

from app.core.config import settings


class EmailService:
    """Service for sending emails and managing email templates."""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME
        self.use_tls = settings.SMTP_TLS
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send email to recipient.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text content (optional)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            if not all([self.smtp_server, self.smtp_user, self.smtp_password]):
                logger.warning("Email service not configured, skipping email send")
                return True  # Return True in development to not block flows
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            
            # Add text content
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    async def send_verification_email(self, user_email: str, user_name: str, verification_token: str) -> bool:
        """
        Send email verification email.
        
        Args:
            user_email: User's email address
            user_name: User's full name
            verification_token: Email verification token
            
        Returns:
            True if sent successfully
        """
        verification_url = f"http://localhost:3000/verify-email?token={verification_token}"
        
        subject = "Verify Your EduNLP-X Account"
        
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email - EduNLP-X</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #2E86AB; color: white; padding: 20px; text-align: center; }
                .content { padding: 30px; background-color: #f9f9f9; }
                .button { display: inline-block; padding: 12px 24px; background-color: #2E86AB; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 EduNLP-X</h1>
                    <p>Welcome to AI-Powered Education</p>
                </div>
                <div class="content">
                    <h2>Hi {{ user_name }},</h2>
                    <p>Welcome to EduNLP-X! We're excited to have you join our AI-powered educational platform.</p>
                    <p>To get started, please verify your email address by clicking the button below:</p>
                    <div style="text-align: center;">
                        <a href="{{ verification_url }}" class="button">Verify Email Address</a>
                    </div>
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p><a href="{{ verification_url }}">{{ verification_url }}</a></p>
                    <p>This verification link will expire in 24 hours for security reasons.</p>
                    <p>If you didn't create an account with EduNLP-X, please ignore this email.</p>
                    <p>Best regards,<br>The EduNLP-X Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 EduNLP-X. All rights reserved.</p>
                    <p>This is an automated message, please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        html_content = html_template.render(
            user_name=user_name,
            verification_url=verification_url
        )
        
        text_content = f"""
        Hi {user_name},
        
        Welcome to EduNLP-X! Please verify your email address by visiting this link:
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        
        Best regards,
        The EduNLP-X Team
        """
        
        return await self.send_email(user_email, subject, html_content, text_content)
    
    async def send_password_reset_email(self, user_email: str, user_name: str, reset_token: str) -> bool:
        """
        Send password reset email.
        
        Args:
            user_email: User's email address
            user_name: User's full name
            reset_token: Password reset token
            
        Returns:
            True if sent successfully
        """
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"
        
        subject = "Reset Your EduNLP-X Password"
        
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Your Password - EduNLP-X</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #2E86AB; color: white; padding: 20px; text-align: center; }
                .content { padding: 30px; background-color: #f9f9f9; }
                .button { display: inline-block; padding: 12px 24px; background-color: #2E86AB; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .warning { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 EduNLP-X</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <h2>Hi {{ user_name }},</h2>
                    <p>We received a request to reset your password for your EduNLP-X account.</p>
                    <p>If you requested this password reset, click the button below to create a new password:</p>
                    <div style="text-align: center;">
                        <a href="{{ reset_url }}" class="button">Reset Password</a>
                    </div>
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p><a href="{{ reset_url }}">{{ reset_url }}</a></p>
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul>
                            <li>This reset link will expire in 1 hour for security</li>
                            <li>If you didn't request this reset, please ignore this email</li>
                            <li>Your account is secure and no changes have been made</li>
                        </ul>
                    </div>
                    <p>For security reasons, please don't share this link with anyone.</p>
                    <p>Best regards,<br>The EduNLP-X Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 EduNLP-X. All rights reserved.</p>
                    <p>This is an automated message, please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        html_content = html_template.render(
            user_name=user_name,
            reset_url=reset_url
        )
        
        text_content = f"""
        Hi {user_name},
        
        We received a request to reset your password for your EduNLP-X account.
        
        If you requested this, please visit: {reset_url}
        
        This link will expire in 1 hour for security.
        
        If you didn't request this reset, please ignore this email.
        
        Best regards,
        The EduNLP-X Team
        """
        
        return await self.send_email(user_email, subject, html_content, text_content)
    
    @staticmethod
    def generate_verification_token() -> str:
        """Generate secure verification token."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_reset_token() -> str:
        """Generate secure password reset token."""
        return secrets.token_urlsafe(32)
