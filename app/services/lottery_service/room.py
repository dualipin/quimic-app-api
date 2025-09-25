import uuid
from typing import List
from app.schemas.lottery_schema import RoomCreate, Room, Player


class RoomService:
    def __init__(self):
        self.rooms: List[Room] = []

    def create_room(self, room_data: RoomCreate, user_id: str) -> Room:
        room = Room(id=str(uuid.uuid4())[:8], name=room_data.name, host=user_id)
        self.rooms.append(room)
        return room

    def get_rooms(self):
        return self.rooms

    def get_room_by_id(self, room_id: str) -> Room | None:
        # Using next with a generator expression and a default value
        # This is more efficient than a full loop when we only need the first match
        return next((room for room in self.rooms if room.id == room_id), None)

    def add_player_to_room(self, room_id: str, player: Player) -> Room | None:
        room = self.get_room_by_id(room_id)
        if room:
            room.players.append(player)
            return room
        return None

    def remove_player_from_room(self, room_id: str, player_id: str) -> Room | None:
        room = self.get_room_by_id(room_id)
        if not room:
            return None

        # Find player index to avoid creating a new list unnecessarily
        for i, player in enumerate(room.players):
            if player.id == player_id:
                room.players.pop(i)
                break

        return room
