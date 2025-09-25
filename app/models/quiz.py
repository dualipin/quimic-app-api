from sqlalchemy import Column, Integer, String
from sqlalchemy.types import JSON
from app.core.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    answer = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="medium", nullable=True)
    created_by = Column(String(50), default="system", nullable=True)
