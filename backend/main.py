from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import json
import time

app = FastAPI()

# One global async queue (fast & simple)
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
    """
    Optimized SSE generator:
    - Non-blocking
    - Handles client disconnects cleanly
    """
    while True:
        if await request.is_disconnected():
            break
        try:
            message = await asyncio.wait_for(
                message_queue.get(), timeout=15
            )
            yield f"data: {json.dumps(message)}\n\n"
        except asyncio.TimeoutError:
            # keep-alive ping (important for proxies)
            yield "data: {}\n\n"

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
