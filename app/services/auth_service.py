from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi_mail import MessageSchema, MessageType, FastMail
from app.core.mail import conf
from app.core.security import Hasher
from app.schemas.auth_schema import AuthSchema
from app.schemas.user_schema import UserRead
from app.models.user import User


def authenticate_user(auth: AuthSchema, db: Session = None) -> UserRead:
    user = db.query(User).filter(User.email == auth.email).first()
    if not user or not Hasher.verify_password(auth.password, user.hashed_password):
        return None
    if user:
        return UserRead.model_validate(user)
    return None


async def password_recovery(email: str, db: Session) -> str:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return "Usuario no encontrado"
    new_password = "nueva"
    user.hashed_password = Hasher.get_password_hash(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    await send_password_recovery_email(
        email=user.email, full_name=user.full_name, new_password=new_password
    )

    return "Contraseña actualizada y enviada por correo electrónico"


async def send_password_recovery_email(
    email: EmailStr, full_name: str, new_password: str = None
):
    message = MessageSchema(
        subject="Recupera tu contraseña",
        recipients=[email],
        template_body={"full_name": full_name, "new_password": new_password},
        subtype=MessageType.html,
    )

    fm = FastMail(conf)

    await fm.send_message(message, template_name="password_recovery.html")
