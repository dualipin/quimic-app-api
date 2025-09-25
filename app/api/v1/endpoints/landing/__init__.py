from fastapi import APIRouter
from .history import router as history_router
from .timeline import router as timeline_router
from .periodic_table import router as periodic_table_router

router = APIRouter(prefix="/landing", tags=["Landing Endpoints"])

router.include_router(history_router)
router.include_router(timeline_router)
router.include_router(periodic_table_router)
