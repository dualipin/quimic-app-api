from sqlalchemy.orm import Session
from app.models.user import User
from pydantic import EmailStr
from fastapi_mail import MessageSchema, MessageType, FastMail
from app.schemas.user_schema import UserCreate, UserRead
from app.core.mail import conf
from app.core.security import Hasher  # Asegúrate de que esto exista


async def send_welcome_email(email: str, full_name: str):
    message = MessageSchema(
        subject="Bienvenido a Studying Chemistry",
        recipients=[email],
        template_body={"full_name": full_name},
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    return await fm.send_message(message, template_name="welcome.html")


async def register_user(db: Session, user: UserCreate) -> UserRead:
    # Extraemos los campos necesarios para crear el modelo SQLAlchemy
    user_data = user.model_dump(exclude={"password"})

    # Creamos el usuario con la contraseña hasheada
    db_user = User(**user_data)
    db_user.hashed_password = Hasher.get_password_hash(user.password)
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise ValueError("Correo electrónico ya registrado")
    except ValueError as e:
        raise e

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Enviamos el correo de bienvenida
    await send_welcome_email(email=db_user.email, full_name=db_user.full_name)

    return UserRead.model_validate(db_user)
