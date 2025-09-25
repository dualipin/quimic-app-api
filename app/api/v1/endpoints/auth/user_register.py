from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_service import register_user

router = APIRouter()


@router.post("/register", tags=["User Registration"])
async def user_register(user: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    try:
        user = await register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during user registration: {str(e)}",
        )

    return user
