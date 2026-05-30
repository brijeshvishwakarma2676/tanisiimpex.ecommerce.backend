"""
Email service for sending inquiry notifications.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from jinja2 import Template

from app.core.config import settings


# --- Email Templates ---

ADMIN_NOTIFICATION_TEMPLATE = """
<html>
<body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa; padding: 20px;">
  <div style="background: #ffffff; border-radius: 12px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <h2 style="color: #1a1a2e; margin-top: 0;">📩 New Product Inquiry</h2>
    <hr style="border: none; border-top: 2px solid #e8e8e8; margin: 16px 0;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr><td style="padding: 8px 0; color: #666; width: 140px;">Product:</td><td style="padding: 8px 0; font-weight: 600;">{{ product_name }}</td></tr>
      <tr><td style="padding: 8px 0; color: #666;">Customer:</td><td style="padding: 8px 0;">{{ customer_name }}</td></tr>
      <tr><td style="padding: 8px 0; color: #666;">Email:</td><td style="padding: 8px 0;">{{ email }}</td></tr>
      <tr><td style="padding: 8px 0; color: #666;">Phone:</td><td style="padding: 8px 0;">{{ phone }}</td></tr>
      <tr><td style="padding: 8px 0; color: #666;">Company:</td><td style="padding: 8px 0;">{{ company_name }}</td></tr>
      <tr><td style="padding: 8px 0; color: #666;">Quantity:</td><td style="padding: 8px 0;">{{ quantity_required }} units</td></tr>
    </table>
    <div style="margin-top: 16px; padding: 16px; background: #f8f9fa; border-radius: 8px;">
      <p style="color: #666; margin: 0 0 8px 0; font-size: 13px;">Message:</p>
      <p style="margin: 0; color: #333;">{{ message }}</p>
    </div>
  </div>
</body>
</html>
"""

CUSTOMER_CONFIRMATION_TEMPLATE = """
<html>
<body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa; padding: 20px;">
  <div style="background: #ffffff; border-radius: 12px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <h2 style="color: #1a1a2e; margin-top: 0;">Thank You for Your Inquiry!</h2>
    <p style="color: #555; line-height: 1.6;">
      Dear {{ customer_name }},<br><br>
      We have received your inquiry for <strong>{{ product_name }}</strong>.
      Our team will review your requirements and get back to you within 24 hours.
    </p>
    <div style="margin-top: 20px; padding: 16px; background: #f0f7ff; border-radius: 8px; border-left: 4px solid #3b82f6;">
      <p style="margin: 0; color: #333; font-size: 14px;">
        <strong>Inquiry Details:</strong><br>
        Product: {{ product_name }}<br>
        Quantity: {{ quantity_required }} units
      </p>
    </div>
    <p style="color: #555; margin-top: 20px; line-height: 1.6;">
      If you have any urgent questions, feel free to reach us on WhatsApp or call us directly.
    </p>
    <p style="color: #888; font-size: 13px; margin-top: 24px;">
      Best Regards,<br>
      <strong>{{ company_name }}</strong>
    </p>
  </div>
</body>
</html>
"""


def send_email(
    to_email: str,
    subject: str,
    html_body: str,
    from_name: Optional[str] = None,
) -> bool:
    """Send an email using SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{from_name or settings.APP_NAME} <{settings.SMTP_USER}>"
        msg["To"] = to_email

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


def send_inquiry_admin_notification(inquiry_data: dict) -> bool:
    """Send inquiry notification to admin."""
    template = Template(ADMIN_NOTIFICATION_TEMPLATE)
    html = template.render(**inquiry_data)
    return send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=f"New Inquiry: {inquiry_data.get('product_name', 'Unknown Product')}",
        html_body=html,
    )


def send_inquiry_customer_confirmation(inquiry_data: dict) -> bool:
    """Send confirmation email to customer."""
    template = Template(CUSTOMER_CONFIRMATION_TEMPLATE)
    html = template.render(**inquiry_data, company_name=settings.APP_NAME)
    return send_email(
        to_email=inquiry_data["email"],
        subject=f"Inquiry Received - {settings.APP_NAME}",
        html_body=html,
    )
