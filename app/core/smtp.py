"""
SMTP client for sending emails
"""
import logging
import base64
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional

import aiosmtplib

from app.core.config import settings
from app.models.email import EmailRequest

logger = logging.getLogger(__name__)


class SMTPClient:
    """Async SMTP client wrapper"""

    def __init__(self):
        self.host = settings.smtp_host
        self.port = settings.smtp_port
        self.username = settings.smtp_username
        self.password = settings.smtp_password
        self.use_tls = settings.smtp_use_tls
        self.timeout = settings.smtp_timeout

    def _build_message(self, email: EmailRequest) -> MIMEMultipart:
        """Build MIME message from email request"""

        # Create message container
        if email.attachments:
            msg = MIMEMultipart("mixed")
            body_part = MIMEMultipart("alternative")
        elif email.html and email.text:
            msg = MIMEMultipart("alternative")
            body_part = msg
        else:
            msg = MIMEMultipart()
            body_part = msg

        # Set headers
        if email.from_name:
            msg["From"] = f"{email.from_name} <{email.from_email}>"
        else:
            msg["From"] = email.from_email

        msg["To"] = ", ".join(email.to)
        msg["Subject"] = email.subject

        if email.cc:
            msg["Cc"] = ", ".join(email.cc)

        if email.reply_to:
            msg["Reply-To"] = email.reply_to

        # Add custom headers
        if email.headers:
            for key, value in email.headers.items():
                msg[key] = value

        # Add body content
        if email.text:
            text_part = MIMEText(email.text, "plain", "utf-8")
            body_part.attach(text_part)

        if email.html:
            html_part = MIMEText(email.html, "html", "utf-8")
            body_part.attach(html_part)

        # Add body to message if we created a separate body part
        if email.attachments and body_part != msg:
            msg.attach(body_part)

        # Add attachments
        if email.attachments:
            for attachment in email.attachments:
                self._add_attachment(msg, attachment)

        return msg

    def _add_attachment(self, msg: MIMEMultipart, attachment) -> None:
        """Add attachment to MIME message"""
        try:
            # Decode base64 content
            content = base64.b64decode(attachment.content)

            # Create MIME part
            part = MIMEBase(*attachment.content_type.split("/", 1))
            part.set_payload(content)
            encoders.encode_base64(part)

            # Add header
            disposition = "inline" if getattr(attachment, "cid", None) else "attachment"
            part.add_header("Content-Disposition", f"{disposition}; filename={attachment.filename}")
            if getattr(attachment, "cid", None):
                part.add_header("Content-ID", f"<{attachment.cid}>")

            msg.attach(part)

        except Exception as e:
            logger.error(f"Failed to add attachment {attachment.filename}: {e}")
            raise


    async def _send_async(self, msg: MIMEMultipart, recipient: list[str]) -> None:
        """Send email in background and log failures."""
        try:
            async with aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                timeout=self.timeout,
                use_tls=self.use_tls
            ) as smtp:
                if self.username and self.password:
                    await smtp.login(self.username, self.password)
                await smtp.send_message(msg)
                logger.info("Email dispatched to %s", recipient)
        except Exception:
            logger.exception("Background send failed for %s", recipient)


    async def send_email(self, email: EmailRequest) -> tuple[bool, str, Optional[str]]:
        """
        Fire-and-forget sending: schedule SMTP send and return immediately.

        Success means the send task was scheduled without raising.
        """
        try:
            msg = self._build_message(email)
            asyncio.create_task(self._send_async(msg, email.to))
            return True, "Email dispatch started", msg.get("Message-ID")
        except Exception as e:
            error_msg = f"Failed to start email dispatch: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg, None


# Global SMTP client instance
smtp_client = SMTPClient()
