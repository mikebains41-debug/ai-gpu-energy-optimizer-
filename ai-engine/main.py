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
    power_draw: float = 250.0

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

# ========== MOCK DATA (fallback) ==========
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
    return {"status": "ok", "service": "ai-gpu-brain-v2"}

@app.get("/")
def root():
    return {"message": "AI GPU Energy Optimizer API", "docs": "/docs", "health": "/health"}

@app.get("/optimize")
def get_optimization():
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
                    "active_gpus": 1,
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
        return generate_realistic_metrics()

@app.post("/optimize")
def post_optimization(input: GPUInput):
    metrics = generate_realistic_metrics()
    recommendations = []
    
    if input.temperature > 75:
        recommendations.append({
            "action": "Reduce GPU frequency by 10-15%",
            "estimated_savings_per_hour": round(input.power_draw * 0.12, 2),
            "priority": "high"
        })
    
    if input.gpu_utilization < 40:
        recommendations.append({
            "action": "Consolidate workloads or enable power capping",
            "estimated_savings_per_hour": round(input.power_draw * 0.25, 2),
            "priority": "medium"
        })
    
    if input.memory_usage > 85:
        recommendations.append({
            "action": "Move data to shared memory or reduce batch size",
            "estimated_savings_per_hour": 0,
            "priority": "low"
        })
    
    metrics["recommendations"] = recommendations
    metrics["input_received"] = input.dict()
    return metrics

@app.post("/recommend-power-cap")
def recommend_power_cap(gpu_id: int, workload_type: str = "inference"):
    if workload_type == "training":
        recommended_power = 400
    else:
        recommended_power = 250
    
    estimated_savings = (450 - recommended_power) * 0.12
    
    return {
        "gpu_id": gpu_id,
        "workload_type": workload_type,
        "recommended_power_cap_watts": recommended_power,
        "estimated_savings_per_hour_usd": round(estimated_savings, 2)
    }

@app.get("/thermal-alerts")
def get_thermal_alerts(threshold_celsius: int = 80):
    alerts = []
    
    for cluster_id, cluster_metrics in metrics_store.items():
        for metric in cluster_metrics[-10:]:
            for gpu in metric.get('gpus', []):
                temp = gpu.get('temperature_celsius', 0)
                if temp > threshold_celsius:
                    alerts.append({
                        "cluster_id": cluster_id,
                        "gpu_id": gpu.get('gpu_id'),
                        "temperature_celsius": temp,
                        "timestamp": metric.get('timestamp'),
                        "action": "Reduce workload or increase cooling immediately",
                        "estimated_risk": "High – potential throttling or shutdown" if temp > 85 else "Medium"
                    })
    
    return {
        "alert_count": len(alerts),
        "threshold_celsius": threshold_celsius,
        "alerts": alerts
    }

# ========== ENHANCED POWER HEADROOM (OC1-OC4 Throttling Levels) ==========
@app.get("/power-headroom")
def power_headroom(gpu_power: float, cpu_power: float):
    total_power = gpu_power + cpu_power
    
    if total_power > 210:
        return {
            "action": "CRITICAL: Reduce GPU frequency immediately",
            "throttle_level": "OC4",
            "urgency": "critical",
            "time_to_throttle_seconds": 0,
            "gpu_reduction_percent": 75,
            "cpu_reduction_percent": 75
        }
    elif total_power > 168:
        return {
            "action": "Schedule urgent workload reduction",
            "throttle_level": "OC2",
            "urgency": "high",
            "time_to_throttle_seconds": 30,
            "gpu_reduction_percent": 50,
            "cpu_reduction_percent": 50
        }
    elif total_power > 144:
        return {
            "action": "Reduce GPU frequency by 15%",
            "throttle_level": "OC1",
            "urgency": "medium",
            "time_to_throttle_seconds": 60,
            "gpu_reduction_percent": 25,
            "cpu_reduction_percent": 0
        }
    else:
        return {
            "action": "Normal operation",
            "throttle_level": "None",
            "urgency": "none",
            "gpu_reduction_percent": 0,
            "cpu_reduction_percent": 0
        }

# ========== CPU POWER READING ==========
@app.get("/cpu-power")
def cpu_power():
    import glob
    try:
        power_files = glob.glob("/sys/bus/i2c/devices/*/hwmon/hwmon*/power")
        if power_files:
            with open(power_files[0], 'r') as f:
                power_mw = int(f.read().strip())
                return {"cpu_power_watts": power_mw / 1000, "source": "real"}
    except:
        pass
    return {"cpu_power_watts": 45.0, "source": "mock", "note": "Replace with actual IGX power reading"}

# ========== SYSTEM POWER (GPU + CPU + I/O) ==========
@app.get("/system-power")
def system_power(gpu_power: float = None):
    cpu_result = cpu_power()
    cpu_watts = cpu_result.get("cpu_power_watts", 45.0)
    gpu_watts = gpu_power if gpu_power is not None else 150.0
    io_watts = 10.0
    total_watts = gpu_watts + cpu_watts + io_watts
    
    return {
        "gpu_power_watts": gpu_watts,
        "cpu_power_watts": cpu_watts,
        "io_power_watts": io_watts,
        "total_power_watts": round(total_watts, 1),
        "thermal_risk": "high" if total_watts > 168 else "medium" if total_watts > 144 else "low"
    }

# ========== GPU POWER MODE (Max-Q / Max-P) ==========
@app.get("/gpu-power-mode")
def gpu_power_mode(gpu_id: int = 0):
    import subprocess
    try:
        result = subprocess.run(
            ["nvidia-smi", "-q", "-d", "PERFORMANCE"],
            capture_output=True, text=True, timeout=5
        )
        if "Max-Q" in result.stdout:
            return {"gpu_id": gpu_id, "power_mode": "Max-Q", "description": "Power efficient", "recommended_workload": "inference"}
        elif "Max-P" in result.stdout:
            return {"gpu_id": gpu_id, "power_mode": "Max-P", "description": "Maximum performance", "recommended_workload": "training"}
        else:
            return {"gpu_id": gpu_id, "power_mode": "Unknown"}
    except:
        return {"gpu_id": gpu_id, "power_mode": "Max-P (mock)", "description": "Testing mode - no GPU detected", "recommended_workload": "training"}

# ========== MISSION CONTROL INTEGRATION ==========
@app.post("/mission-control/power-optimize")
def mission_control_optimize(robot_id: str, mission_type: str = "transport"):
    if mission_type == "transport":
        return {
            "robot_id": robot_id,
            "mission_type": mission_type,
            "recommended_power_cap_watts": 150,
            "duration_minutes": 30,
            "expected_energy_savings_percent": 35
        }
    elif mission_type == "charging":
        return {
            "robot_id": robot_id,
            "mission_type": mission_type,
            "recommended_power_cap_watts": 50,
            "duration_minutes": "idle",
            "expected_energy_savings_percent": 70
        }
    else:
        return {
            "robot_id": robot_id,
            "mission_type": mission_type,
            "recommended_power_cap_watts": 250,
            "duration_minutes": "unknown",
            "expected_energy_savings_percent": 15
        }

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
