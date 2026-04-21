from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from datetime import datetime
import asyncio
import json

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

def generate_realistic_metrics():
    clusters = [
        {
          {
    "id": "h100-cluster-1",
    "name": "NVIDIA H100 Cluster",
    "location": "US-West",
    "gpu_utilization": round(np.random.uniform(85, 98), 1),
    "memory_usage": round(np.random.uniform(12, 15), 2),
    "temperature": round(np.random.uniform(65, 78), 1),
    "power_draw": round(np.random.uniform(1.5, 2.1), 2),
    "efficiency_score": round(np.random.uniform(90, 97), 1)
},  
        },
        {
            "id": "a100-cluster-1",
            "name": "NVIDIA A100 Cluster",
            "location": "US-East",
            "gpu_utilization": round(np.random.uniform(80, 95), 1),
            "memory_usage": round(np.random.uniform(10, 14), 2),
            "temperature": round(np.random.uniform(70, 82), 1),
            "power_draw": round(np.random.uniform(0.8, 1.2), 2),
            "efficiency_score": round(np.random.uniform(85, 93), 1)
        }
    ]
    
    recommendations = [
        {
            "id": "rec-1",
            "cluster_id": "h100-cluster-1",
            "action": "Shift jobs to off-peak hours",
            "estimated_savings_monthly": round(np.random.uniform(15000, 20000), 0),
            "priority": "high"
        },
        {
            "id": "rec-2",
            "cluster_id": "a100-cluster-1",
            "action": "Improve thermal management",
            "estimated_savings_monthly": round(np.random.uniform(7000, 10000), 0),
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
        "service": "ai-gpu-brain-v2",        "timestamp": datetime.now().isoformat()
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = generate_realistic_metrics()
            await websocket.send_json(data)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
# ==========================================
# PHASE 2: API Endpoint for GPU Monitor Agent
# ==========================================

from pydantic import BaseModel
from typing import List, Optional
from fastapi import Header, HTTPException

class GPUMetric(BaseModel):
    gpu_id: int
    utilization_percent: float
    memory_used_gb: float
    memory_total_gb: float
    temperature_celsius: float
    power_draw_watts: float

class ClusterMetrics(BaseModel):
    cluster_id: str
    timestamp: float
    gpus: List[GPUMetric]

# Temporary in-memory storage (replace with DB in production)
metrics_store = {}

@app.post("/api/v1/metrics")
async def receive_metrics(
    metrics: ClusterMetrics,
    authorization: Optional[str] = Header(None)
):
    """Receive GPU metrics from data center agents"""
    
    # Basic API Key validation
    if not authorization or "Bearer" not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized: Missing API key")
    
    # Store metrics
    if metrics.cluster_id not in metrics_store:
        metrics_store[metrics.cluster_id] = []
    
    # Convert to dict for safe storage
    metrics_store[metrics.cluster_id].append(metrics.model_dump())
    
    # Keep only last 500 entries per cluster to prevent memory leaks
    if len(metrics_store[metrics.cluster_id]) > 500:
        metrics_store[metrics.cluster_id] = metrics_store[metrics.cluster_id][-500:]
    
    print(f"✅ Received metrics for cluster: {metrics.cluster_id} ({len(metrics.gpus)} GPUs)")
    
    return {"status": "ok", "received": True}

# ==========================================
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
