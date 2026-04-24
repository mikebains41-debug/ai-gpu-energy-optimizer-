from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import random
from datetime import datetime
import asyncio
import json
import os
from typing import List, Optional
from fastapi import Header, HTTPException

# Database disabled – mock data only
# from database import SessionLocal, GPUMetric

app = FastAPI(title="AI GPU Energy Optimizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GPUInput(BaseModel):
    gpu_utilization: float
    memory_usage: float
    temperature: float

class GPUMetric(BaseModel):
    gpu_id: int
    utilization_percent: float
    memory_used_gb: float
    memory_total_gb: Optional[float] = 80.0
    temperature_celsius: float
    power_draw_watts: float

class ClusterMetrics(BaseModel):
    cluster_id: str
    timestamp: float
    gpus: List[GPUMetric]

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()
metrics_store = {}
VALID_API_KEYS = os.environ.get("VALID_API_KEYS", "test_key_123,gpu_opt_demo").split(",")

def validate_api_key(api_key: str) -> bool:
    return api_key in VALID_API_KEYS

# ========== MOCK DATA FOR DASHBOARD ==========
def generate_realistic_metrics():
    clusters = [
        {
            "id": "h100-cluster-1",
            "name": "NVIDIA H100 Cluster",
            "location": "US-West",
            "gpu_utilization": round(random.uniform(85, 98), 1),
            "memory_usage": round(random.uniform(12, 15), 2),
            "temperature": round(random.uniform(65, 78), 1),
            "power_draw": round(random.uniform(1.5, 2.1), 2),
            "efficiency_score": round(random.uniform(90, 97), 1)
        },
        {
            "id": "a100-cluster-1",
            "name": "NVIDIA A100 Cluster",
            "location": "US-East",
            "gpu_utilization": round(random.uniform(80, 95), 1),
            "memory_usage": round(random.uniform(10, 14), 2),
            "temperature": round(random.uniform(70, 82), 1),
            "power_draw": round(random.uniform(0.8, 1.2), 2),
            "efficiency_score": round(random.uniform(85, 93), 1)
        }
    ]
    recommendations = []
    total_power = sum(c["power_draw"] for c in clusters)
    return {
        "clusters": clusters,
        "recommendations": recommendations,
        "total_power_mw": round(total_power, 2),
        "grid_carbon_intensity": round(random.uniform(0.3, 0.6), 3)
    }

# ========== API ENDPOINTS ==========
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-gpu-brain-v4"}

@app.get("/")
def root():
    return {"message": "AI GPU Energy Optimizer API", "docs": "/docs", "health": "/health"}

@app.get("/optimize")
def get_optimization():
    return generate_realistic_metrics()

@app.post("/api/v1/metrics")
async def receive_metrics(
    metrics: ClusterMetrics,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization")
    
    api_key = authorization.replace("Bearer ", "")
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if metrics.cluster_id not in metrics_store:
        metrics_store[metrics.cluster_id] = []
    metrics_store[metrics.cluster_id].append(metrics.model_dump())
    
    if len(metrics_store[metrics.cluster_id]) > 500:
        metrics_store[metrics.cluster_id] = metrics_store[metrics.cluster_id][-500:]
    
    # Database disabled – mock data only
    # try:
    #     db = SessionLocal()
    #     for gpu in metrics.gpus:
    #         db_metric = GPUMetric(...)
    #         db.add(db_metric)
    #     db.commit()
    # except Exception as e:
    #     print(f"DB error: {e}")
    # finally:
    #     db.close()
    
    return {"status": "ok", "received": True}

@app.get("/metrics")
def get_metrics():
    return metrics_store

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(2)
            await websocket.send_json({"type": "ping", "timestamp": datetime.now().isoformat()})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
