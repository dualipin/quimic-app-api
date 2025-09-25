from fastapi import APIRouter
from .user_register import router as user_register_router
from .user_auth import router as user_auth_router

router = APIRouter(prefix="/auth")

router.include_router(user_register_router, tags=["User Registration"])
router.include_router(user_auth_router, tags=["User Authentication"])
