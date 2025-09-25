from fastapi import WebSocket, WebSocketDisconnect, WebSocketException


class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        self.active_connections[room_id] = websocket

    def disconnect(self, room_id: str):
        if room_id in self.active_connections:
            del self.active_connections[room_id]

    async def send_message(self, room_id: str, message: str):
        if room_id in self.active_connections:
            websocket = self.active_connections[room_id]
            await websocket.send_json(message)

    async def receive_message(self, room_id: str) -> str:
        if room_id in self.active_connections:
            websocket = self.active_connections[room_id]
            try:
                return await websocket.receive_json()
            except WebSocketDisconnect:
                self.disconnect(room_id)
                raise
            except WebSocketException as e:
                raise e
        else:
            raise ValueError("No active connection for this room")
