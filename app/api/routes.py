"""
API routes for SMTP bridge
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.email import EmailRequest, EmailResponse
from app.core.smtp import smtp_client
from app.core.security import verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/send", response_model=EmailResponse)
async def send_email(
    email: EmailRequest,
    api_key: str = Depends(verify_api_key)
) -> EmailResponse:
    """
    Send email via SMTP

    Args:
        email: Email request data
        api_key: API key for authentication

    Returns:
        EmailResponse with success status and message ID
    """
    logger.info(f"Received email request from {email.from_email} to {email.to}")

    # Validate email content
    if not email.text and not email.html:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must contain either text or html content"
        )

    # Send email
    success, message, message_id = await smtp_client.send_email(email)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )

    return EmailResponse(
        success=success,
        message=message,
        message_id=message_id
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "smtp-bridge"
    }
