from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def broadcast(self, message: str, room: str):
        connections = self.active_connections.get(room, [])
        for connection in connections:
            await connection.send_text(message)
