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

def generate_realistic_metrics():
    clusters = [
        {
            "id": "h100-cluster-1",
            "name": "NVIDIA H100 Cluster",
            "location": "US-West",
            "gpu_utilization": round(np.random.uniform(85, 98), 1),
            "memory_usage": round(np.random.uniform(60, 80), 2),
            "temperature": round(np.random.uniform(65, 75), 1),
            "power_draw": round(np.random.uniform(1.8, 2.1), 2),
            "efficiency_score": round(np.random.uniform(90, 97), 1),
            "renewable_pct": round(np.random.uniform(60, 75), 1),
            "active_gpus": random.randint(240, 256),
            "total_gpus": 256
        },
        {
            "id": "a100-cluster-1",
            "name": "NVIDIA A100 Cluster",
            "location": "US-East",
            "gpu_utilization": round(np.random.uniform(80, 95), 1),
            "memory_usage": round(np.random.uniform(50, 70), 2),
            "temperature": round(np.random.uniform(70, 80), 1),
            "power_draw": round(np.random.uniform(0.8, 1.2), 2),
            "efficiency_score": round(np.random.uniform(85, 93), 1),
            "renewable_pct": round(np.random.uniform(40, 55), 1),
            "active_gpus": random.randint(100, 128),
            "total_gpus": 128
        }
    ]
    
    recommendations = [
        {
            "id": "rec-1",
            "cluster_id": "h100-cluster-1",
            "action": "Shift non-critical jobs to off-peak hours (2am-6am)",
            "estimated_savings_monthly": round(np.random.uniform(15000, 20000), 0),
            "priority": "high"
        },
        {
            "id": "rec-2",
            "cluster_id": "a100-cluster-1",
            "action": "Optimize cooling system and increase airflow",
            "estimated_savings_monthly": round(np.random.uniform(7000, 10000), 0),
            "priority": "medium"
        },
        {
            "id": "rec-3",
            "cluster_id": "h100-cluster-1",
            "action": "Enable power capping during low utilization periods",
            "estimated_savings_monthly": round(np.random.uniform(8000, 12000), 0),
            "priority": "medium"
        }
    ]
    
    total_power = sum(c["power_draw"] for c in clusters)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "clusters": clusters,
        "recommendations": recommendations,
        "total_power_mw": round(total_power, 2),
        "grid_carbon_intensity": round(np.random.uniform(0.3, 0.6), 3)
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-gpu-brain-v2",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
def root():
    return {
        "message": "AI GPU Energy Optimizer API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/optimize")
def get_optimization():
    return generate_realistic_metrics()

@app.post("/optimize")
def post_optimization(input: GPUInput):
    metrics = generate_realistic_metrics()
    metrics["input_received"] = input.dict()
    return metrics

@app.post("/api/v1/metrics")
async def receive_metrics(
    metrics: ClusterMetrics,
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth format. Use Bearer token")
    
    api_key = authorization.replace("Bearer ", "")
    
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if metrics.cluster_id not in metrics_store:
        metrics_store[metrics.cluster_id] = []
    
    metrics_store[metrics.cluster_id].append(metrics.model_dump())
    
    if len(metrics_store[metrics.cluster_id]) > 500:
        metrics_store[metrics.cluster_id] = metrics_store[metrics.cluster_id][-500:]
    
    print(f"✅ Received metrics for cluster: {metrics.cluster_id} ({len(metrics.gpus)} GPUs)")
    
    return {"status": "ok", "received": True}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    last_ping = datetime.now()
    
    try:
        while True:
            data = generate_realistic_metrics()
            await websocket.send_json(data)
            
            if (datetime.now() - last_ping).seconds > 10:
                await websocket.send_json({"type": "ping"})
                last_ping = datetime.now()
            
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
