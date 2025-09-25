from fastapi_mail import ConnectionConfig
from typing import Annotated
from app.core.config import Settings, get_settings


def get_mail_config(settings: Annotated[Settings, get_settings]):
    return ConnectionConfig(
        MAIL_FROM_NAME="Studying Chemistry",
        MAIL_USERNAME=settings.email_from,
        MAIL_PASSWORD=settings.email_password,
        MAIL_FROM=f"Studying Chemistry <{settings.email_from}>",
        MAIL_PORT=587,
        MAIL_SERVER=settings.email_host,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        TEMPLATE_FOLDER="app/core/templates",
    )


# Configuración de la conexión SMTP
conf = get_mail_config(get_settings())
