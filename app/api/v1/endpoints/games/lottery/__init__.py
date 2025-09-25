from fastapi import APIRouter
from .room import router as room_router
from .websocket import router as websocket_router


router = APIRouter(prefix="/lottery")


router.include_router(room_router)
router.include_router(websocket_router)
