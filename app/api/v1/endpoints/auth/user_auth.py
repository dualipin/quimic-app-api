from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth_schema import AuthSchema, PasswordRecoverySchema
from app.schemas.user_schema import UserRead
from app.services.auth_service import authenticate_user, password_recovery
from app.core.database import get_db

router = APIRouter()


@router.post("/login", response_model=UserRead)
async def user_login(auth: AuthSchema, db: Session = Depends(get_db)):
    result = authenticate_user(auth, db)
    return result


@router.post("/recover")
async def forgot_password(
    recovery: PasswordRecoverySchema, db: Session = Depends(get_db)
):
    result = await password_recovery(recovery.email, db)
    return {"message": result}
