import random
import uuid
from app.services.periodic_table_service import get_all_elements

from app.schemas.lottery_schema import PlayerCard, RoomState


def get_symbols() -> list[str]:
    elements = get_all_elements()
    return [element.symbol for element in elements]


ELEMENTS = get_symbols()


def generate_card() -> list[str]:
    return random.sample(ELEMENTS, 16)


def create_room(host_name: str) -> RoomState:
    room_code = str(uuid.uuid4())[:6].upper()
    host_id = str(uuid.uuid4())
    host_card = PlayerCard(
        player_id=host_id, elements=generate_card(), player_name=host_name
    )
    room = RoomState(
        room_code=room_code, host_id=host_id, players=[host_card], drawn_elements=[]
    )
    return room, host_card


def join_room(room: RoomState, player_name: str) -> PlayerCard:
    player_id = str(uuid.uuid4())
    card = PlayerCard(
        player_id=player_id, elements=generate_card(), player_name=player_name
    )
    room.players.append(card)
    return card


def draw_element(room: RoomState) -> str:
    remaining = list(set(ELEMENTS) - set(room.drawn_elements))
    if not remaining:
        return None
    element = random.choice(remaining)
    room.drawn_elements.append(element)
    return element
