from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    email: EmailStr
    password: str


class PasswordRecoverySchema(BaseModel):
    email: EmailStr
