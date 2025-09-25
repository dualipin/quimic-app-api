from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.lottery_schema import (
    CreateRoomRequest,
    JoinRoomRequest,
    RoomState,
    PlayerCard,
    CreateRoomResponse,
)
from app.services.lottery_service.managers import game as game_logic
from app.services.lottery_service.state import rooms

router = APIRouter()


@router.get("/rooms", response_model=List[RoomState])
def get_rooms():
    return list(rooms.values())


@router.post("/rooms", response_model=CreateRoomResponse)
def create_room(data: CreateRoomRequest):
    room, host_card = game_logic.create_room(data.host_name)
    rooms[room.room_code] = room
    return CreateRoomResponse(room=room, host_card=host_card)


@router.post("/join")
def join_room(data: JoinRoomRequest):
    room = rooms.get(data.room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    card = game_logic.join_room(room, data.player_name)
    return {"room": room, "player_card": card}
