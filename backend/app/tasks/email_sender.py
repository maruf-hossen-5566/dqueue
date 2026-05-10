from smtplib import SMTPException

import resend
from email_validator import validate_email, EmailNotValidError

from app.core.config import settings
from app.core.logging import setup_logger
from app.tasks.registry import task
from app.worker_logic.exception import TaskException

logger = setup_logger(__name__)

resend.api_key = settings.RESEND_API_KEY


@task(name="send_email")
async def send_email(payload: str):
    if not payload or not payload.strip():
        raise ValueError("Payload is missing")

    emails = set(
        [mail.strip() for mail in payload.split(",") if mail.strip()],
    )

    valid_emails = []
    for email in emails:
        try:
            validated_email = validate_email(email)
            valid_emails.append(validated_email.email)
        except EmailNotValidError as error:
            raise TaskException(f"Invalid email '{email}': {error}")

    if not valid_emails:
        raise ValueError(f"Invalid email(s): {payload}")

    mail_body = f"""
        <div>
            <h1>DQueue — Distributed Task Processing System for Python</h1>
            <h3>This email sent using <strong>DQueue</strong></h3>
        </div>
        """

    params: resend.Emails.SendParams = {
        "from": f"{settings.RESEND_NAME} <{settings.RESEND_EMAIL}>",
        "to": list(valid_emails),
        "subject": "DQueue - Distributed Task Processing System for Python",
        "html": mail_body,
    }
    try:
        resend.Emails.send(params)
        logger.info(f"Mail sent successfully to <{valid_emails}>")
    except SMTPException as error:
        logger.error(f"Failed to send email to <{emails}>:{error}")
        raise TaskException(error) from error
    except Exception as error:
        logger.error(f"Failed to send email to <{emails}>:{error}")
        raise TaskException(error) from error
