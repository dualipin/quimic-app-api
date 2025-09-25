from fastapi import APIRouter
from .games import router as games_router
from .auth import router as auth_router
from .landing import router as landing_router

router = APIRouter(prefix="/v1")
router.include_router(games_router)
router.include_router(auth_router)
router.include_router(landing_router)
