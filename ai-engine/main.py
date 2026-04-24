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

# ========== MOCK DATA FOR DASHBOARD (fallback) ==========
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
            "efficiency_score": round(random.uniform(90, 97), 1),
            "active_gpus": random.randint(240, 256),
            "total_gpus": 256,
            "renewable_pct": round(random.uniform(60, 75), 1)
        },
        {
            "id": "a100-cluster-1",
            "name": "NVIDIA A100 Cluster",
            "location": "US-East",
            "gpu_utilization": round(random.uniform(80, 95), 1),
            "memory_usage": round(random.uniform(10, 14), 2),
            "temperature": round(random.uniform(70, 82), 1),
            "power_draw": round(random.uniform(0.8, 1.2), 2),
            "efficiency_score": round(random.uniform(85, 93), 1),
            "active_gpus": random.randint(100, 128),
            "total_gpus": 128,
            "renewable_pct": round(random.uniform(40, 55), 1)
        }
    ]
    recommendations = [
        {
            "id": "rec-1",
            "cluster_id": "h100-cluster-1",
            "action": "Shift non-critical jobs to off-peak hours (2am-6am)",
            "estimated_savings_monthly": round(random.uniform(15000, 20000), 0),
            "priority": "high"
        },
        {
            "id": "rec-2",
            "cluster_id": "a100-cluster-1",
            "action": "Optimize cooling system and increase airflow",
            "estimated_savings_monthly": round(random.uniform(7000, 10000), 0),
            "priority": "medium"
        },
        {
            "id": "rec-3",
            "cluster_id": "h100-cluster-1",
            "action": "Enable power capping during low utilization periods",
            "estimated_savings_monthly": round(random.uniform(8000, 12000), 0),
            "priority": "medium"
        }
    ]
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

# ========== NEW /optimize endpoint that returns real stored metrics if available ==========
@app.get("/optimize")
def get_optimization():
    # If we have stored metrics, return the latest one for each cluster
    if metrics_store:
        clusters = []
        for cluster_id, measurements in metrics_store.items():
            if measurements:
                latest = measurements[-1]
                gpu_data = latest.get("gpus", [{}])[0]
                clusters.append({
                    "id": cluster_id,
                    "name": cluster_id.upper().replace("-", " "),
                    "location": "Unknown",
                    "gpu_utilization": gpu_data.get("utilization_percent", 0),
                    "memory_usage": gpu_data.get("memory_used_gb", 0),
                    "temperature": gpu_data.get("temperature_celsius", 0),
                    "power_draw": gpu_data.get("power_draw_watts", 0) / 1000,
                    "efficiency_score": 90 + (gpu_data.get("utilization_percent", 0) / 10),
                    "active_gpus": 1,      # you can improve later
                    "total_gpus": 1,
                    "renewable_pct": 50
                })
        return {
            "clusters": clusters,
            "recommendations": [],
            "total_power_mw": sum(c.get("power_draw", 0) for c in clusters),
            "grid_carbon_intensity": 0.45
        }
    else:
        # fallback to mock data if no real metrics yet
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
