from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    alumno = "alumno"
    profesor = "profesor"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    full_name = Column(String(255), index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.alumno, nullable=False)
