"""
AI Optimization Engine API & Real-Time Stream
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List
from datetime import datetime
from optimizer import engine, Recommendation
from metrics_simulator import generate_cluster_metrics
import os
import requests

app = FastAPI(title="AI GPU Optimization Engine", version="1.0.0")

# Allow Next.js frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/metrics")
async def get_metrics():
    telemetry_url = os.getenv("GPU_TELEMETRY_URL")
    
    # 1. Try to fetch real data from Colab if URL is set
    if telemetry_url:
        try:
            print(f"🔍 Fetching from Colab: {telemetry_url}")
            response = requests.get(telemetry_url, timeout=10)
            response.raise_for_status()
            real_data = response.json()
            print(f"✅ Got real data: {real_data}")
            
            # Return the real data
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "real_gpu": real_data,
                "is_mock": False
            }
        except Exception as e:
            print(f"❌ Failed to fetch from Colab (using mock): {e}")

    # 2. Fallback to Fake Data if Colab is down
    print("⚠️ Using Mock Data")
    clusters, carbon = generate_cluster_metrics()
    recommendations = engine.analyze(clusters, carbon)
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "clusters": [c.dict() for c in clusters],
        "recommendations": [r.dict() for r in recommendations],
        "grid_carbon_intensity": carbon,
        "total_power_mw": sum(c.power_draw for c in clusters),
        "avg_utilization": sum(c.utilization for c in clusters) / len(clusters),
        "is_mock": True
    }

@app.post("/api/apply-recommendation/{rec_id}")
async def apply_recommendation(rec_id: str):
    return {"status": "applied", "recommendation_id": rec_id, "action": "simulated"}

async def live_stream_loop():
    while True:
        metrics = await get_metrics()
        await manager.broadcast(metrics)        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(live_stream_loop())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
