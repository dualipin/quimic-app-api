from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    alumno = "alumno"
    profesor = "profesor"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Optional[UserRole] = UserRole.alumno


class UserCreate(UserBase):
    password: str  # Plain password for creation


class UserRead(UserBase):
    id: int
    is_active: Optional[bool] = True

    model_config = {"from_attributes": True}


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: Optional[bool] = True

    model_config = {"from_attributes": True}
