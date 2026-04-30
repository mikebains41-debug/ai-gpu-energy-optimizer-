# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.
# Contact: Mikebains41@gmail.com
# Unauthorized use prohibited.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import numpy as np
import random
from datetime import datetime
import asyncio
import json
import os
import subprocess
import glob
from typing import List, Optional, Dict

# Fix: Import from ai-engine/engines/ (correct path)
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.engine1_efficiency import calculate_true_efficiency
from engines.engine2_idle import calculate_idle_waste
from engines.engine3_burst import detect_compute_bursts
from engines.engine4_sampling import estimate_sampling_gap
from engines.engine5_alerts import evaluate_alerts
from engines.engine6_export import export_dataset
from engines.engine7_powerstate import detect_power_state
from engines.engine8_delta import calculate_efficiency_delta

# ========== PERSISTENT STORAGE ==========
DATA_DIR = "/opt/render/project/src/persistent_data"
METRICS_FILE = os.path.join(DATA_DIR, "metrics.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_metrics():
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading metrics: {e}")
            return {}
    return {}

def save_metrics(metrics):
    try:
        with open(METRICS_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)
    except Exception as e:
        print(f"Error saving metrics: {e}")

# ========== APP INITIALIZATION ==========
app = FastAPI(title="AI GPU Energy Optimizer", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_store = load_metrics()
VALID_API_KEYS = os.environ.get("VALID_API_KEYS", "test_key_123,gpu_opt_demo").split(",")

def validate_api_key(api_key: str) -> bool:
    return api_key in VALID_API_KEYS

# ========== WEBSOCKET MANAGER ==========
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

# ========== HELPER FUNCTION ==========
def get_metrics_list() -> List[Dict]:
    """Convert metrics_store dict to list for engine functions"""
    result = []
    for cluster_id, measurements in metrics_store.items():
        for m in measurements:
            m_copy = m.copy()
            m_copy['cluster_id'] = cluster_id
            result.append(m_copy)
    return result

# ========== ENDPOINTS ==========
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-gpu-brain-v3", "engines": 8}

@app.get("/")
def root():
    return {"message": "AI GPU Energy Optimizer API", "docs": "/docs", "health": "/health", "engines": 8}

@app.get("/metrics")
def get_metrics():
    return metrics_store

@app.get("/metrics/a100")
def get_a100_metrics():
    return {k: v for k, v in metrics_store.items() if "a100" in k.lower()}

@app.get("/metrics/h100")
def get_h100_metrics():
    return {k: v for k, v in metrics_store.items() if "h100" in k.lower()}

@app.post("/api/v1/metrics")
async def receive_metrics(metrics: dict, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization")
    api_key = authorization.replace("Bearer ", "")
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    cluster_id = metrics.get("cluster_id", "unknown")
    if cluster_id not in metrics_store:
        metrics_store[cluster_id] = []
    metrics_store[cluster_id].append(metrics)
    
    if len(metrics_store[cluster_id]) > 500:
        metrics_store[cluster_id] = metrics_store[cluster_id][-500:]
    
    save_metrics(metrics_store)
    return {"status": "ok", "received": True}

# ========== ENGINE 1-8 ENDPOINTS ==========
@app.get("/engine/efficiency")
def get_efficiency():
    return calculate_true_efficiency(get_metrics_list())

@app.get("/engine/idle")
def get_idle():
    return calculate_idle_waste(get_metrics_list())

@app.get("/engine/burst")
def get_burst():
    return detect_compute_bursts(get_metrics_list())

@app.get("/engine/sampling")
def get_sampling():
    return estimate_sampling_gap(get_metrics_list())

@app.get("/engine/alerts")
def get_alerts():
    return evaluate_alerts(get_metrics_list())

@app.get("/engine/export")
def get_export(format: str = "json"):
    return export_dataset(get_metrics_list(), format)

@app.get("/engine/powerstate")
def get_powerstate():
    return detect_power_state(get_metrics_list())

@app.get("/engine/delta")
def get_delta(baseline_sec: int = 60, after_sec: int = 60):
    return calculate_efficiency_delta(get_metrics_list(), baseline_sec, after_sec)

# ========== WEBSOCKET ==========
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
