import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
from app.services.lottery_service.state import rooms
from app.services.lottery_service.managers.game import draw_element

router = APIRouter()

# Diccionario para mantener conexiones por sala
connections: Dict[str, List[WebSocket]] = {}


async def schedule_room_deletion(
    room_code: str, delay: int = 900
):  # 900 segundos = 15 minutos
    await asyncio.sleep(delay)
    room = rooms.get(room_code)
    if room and not room.players:  # Solo eliminar si no hay jugadores
        rooms.pop(room_code, None)
        connections.pop(room_code, None)
        print(
            f"Sala {room_code} eliminada automáticamente tras 15 minutos de inactividad"
        )


@router.websocket("/ws/{room_code}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_id: str):
    await websocket.accept()

    if room_code not in connections:
        connections[room_code] = []
        asyncio.create_task(schedule_room_deletion(room_code))
    connections[room_code].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            player = rooms[room_code].players[0] if room_code in rooms else None
            if not player or player.player_id != player_id:
                await websocket.send_json({"error": "Jugador no encontrado en la sala"})
                await websocket.close()
                return

            if rooms.get(room_code) is None:
                await websocket.send_json({"error": "Sala no encontrada"})
                await websocket.close()
                return

            if rooms[room_code].winner:
                await websocket.send_json({"error": "Ya hay un ganador en esta sala"})
                continue

            if data["action"] == "bingo":
                room = rooms.get(room_code)
                if not room:
                    await websocket.send_json({"error": "Sala no encontrada"})
                    continue
                if room.winner:
                    await websocket.send_json({"error": "Ya hay un ganador"})
                    continue
                room.winner = player
                await broadcast(
                    room_code,
                    {
                        "event": "winner",
                        "player_id": player_id,
                        "player_name": data.get("player_name", "Jugador"),
                        "message": f"{data.get('player_name', 'Jugador')} ha ganado el bingo",
                    },
                )
            elif data["action"] == "draw":
                room = rooms.get(room_code)
                if not room or room.host_id != player_id:
                    await websocket.send_json({"error": "No autorizado para lanzar"})
                    continue

                element = draw_element(room)
                if not element:
                    await broadcast(
                        room_code,
                        {
                            "event": "end",
                            "message": "Todos los elementos han sido lanzados",
                        },
                    )
                    continue

                await broadcast(room_code, {"event": "draw", "element": element})

    except WebSocketDisconnect:
        connections[room_code].remove(websocket)

        # If the room exists but has no players after removal, delete the room

        room = rooms.get(room_code)
        player_name = "Desconocido"

        if room:
            for p in room.players:
                if p.player_id == player_id:
                    player_name = p.player_name
                    break

            room.players = [p for p in room.players if p.player_id != player_id]

        await broadcast(
            room_code,
            {
                "event": "player_left",
                "player_id": player_id,
                "player_name": player_name,
                "remaining_players": len(room.players) if room else 0,
                "message": f"{player_name} ha salido de la sala",
            },
        )

        if room and not room.players:
            del rooms[room_code]
            print(f"Room {room_code} deleted because it has no players")

        if not connections[room_code]:
            del connections[room_code]


async def broadcast(room_code: str, message: dict):
    for connection in connections.get(room_code, []):
        await connection.send_json(message)
