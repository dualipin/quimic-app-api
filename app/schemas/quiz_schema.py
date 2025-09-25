from pydantic import BaseModel
from typing import Optional


class QuizSchema(BaseModel):
    """Schema for quiz questions."""

    id: Optional[int] = None
    question: str
    options: list[str | dict[str, bool]]
    answer: str
    difficulty: Optional[str] = "medium"
    created_by: Optional[str] = "system"

    model_config = {"from_attributes": True}


class CreateQuizSchema(QuizSchema):
    """Schema for creating a quiz question."""

    id: None
