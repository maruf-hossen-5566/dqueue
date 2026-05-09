from smtplib import SMTPException

from email_validator import validate_email, EmailNotValidError
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings
from app.core.logging import setup_logger
from app.tasks.registry import task
from app.worker_logic.exception import TaskException

logger = setup_logger(__name__)

config = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_ADDRESS,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_ADDRESS,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


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
            <p>This email sent using <strong>DQueue</strong></p>
        </div>
        """
    message = MessageSchema(
        subject="DQueue - Distributed Task Processing System for Python",
        recipients=list(valid_emails),
        body=mail_body,
        subtype=MessageType.html,
    )
    try:
        fm = FastMail(config=config)
        await fm.send_message(message)
        logger.info(f"Mail sent successfully to <{emails}>")
    except SMTPException as error:
        logger.error(f"Failed to send email to <{emails}>:{error}")
        raise TaskException(error) from error
