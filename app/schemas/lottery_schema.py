from pydantic import BaseModel
from typing import List, Optional


class CreateRoomRequest(BaseModel):
    host_name: str


class JoinRoomRequest(BaseModel):
    room_code: str
    player_name: str


class Player(BaseModel):
    player_id: str
    player_name: str = None


class PlayerCard(Player):
    elements: List[str]


class RoomState(BaseModel):
    room_code: str
    host_id: str
    players: List[PlayerCard]
    drawn_elements: List[str]
    winner: Optional[Player] = None


class CreateRoomResponse(BaseModel):
    room: RoomState
    host_card: PlayerCard = None
