import json
import random
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from app.models.quiz import Quiz
from app.schemas.quiz_schema import QuizSchema
from .gemeni_service import model


def load_initial_quizzes() -> list[Quiz]:
    """
    Load the initial quiz data and return Quiz instances (not yet in DB).
    """
    file_path = Path("app") / "statics" / "json" / "quizzes.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Quiz data file not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        quizzes_data: list[dict] = json.load(file)

    return [Quiz(**item) for item in quizzes_data]


def remove_dictionary_options(quiz: Quiz) -> Quiz:
    """
    Remove dictionary options from the quiz object.
    """
    quiz.options = [
        option if isinstance(option, str) else list(option.keys())[0]
        for option in quiz.options
    ]
    return quiz


def get_random_quizzes(db: Session, quizz_count: int = 5) -> list[QuizSchema]:
    """
    Get random quizzes from the database. Load from JSON if DB is empty.
    """
    existing_quizzes = db.query(Quiz).filter(Quiz.created_by == "system").all()

    if not existing_quizzes:
        new_quizzes = load_initial_quizzes()
        db.add_all(new_quizzes)
        db.commit()
        db.refresh(new_quizzes[0])  # Opcional
        existing_quizzes = new_quizzes

    if quizz_count <= 0:
        return []

    all_quizzes = db.query(Quiz).all()
    if not all_quizzes:
        raise ValueError("No quizzes available in the database.")

    quizz_count = min(quizz_count, len(all_quizzes))
    selected = random.sample(all_quizzes, quizz_count)
    selected = [remove_dictionary_options(quiz) for quiz in selected]

    return [QuizSchema.model_validate(quiz) for quiz in selected]


def generate_ai_quizzes_with_gemini(count: int) -> list[dict]:
    prompt = f"""Genera {count} preguntas sobre química para estudiantes de preparatoria con diferentes grados de dificultad.
Cada pregunta debe tener 4 opciones y una respuesta correcta.
Responde únicamente con un array JSON como este:

[
  {{
    "question": "¿Cuál es el símbolo químico del sodio?",
    "options": [
      {{"Na"}},
      {{"S"}},
      {{"So"}},
      {{"N"}}
    ],
    "difficulty": {{ "hard" | "medium" | "easy"}},
    "answer": "Na"
  }}
]
"""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        print("✅ Respuesta bruta del modelo:", raw_text)

        # --- Limpieza de la respuesta ---
        # Elimina "```json" y "```" si el modelo los añade
        if raw_text.startswith("```json"):
            json_text = raw_text[len("```json") :].strip()
            if json_text.endswith("```"):
                json_text = json_text[: -len("```")].strip()
        else:
            json_text = raw_text
        # --- Fin de limpieza ---

        print("✅ JSON después de la limpieza:", json_text)

        if not json_text:
            raise ValueError(
                "No se encontró un array JSON válido en la respuesta después de la limpieza."
            )

        # Intenta parsear el JSON
        parsed_json = json.loads(json_text)
        print("✅ Preguntas generadas y parseadas correctamente.")
        return parsed_json

    except json.JSONDecodeError as e:
        print(f"❌ Error de formato JSON al parsear la respuesta: {e}")
        print(f"❌ La cadena que intentó parsear fue: '{json_text}'")
        return []
    except Exception as e:
        print(f"❌ Error general al generar o parsear las preguntas: {e}")
        return []


async def get_ai_quizzes(db: Session, quizz_count: int = 5) -> list[QuizSchema]:
    """
    Obtener quizzes generados por IA, y siempre generar y guardar nuevos además de los existentes.
    """
    if quizz_count <= 0:
        return []

    # Generar nuevos quizzes con IA
    ai_quizzes = generate_ai_quizzes_with_gemini(quizz_count)

    new_quizzes = []
    for item in ai_quizzes:
        # Validar existencia por pregunta
        exists_query = db.query(
            exists().where(Quiz.question == item["question"])
        ).scalar()

        if not exists_query:
            quiz = Quiz(
                question=item["question"],
                options=item["options"],
                answer=item["answer"],
                difficulty=item.get("difficulty", "medium"),
                created_by="IA",
            )
            db.add(quiz)
            new_quizzes.append(quiz)

    db.commit()

    for quiz in new_quizzes:
        db.refresh(quiz)

    # Combinar los nuevos quizzes con los existentes
    existing_quizzes = db.query(Quiz).filter(Quiz.created_by == "IA").all()
    selected = random.sample(existing_quizzes, min(quizz_count, len(existing_quizzes)))

    selected = [remove_dictionary_options(quiz) for quiz in selected]

    return [QuizSchema.model_validate(quiz) for quiz in selected]


def get_all_quizzes(db: Session) -> list[QuizSchema]:
    """
    Obtener todos los quizzes del sistema.
    """
    quizzes = db.query(Quiz).all()

    # options = [key for item in quizzes for key in item.options]
    if not quizzes:
        return []

    quizzes = [remove_dictionary_options(quiz) for quiz in quizzes]

    return [QuizSchema.model_validate(quiz) for quiz in quizzes]


from app.schemas.quiz_schema import CreateQuizSchema


def create_quiz(db: Session, quiz_data: CreateQuizSchema) -> QuizSchema:
    """
    Crear un nuevo quiz en el sistema.
    """
    quiz = Quiz(
        question=quiz_data.question,
        options=quiz_data.options,
        answer=quiz_data.answer,
        difficulty=quiz_data.difficulty,
        created_by=quiz_data.created_by,
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return QuizSchema.model_validate(quiz)
