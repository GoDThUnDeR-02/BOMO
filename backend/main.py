from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time
import uuid

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Each client gets its own queue
clients: dict[str, asyncio.Queue] = {}

@app.get("/")
def root():
    return {"status": "BUMO running (FastAPI + SSE)"}

@app.post("/send")
async def send_message(payload: dict):
    message = {
        "text": payload["text"],
        "timestamp": time.time()
    }

    # 🔥 BROADCAST to ALL clients
    for queue in clients.values():
        await queue.put(message)

    return {"status": "sent"}

async def sse_event_generator(request: Request, client_id: str):
    queue = clients[client_id]

    try:
        while True:
            if await request.is_disconnected():
                break

            try:
                message = await asyncio.wait_for(queue.get(), timeout=15)
                yield f"data: {json.dumps(message)}\n\n"
            except asyncio.TimeoutError:
                yield "data: {}\n\n"  # keep-alive
    finally:
        # 🧹 cleanup on disconnect
        del clients[client_id]

@app.get("/events")
async def events(request: Request):
    client_id = str(uuid.uuid4())
    clients[client_id] = asyncio.Queue()

    return StreamingResponse(
        sse_event_generator(request, client_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
