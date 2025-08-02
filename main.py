from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from collections import deque
import asyncio, random, time

app = FastAPI()
# serve our static frontend at root
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    html = Path("static/index.html").read_text()
    return HTMLResponse(content=html)

# keep last 1k events
EVENT_QUEUE = deque(maxlen=1000)

@app.websocket("/ws/events")
async def events_ws(ws: WebSocket):
    await ws.accept()
    while True:
        event = {"timestamp": time.time(), "value": random.random()}
        EVENT_QUEUE.append(event)
        await ws.send_json(event)
        await asyncio.sleep(0.1)  # 10 events/sec

@app.websocket("/ws/metrics")
async def metrics_ws(ws: WebSocket):
    await ws.accept()
    while True:
        now = time.time()
        recent = [e for e in EVENT_QUEUE if now - e["timestamp"] <= 1]
        throughput = len(recent)
        avg_value = sum(e["value"] for e in recent) / throughput if throughput else 0
        await ws.send_json({"throughput": throughput, "avg_value": avg_value})
        await asyncio.sleep(1)  # 1 update/sec

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80)

