from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.quiz_service import (
    get_random_quizzes,
    get_ai_quizzes,
    get_all_quizzes,
    create_quiz,
)
from app.schemas.quiz_schema import QuizSchema
from app.core.database import get_db

router = APIRouter(prefix="/quizzes")


@router.get("/random", response_model=list[QuizSchema])
@router.get("/random/{quizz_count}", response_model=list[QuizSchema])
def random_quizzes(db: Session = Depends(get_db), quizz_count: int = 5):
    """Get a list of random quizzes."""
    return get_random_quizzes(db, quizz_count)


@router.get("/ai/{quizz_count}", response_model=list[QuizSchema])
@router.get("/ai", response_model=list[QuizSchema])
async def generate_quizzes(db: Session = Depends(get_db), quizz_count: int = 5):
    """Generar una lista de quizzes utilizando IA."""
    return await get_ai_quizzes(db=db, quizz_count=quizz_count)


@router.get("/", response_model=list[QuizSchema])
def get_all_quizzes_endpoint(db: Session = Depends(get_db)):
    """Obtener todos los quizzes del sistema."""
    return get_all_quizzes(db)


from app.schemas.quiz_schema import CreateQuizSchema


@router.post("/", response_model=QuizSchema)
def create_quiz_endpoint(quiz_data: CreateQuizSchema, db: Session = Depends(get_db)):
    """Crear un nuevo quiz en el sistema."""
    return create_quiz(db=db, quiz_data=quiz_data)
