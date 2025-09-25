from fastapi import APIRouter
from .periodic_table import router as periodic_table_router
from .quiz import router as quiz_router
from .lottery import router as lottery_router
from .rankig import router as ranking_router

router = APIRouter(prefix="/games")

router.include_router(periodic_table_router, tags=["Periodic Table"])

router.include_router(quiz_router, tags=["Quiz"])

router.include_router(lottery_router, tags=["Lottery"])

router.include_router(ranking_router, tags=["Ranking"])
