"""
Email models for request/response handling
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class EmailAttachment(BaseModel):
    """Email attachment model"""
    filename: str = Field(..., description="Attachment filename")
    content: str = Field(..., description="Base64 encoded attachment content")
    content_type: str = Field(default="application/octet-stream", description="MIME type")


class EmailRequest(BaseModel):
    """Email send request model"""
    from_email: EmailStr = Field(..., alias="from", description="Sender email address")
    from_name: Optional[str] = Field(None, description="Sender name")
    to: list[EmailStr] = Field(..., min_length=1, description="Recipient email addresses")
    cc: Optional[list[EmailStr]] = Field(None, description="CC recipients")
    bcc: Optional[list[EmailStr]] = Field(None, description="BCC recipients")
    subject: str = Field(..., min_length=1, description="Email subject")
    text: Optional[str] = Field(None, description="Plain text content")
    html: Optional[str] = Field(None, description="HTML content")
    attachments: Optional[list[EmailAttachment]] = Field(None, description="Email attachments")
    reply_to: Optional[EmailStr] = Field(None, description="Reply-to address")
    headers: Optional[dict[str, str]] = Field(None, description="Custom headers")

    model_config = {
        "json_schema_extra": {
            "example": {
                "from": "sender@example.com",
                "from_name": "John Doe",
                "to": ["recipient@example.com"],
                "subject": "Test Email",
                "text": "This is a test email",
                "html": "<p>This is a test email</p>"
            }
        }
    }


class EmailResponse(BaseModel):
    """Email send response model"""
    success: bool
    message: str
    message_id: Optional[str] = None
