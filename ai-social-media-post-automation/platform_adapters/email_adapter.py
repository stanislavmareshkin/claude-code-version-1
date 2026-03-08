"""
Email adapter for sending proposals and newsletters via SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from PIL import Image

from .base import PlatformAdapter
from ..config import EMAIL_CONFIG


class EmailAdapter(PlatformAdapter):
    """
    Email adapter using SMTP.
    Used for cold outreach proposals and follow-ups.
    """

    def __init__(self, credentials: Optional[Dict[str, Any]] = None):
        creds = credentials or {
            "smtp_host": EMAIL_CONFIG["smtp_host"],
            "smtp_port": EMAIL_CONFIG["smtp_port"],
            "smtp_user": EMAIL_CONFIG["smtp_user"],
            "smtp_password": EMAIL_CONFIG["smtp_password"],
            "from_name": EMAIL_CONFIG["from_name"],
            "from_email": EMAIL_CONFIG["from_email"],
            "reply_to": EMAIL_CONFIG.get("reply_to", ""),
        }
        super().__init__(creds)
        self.smtp_host = creds["smtp_host"]
        self.smtp_port = creds["smtp_port"]
        self.smtp_user = creds["smtp_user"]
        self.smtp_password = creds["smtp_password"]
        self.from_name = creds.get("from_name", "")
        self.from_email = creds.get("from_email", self.smtp_user)
        self.reply_to = creds.get("reply_to", "")
        self.authenticated = False

    def authenticate(self) -> bool:
        """Test SMTP connection."""
        if not self.smtp_user or not self.smtp_password:
            return False
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
            self.authenticated = True
            return True
        except Exception as e:
            print(f"Email auth failed: {e}")
            return False

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html: bool = False,
        to_name: str = "",
    ) -> Dict[str, Any]:
        """
        Send a single email.

        Args:
            to_email: Recipient email
            subject: Email subject
            body: Email body (plain text or HTML)
            html: Whether body is HTML
            to_name: Recipient display name

        Returns:
            Result dict with success status
        """
        msg = MIMEMultipart("alternative")
        sender = f"{self.from_name} <{self.from_email}>" if self.from_name else self.from_email
        msg["From"] = sender
        msg["To"] = f"{to_name} <{to_email}>" if to_name else to_email
        msg["Subject"] = subject
        if self.reply_to:
            msg["Reply-To"] = self.reply_to

        content_type = "html" if html else "plain"
        msg.attach(MIMEText(body, content_type, "utf-8"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            self.last_post_time = datetime.now()
            return {
                "success": True,
                "post_id": f"email_{to_email}_{datetime.now().timestamp():.0f}",
                "platform": "email",
                "to": to_email,
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": f"Email send failed: {e}"}

    # ── PlatformAdapter interface ───────────────────────────────────

    def publish_post(
        self,
        text: str,
        images: Optional[List[Image.Image]] = None,
        scheduled_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        PlatformAdapter interface — sends text as email.
        For outreach, prefer send_email() with subject/body.
        """
        # Extract subject from first line if present
        lines = text.strip().split("\n", 1)
        subject = lines[0][:78] if lines else "Update"
        body = lines[1] if len(lines) > 1 else text

        return self.send_email(
            to_email=self.credentials.get("default_to", ""),
            subject=subject,
            body=body,
        )

    def get_analytics(
        self,
        post_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Email analytics — requires external tracking (Mailgun, SendGrid, etc.)."""
        return {
            "post_id": post_id,
            "platform": "email",
            "note": "Email tracking requires webhook integration (SendGrid/Mailgun)",
        }

    def validate_content(
        self, text: str, images: Optional[List[Image.Image]] = None
    ) -> Tuple[bool, Optional[str]]:
        """Validate email content."""
        if not text.strip():
            return False, "Email body cannot be empty"
        return True, None
