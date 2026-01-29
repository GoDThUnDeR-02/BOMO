from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.websocket_manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

@app.get("/")
async def root():
    return {"status": "BUMO FastAPI running"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()   # 🔥 EXPLICIT ACCEPT (important for Render)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        pass
