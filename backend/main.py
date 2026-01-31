from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time

app = FastAPI()

# ✅ CORS FIX (THIS IS THE KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

message_queue = asyncio.Queue()

@app.get("/")
def root():
    return {"status": "BUMO running (FastAPI + SSE)"}

@app.post("/send")
async def send_message(payload: dict):
    message = {
        "text": payload["text"],
        "timestamp": time.time()
    }
    await message_queue.put(message)
    return {"status": "sent"}

async def sse_event_generator(request: Request):
    while True:
        if await request.is_disconnected():
            break
        try:
            message = await asyncio.wait_for(message_queue.get(), timeout=15)
            yield f"data: {json.dumps(message)}\n\n"
        except asyncio.TimeoutError:
            yield "data: {}\n\n"  # keep-alive

@app.get("/events")
async def events(request: Request):
    return StreamingResponse(
        sse_event_generator(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
