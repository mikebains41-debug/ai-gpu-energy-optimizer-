# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Manmohan Bains. All Rights Reserved.
# Contact: mikebains41@gmail.com
# Unauthorized use prohibited.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Header, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from datetime import datetime
import asyncio
import json
import os
import time
from typing import List, Dict, Optional

app = FastAPI(title="AI GPU Energy Optimizer", version="3.0.0")

# ========== SORT HELPER ==========
def sort_by_test_number(folders):
    import re
    def key(f):
        m = re.search(r'test-(\d+)', f)
        return int(m.group(1)) if m else 999
    return sorted(folders, key=key)

# ========== HELPER FOR FLEXIBLE TEST ID ==========
def find_test_result(base_dir: str, test_id: str):
    if not os.path.isdir(base_dir):
        return None
    tid = test_id.lower()
    folders = os.listdir(base_dir)
    # exact match
    for f in folders:
        if f.lower() == tid:
            cand = os.path.join(base_dir, f, "summary.json")
            if os.path.exists(cand):
                return cand
    # prefix match
    for f in folders:
        if f.lower().startswith(tid):
            cand = os.path.join(base_dir, f, "summary.json")
            if os.path.exists(cand):
                return cand
    # numeric short id (e.g., "11")
    if test_id.isdigit():
        padded = f"test-{int(test_id):02d}"
        for f in folders:
            if f.lower().startswith(padded):
                cand = os.path.join(base_dir, f, "summary.json")
                if os.path.exists(cand):
                    return cand
    # handle "test-9"
    if tid.startswith("test-") and tid[5:].isdigit():
        num = int(tid[5:])
        padded = f"test-{num:02d}"
        for f in folders:
            if f.lower().startswith(padded):
                cand = os.path.join(base_dir, f, "summary.json")
                if os.path.exists(cand):
                    return cand
    return None

# ========== ENGINE 1: TRUE EFFICIENCY ==========
def calculate_true_efficiency(metrics_history: List[Dict]) -> Dict:
    if len(metrics_history) < 2:
        return {"error": "Insufficient data", "samples": len(metrics_history)}
    util_series, power_series, timestamps = [], [], []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            util_series.append(gpu.get('utilization_percent', 0))
            power_series.append(gpu.get('power_draw_watts', 0))
            timestamps.append(m.get('timestamp', 0))
    if len(util_series) < 2:
        return {"error": "No valid GPU data"}
    total_time = timestamps[-1] - timestamps[0] if timestamps[-1] > timestamps[0] else len(util_series)
    useful_compute_time = sum(1 for u in util_series if u > 5)
    avg_util = np.mean(util_series) / 100.0
    avg_power = max(np.mean(power_series), 1.0)
    util_variance = np.var(util_series)
    normalized_variance = min(util_variance / 100.0, 1.0)
    consistency = 1.0 - normalized_variance
    efficiency = (useful_compute_time / total_time) * (avg_util / avg_power) * consistency
    efficiency = max(0.0, min(1.0, efficiency))
    return {
        "efficiency_score": round(efficiency, 4),
        "efficiency_percentage": round(efficiency * 100, 2),
        "useful_compute_ratio": round(useful_compute_time / total_time, 4),
        "consistency": round(consistency, 4),
        "samples_analyzed": len(util_series)
    }

# ========== ENGINE 2: IDLE DETECTION ==========
def calculate_idle_waste(metrics_history: List[Dict], cost_per_hour: float = 3.50) -> Dict:
    if len(metrics_history) < 10:
        return {"error": "Insufficient data", "samples": len(metrics_history)}
    util_series, power_series = [], []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            util_series.append(gpu.get('utilization_percent', 0))
            power_series.append(gpu.get('power_draw_watts', 0))
    idle_periods, current_start = [], None
    for i, u in enumerate(util_series):
        if u < 5 and current_start is None:
            current_start = i
        elif u >= 5 and current_start is not None:
            duration = i - current_start
            if duration >= 2:
                idle_periods.append(duration)
            current_start = None
    total_idle = sum(idle_periods)
    total_time = len(util_series)
    idle_pct = (total_idle / total_time) * 100
    cost_waste = total_idle * (cost_per_hour / 3600)
    false_idle = sum(1 for u, p in zip(util_series, power_series) if u < 5 and p > 120)
    if idle_pct > 30:
        rec = f"GPU idle {idle_pct:.1f}% → reduce instances"
    elif idle_pct > 15:
        rec = f"GPU idle {idle_pct:.1f}% → consolidate workloads"
    else:
        rec = "Idle within acceptable range"
    return {
        "idle_percentage": round(idle_pct, 2),
        "total_idle_seconds": total_idle,
        "idle_periods": len(idle_periods),
        "cost_waste_usd": round(cost_waste, 4),
        "false_idle_detections": false_idle,
        "recommendation": rec
    }

# ========== ENGINE 3: BURST DETECTION ==========
def detect_compute_bursts(metrics_history: List[Dict]) -> Dict:
    if len(metrics_history) < 10:
        return {"error": "Insufficient data", "burst_count": 0}
    power_series, util_series = [], []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            power_series.append(gpu.get('power_draw_watts', 0))
            util_series.append(gpu.get('utilization_percent', 0))
    bursts, confidence = [], {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for i in range(1, len(power_series)):
        power_delta = power_series[i] - power_series[i-1]
        util_delta = abs(util_series[i] - util_series[i-1])
        if power_delta > 50 and util_delta < 5:
            if power_delta > 100:
                conf = "HIGH"
            elif power_delta > 50:
                conf = "MEDIUM"
            else:
                conf = "LOW"
            confidence[conf] += 1
    minutes = len(metrics_history) / 60
    bursts_per_min = len(bursts) / minutes if minutes > 0 else 0
    return {
        "burst_count": len(bursts),
        "bursts_per_minute": round(bursts_per_min, 2),
        "peak_power_watts": round(max(power_series), 1) if power_series else 0,
        "confidence": confidence
    }

# ========== ENGINE 4: SAMPLING GAP ==========
def estimate_sampling_gap(metrics_history: List[Dict]) -> Dict:
    burst = detect_compute_bursts(metrics_history)
    burst_count = burst.get("burst_count", 0)
    missed_sec = burst_count * 0.05
    total_time = len(metrics_history)
    gap_pct = (missed_sec / total_time) * 100 if total_time > 0 else 0
    if gap_pct > 5:
        severity, msg = "HIGH", f"Monitoring misses ~{gap_pct:.1f}% of compute activity"
    elif gap_pct > 1:
        severity, msg = "MEDIUM", f"Monitoring misses ~{gap_pct:.1f}% of compute activity"
    else:
        severity, msg = "LOW", f"Sampling gap is {gap_pct:.2f}% - acceptable"
    return {
        "sampling_gap_percent": round(gap_pct, 2),
        "severity": severity,
        "message": msg,
        "estimated_missed_seconds": round(missed_sec, 3),
        "burst_count": burst_count
    }

# ========== ENGINE 5: ALERTS ==========
_last_alert = {}
def evaluate_alerts(metrics_history: List[Dict], cooldown: int = 300) -> Dict:
    if not metrics_history:
        return {"alerts": []}
    latest = metrics_history[-1]
    if not latest.get('gpus') or len(latest['gpus']) == 0:
        return {"alerts": []}
    gpu = latest['gpus'][0]
    temp = gpu.get('temperature_celsius', 0)
    util = gpu.get('utilization_percent', 0)
    cluster = latest.get('cluster_id', 'unknown')
    alerts, now = [], time.time()
    if temp > 85:
        key = f"{cluster}_temp_crit"
        if key not in _last_alert or (now - _last_alert[key]) > cooldown:
            alerts.append({"type": "TEMPERATURE", "severity": "CRITICAL", "value": temp, "message": f"GPU at {temp}°C - immediate action"})
            _last_alert[key] = now
    elif temp > 75:
        key = f"{cluster}_temp_warn"
        if key not in _last_alert or (now - _last_alert[key]) > cooldown:
            alerts.append({"type": "TEMPERATURE", "severity": "WARNING", "value": temp, "message": f"GPU at {temp}°C - reduce workload"})
            _last_alert[key] = now
    if util < 10:
        key = f"{cluster}_idle"
        if key not in _last_alert or (now - _last_alert[key]) > cooldown:
            alerts.append({"type": "IDLE", "severity": "INFO", "value": util, "message": f"GPU at {util}% utilization - potential waste"})
            _last_alert[key] = now
    return {"alert_count": len(alerts), "alerts": alerts}

# ========== ENGINE 6: EXPORT ==========
def export_dataset(metrics_history: List[Dict], format: str = "json") -> Dict:
    if not metrics_history:
        return {"error": "No data to export"}
    metadata = {
        "export_date": datetime.now().isoformat(),
        "samples": len(metrics_history),
        "sampling_rate_hz": 1,
        "gpu_type": "A100/H100"
    }
    if format == "json":
        return {"metadata": metadata, "data": metrics_history}
    rows = []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            rows.append({
                "timestamp": m.get('timestamp'),
                "utilization": gpu.get('utilization_percent'),
                "power_w": gpu.get('power_draw_watts'),
                "temperature": gpu.get('temperature_celsius')
            })
    return {"format": "csv", "rows": rows, "metadata": metadata, "row_count": len(rows)}

# ========== ENGINE 7: POWER STATE ==========
def detect_power_state(metrics_history: List[Dict]) -> Dict:
    if len(metrics_history) < 10:
        return {"error": "Insufficient data"}
    low_util_high_power = 0
    for m in metrics_history[-60:]:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            if gpu.get('utilization_percent', 0) < 1 and gpu.get('power_draw_watts', 0) > 80:
                low_util_high_power += 1
    if low_util_high_power > 30:
        return {"power_state": "HIGH_RESIDENCY_STATE", "severity": "INFO", "message": "GPU in high-power residency state (normal datacenter behavior)", "samples": low_util_high_power}
    elif low_util_high_power > 10:
        return {"power_state": "INTERMITTENT_HIGH_POWER", "severity": "LOW", "message": "GPU shows intermittent high power at low utilization", "samples": low_util_high_power}
    else:
        return {"power_state": "NORMAL", "severity": "OK", "message": "GPU power state normal", "samples": low_util_high_power}

# ========== ENGINE 8: DELTA TRACKER ==========
def calculate_efficiency_delta(metrics_history: List[Dict], baseline_sec: int = 60, after_sec: int = 60) -> Dict:
    if len(metrics_history) < baseline_sec + after_sec:
        return {"error": f"Insufficient data. Need {baseline_sec + after_sec} samples, have {len(metrics_history)}"}
    baseline, after = metrics_history[:baseline_sec], metrics_history[-after_sec:]
    def avg_util(data): utils = [m['gpus'][0].get('utilization_percent', 0) for m in data if m.get('gpus')]; return sum(utils)/len(utils) if utils else 0
    def avg_power(data): powers = [m['gpus'][0].get('power_draw_watts', 0) for m in data if m.get('gpus')]; return sum(powers)/len(powers) if powers else 0
    base_util, after_util = avg_util(baseline), avg_util(after)
    base_power, after_power = avg_power(baseline), avg_power(after)
    base_eff = base_util / base_power if base_power > 0 else 0
    after_eff = after_util / after_power if after_power > 0 else 0
    delta = after_eff - base_eff
    gain = (delta / base_eff) * 100 if base_eff > 0 else 0
    if delta > 0: conclusion = "Workload scaling improved efficiency"
    elif delta < 0: conclusion = "Workload scaling is inefficient - wasting power"
    else: conclusion = "No change in efficiency"
    return {
        "efficiency_delta": round(delta, 4),
        "efficiency_gain_percent": round(gain, 2),
        "baseline_efficiency": round(base_eff, 4),
        "after_efficiency": round(after_eff, 4),
        "baseline_util_pct": round(base_util, 1),
        "after_util_pct": round(after_util, 1),
        "conclusion": conclusion
    }

# ========== PERSISTENT STORAGE ==========
DATA_DIR = "/opt/render/project/src/persistent_data"
METRICS_FILE = os.path.join(DATA_DIR, "metrics.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_metrics():
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_metrics(metrics):
    try:
        with open(METRICS_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)
    except Exception:
        pass

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

def get_metrics_list() -> List[Dict]:
    result = []
    for cluster_id, measurements in metrics_store.items():
        for m in measurements:
            m_copy = m.copy()
            m_copy['cluster_id'] = cluster_id
            result.append(m_copy)
    return result

# ========== CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== TEST RESULTS ENDPOINTS ==========
@app.get("/results/a100")
def get_a100_results():
    base = os.path.join(get_data_dir(), "tests", "a100")
    out = []
    if os.path.isdir(base):
        for f in sort_by_test_number(os.listdir(base)):
            p = os.path.join(base, f, "summary.json")
            if os.path.exists(p):
                with open(p) as fp:
                    out.append(json.load(fp))
    return out

@app.get("/results/h100")
def get_h100_results():
    base = os.path.join(get_data_dir(), "tests", "h100")
    out = []
    if os.path.isdir(base):
        for f in sort_by_test_number(os.listdir(base)):
            p = os.path.join(base, f, "summary.json")
            if os.path.exists(p):
                with open(p) as fp:
                    out.append(json.load(fp))
    return out

@app.get("/results/a100/count")
def count_a100():
    base = os.path.join(get_data_dir(), "tests", "a100")
    c = 0
    if os.path.isdir(base):
        for f in os.listdir(base):
            if os.path.isdir(os.path.join(base, f)):
                c += 1
    return {"total_a100_tests": c}

@app.get("/results/h100/count")
def count_h100():
    base = os.path.join(get_data_dir(), "tests", "h100")
    c = 0
    if os.path.isdir(base):
        for f in os.listdir(base):
            if os.path.isdir(os.path.join(base, f)):
                c += 1
    return {"total_h100_tests": c}

@app.get("/results/a100/{test_id}")
def get_a100_test_result(test_id: str):
    base = os.path.join(get_data_dir(), "tests", "a100")
    path = find_test_result(base, test_id)
    if not path:
        raise HTTPException(status_code=404, detail=f"Test '{test_id}' not found")
    with open(path) as f:
        return json.load(f)

@app.get("/results/h100/{test_id}")
def get_h100_test_result(test_id: str):
    base = os.path.join(get_data_dir(), "tests", "h100")
    path = find_test_result(base, test_id)
    if not path:
        raise HTTPException(status_code=404, detail=f"Test '{test_id}' not found")
    with open(path) as f:
        return json.load(f)

# ========== DASHBOARD SUMMARY ENDPOINT ==========
@app.get("/api/summary")
def get_dashboard_summary():
    possible_paths = [
        "/opt/render/project/src/data/dashboard-summary.json",
        "data/dashboard-summary.json",
        "../data/dashboard-summary.json",
        "/opt/render/project/src/dashboard-summary.json"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    return {"error": "Summary file not found", "paths_checked": possible_paths}

# ========== CORE ENDPOINTS ==========
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-gpu-brain-v3", "engines": 8}

@app.get("/")
def root():
    return {
        "message": "AI GPU Energy Optimizer API",
        "docs": "/docs",
        "health": "/health",
        "engines": 8,
        "contact": "mikebains41@gmail.com"
    }

@app.get("/metrics")
def get_metrics():
    if metrics_store:
        return metrics_store
    return {"status": "no_live_agent", "a100_tests": 24, "h100_tests": 11, "note": "No live agent connected. Use /results/a100 or /results/h100 for recorded data."}

@app.get("/metrics/a100")
def get_a100_metrics():
    live = {k: v for k, v in metrics_store.items() if "a100" in k.lower()}
    if live:
        return live
    return {"status": "no_live_agent", "recorded_tests": 24, "data": "/results/a100", "note": "Live telemetry requires a running monitoring agent. Recorded test data available at /results/a100"}

@app.get("/metrics/h100")
def get_h100_metrics():
    live = {k: v for k, v in metrics_store.items() if "h100" in k.lower()}
    if live:
        return live
    return {"status": "no_live_agent", "recorded_tests": 11, "data": "/results/h100", "note": "Live telemetry requires a running monitoring agent. Recorded test data available at /results/h100"}

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

# ========== DEBUG ==========
@app.get("/debug/list_tests")
def list_tests():
    base = os.path.join(get_data_dir(), "tests", "a100")
    if not os.path.exists(base):
        return {"error": f"Path {base} does not exist"}
    folders = sorted([d for d in os.listdir(base) if d.startswith("test-")])
    return {"base_path": base, "folders": folders}

# ========== NEW IMPORTS ==========
from fastapi.responses import PlainTextResponse, StreamingResponse
import csv

def get_data_dir():
    """Return absolute path to ai-engine/data directory."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "ai-engine", "data")


# ========== CSV LOADER ==========
def load_csv_for_plot(gpu: str, test_id: str):
    base = f"get_data_dir()/tests/{gpu}"
    path = find_test_result(base, test_id)
    if not path:
        return None, None
    folder_path = os.path.dirname(path)
    csv_path = os.path.join(folder_path, "data.csv")
    if not os.path.exists(csv_path):
        return {}, folder_path
    timestamps, power, utilization, temperature = [], [], [], []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            timestamps.append(i)
            pw = row.get("power_draw_watts") or row.get("power_w") or row.get("power") or row.get("power.draw [W]") or row.get(" power.draw [W]") or "0"
            ut = row.get("utilization_percent") or row.get("utilization") or row.get("util") or row.get("utilization.gpu [%]") or row.get(" utilization.gpu [%]") or "0"
            te = row.get("temperature_celsius") or row.get("temperature_c") or row.get("temp") or "0"
            try:
                power.append(float(pw))
                utilization.append(float(ut))
                temperature.append(float(te))
            except:
                power.append(0); utilization.append(0); temperature.append(0)
    return {"timestamps": timestamps, "power": power, "utilization": utilization, "temperature": temperature}, folder_path

# ========== PROMETHEUS ==========
def generate_prometheus_metrics():
    out = []
    out.append('# HELP gpu_idle_power_floor_watts Idle power floor in watts')
    out.append('# TYPE gpu_idle_power_floor_watts gauge')
    out.append('gpu_idle_power_floor_watts{gpu="a100_sxm"} 67.1')
    out.append('gpu_idle_power_floor_watts{gpu="h100_sxm"} 69.5')
    out.append('# HELP gpu_fp32_peak_tflops Peak FP32 TFLOPS')
    out.append('# TYPE gpu_fp32_peak_tflops gauge')
    out.append('gpu_fp32_peak_tflops{gpu="a100_sxm"} 15.3')
    out.append('gpu_fp32_peak_tflops{gpu="h100_sxm"} 49.13')
    out.append('# HELP gpu_fp16_peak_tflops Peak FP16 TFLOPS')
    out.append('# TYPE gpu_fp16_peak_tflops gauge')
    out.append('gpu_fp16_peak_tflops{gpu="a100_sxm"} 231.08')
    out.append('gpu_fp16_peak_tflops{gpu="h100_sxm"} 592.8')
    out.append('# HELP gpu_efficiency_gflops_per_watt Compute efficiency GFLOPS/W')
    out.append('# TYPE gpu_efficiency_gflops_per_watt gauge')
    out.append('gpu_efficiency_gflops_per_watt{gpu="a100_sxm"} 52.6')
    out.append('gpu_efficiency_gflops_per_watt{gpu="h100_sxm"} 76.5')
    out.append('# HELP gpu_cei_flops_per_joule Compute Energy Intensity')
    out.append('# TYPE gpu_cei_flops_per_joule gauge')
    out.append('gpu_cei_flops_per_joule{gpu="a100_sxm"} 5680000000')
    out.append('# HELP gpu_ghost_power_events_total Ghost power events detected')
    out.append('# TYPE gpu_ghost_power_events_total counter')
    out.append('gpu_ghost_power_events_total{gpu="a100_sxm"} 1')
    out.append('gpu_ghost_power_events_total{gpu="h100_sxm"} 0')
    out.append('# HELP gpu_tests_completed Validation tests completed')
    out.append('# TYPE gpu_tests_completed gauge')
    out.append('gpu_tests_completed{gpu="a100_sxm"} 24')
    out.append('gpu_tests_completed{gpu="h100_sxm"} 11')
    out.append('# HELP gpu_test_mean_power_watts Mean power per recorded test')
    out.append('# TYPE gpu_test_mean_power_watts gauge')
    for g in ["a100", "h100"]:
        base = f"get_data_dir()/tests/{g}"
        if not os.path.isdir(base):
            continue
        for folder in sort_by_test_number(os.listdir(base)):
            spath = os.path.join(base, folder, "summary.json")
            if not os.path.exists(spath):
                continue
            try:
                with open(spath) as f:
                    s = json.load(f)
                tid = s.get("test_id", folder).replace("-", "_")
                if "mean_power_w" in s:
                    out.append(f'gpu_test_mean_power_watts{{gpu="{g}",test="{tid}"}} {s["mean_power_w"]}')
                if "mean_tflops" in s:
                    out.append(f'gpu_test_tflops{{gpu="{g}",test="{tid}"}} {s["mean_tflops"]}')
                if "ghost_power_detected" in s:
                    val = 1 if s["ghost_power_detected"] else 0
                    out.append(f'gpu_ghost_power_detected{{gpu="{g}",test="{tid}"}} {val}')
                if "ghost_power_w" in s:
                    out.append(f'gpu_ghost_power_watts{{gpu="{g}",test="{tid}"}} {s["ghost_power_w"]}')
            except:
                continue
    for cluster_id, measurements in metrics_store.items():
        if measurements:
            latest = measurements[-1]
            if latest.get("gpus"):
                gd = latest["gpus"][0]
                lbl = cluster_id.replace("-", "_")
                if "power_draw_watts" in gd:
                    out.append(f'gpu_live_power_watts{{cluster="{lbl}"}} {gd["power_draw_watts"]}')
                if "utilization_percent" in gd:
                    out.append(f'gpu_live_utilization_percent{{cluster="{lbl}"}} {gd["utilization_percent"]}')
                if "temperature_celsius" in gd:
                    out.append(f'gpu_live_temperature_celsius{{cluster="{lbl}"}} {gd["temperature_celsius"]}')
    return "# GPU Energy Observability Platform\n" + "\n".join(out) + "\n"

@app.get("/metrics/prometheus", response_class=PlainTextResponse)
def prometheus_metrics():
    return PlainTextResponse(generate_prometheus_metrics(), media_type="text/plain; version=0.0.4")

# ========== PLOT ENDPOINTS ==========
@app.get("/plots/{gpu}/{test_id}")
def get_plot(gpu: str, test_id: str):
    if gpu not in ["a100", "h100"]:
        raise HTTPException(status_code=400, detail="gpu must be a100 or h100")
    data, _ = load_csv_for_plot(gpu, test_id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Test {test_id} not found for {gpu}")
    if not data.get("timestamps"):
        raise HTTPException(status_code=404, detail=f"No data.csv for {gpu}/{test_id}")
    return {
        "data": [
            {"x": data["timestamps"], "y": data["power"], "name": "Power (W)", "type": "scatter", "mode": "lines", "line": {"color": "#ff6b35", "width": 2}, "yaxis": "y"},
            {"x": data["timestamps"], "y": data["utilization"], "name": "Utilization (%)", "type": "scatter", "mode": "lines", "line": {"color": "#4ecdc4", "width": 2}, "yaxis": "y2"},
            {"x": data["timestamps"], "y": data["temperature"], "name": "Temperature (C)", "type": "scatter", "mode": "lines", "line": {"color": "#ffe66d", "width": 1, "dash": "dot"}, "yaxis": "y2"}
        ],
        "layout": {
            "title": f"{gpu.upper()} {test_id} — Power / Utilization / Temperature",
            "xaxis": {"title": "Sample (seconds)"},
            "yaxis": {"title": "Power (W)", "side": "left"},
            "yaxis2": {"title": "Utilization / Temp", "side": "right", "overlaying": "y"},
            "plot_bgcolor": "#1a1a2e", "paper_bgcolor": "#16213e", "font": {"color": "#eee"}
        }
    }

@app.get("/plots/{gpu}/{test_id}/divergence")
def get_divergence_plot(gpu: str, test_id: str):
    if gpu not in ["a100", "h100"]:
        raise HTTPException(status_code=400, detail="gpu must be a100 or h100")
    data, _ = load_csv_for_plot(gpu, test_id)
    if data is None or not data.get("timestamps"):
        raise HTTPException(status_code=404, detail=f"No data found for {gpu}/{test_id}")
    ghost_x, ghost_y = [], []
    for i, (p, u) in enumerate(zip(data["power"], data["utilization"])):
        if u == 0 and p > 80:
            ghost_x.append(i)
            ghost_y.append(p)
    return {
        "data": [
            {"x": data["timestamps"], "y": data["power"], "name": "Board Power (W)", "type": "scatter", "mode": "lines", "line": {"color": "#ff6b35", "width": 2}, "yaxis": "y"},
            {"x": data["timestamps"], "y": data["utilization"], "name": "Reported Utilization (%)", "type": "scatter", "mode": "lines", "line": {"color": "#4ecdc4", "width": 2}, "yaxis": "y2"},
            {"x": ghost_x, "y": ghost_y, "name": "Ghost Power Window", "type": "scatter", "mode": "markers", "marker": {"color": "#ff0055", "size": 7, "symbol": "circle"}, "yaxis": "y"}
        ],
        "layout": {
            "title": f"{gpu.upper()} {test_id} — Telemetry Divergence (Ghost Power)",
            "annotations": [{"text": "Red = power drawn at 0% reported utilization", "showarrow": False, "x": 0.5, "y": 1.07, "xref": "paper", "yref": "paper", "font": {"color": "#ff0055", "size": 12}}],
            "xaxis": {"title": "Sample (seconds)"},
            "yaxis": {"title": "Power (W)", "side": "left"},
            "yaxis2": {"title": "Utilization (%)", "side": "right", "overlaying": "y", "range": [0, 110]},
            "plot_bgcolor": "#1a1a2e", "paper_bgcolor": "#16213e", "font": {"color": "#eee"}
        },
        "ghost_power_samples": len(ghost_x),
        "ghost_power_detected": len(ghost_x) > 0
    }

# ========== REPLAY MODE (SSE) ==========
@app.get("/replay/{gpu}/{test_id}")
def replay_info(gpu: str, test_id: str):
    data, _ = load_csv_for_plot(gpu, test_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return {
        "gpu": gpu, "test_id": test_id,
        "total_samples": len(data.get("timestamps", [])),
        "stream_url": f"/replay/{gpu}/{test_id}/stream",
        "note": "Connect via EventSource. Add ?speed=2.0 for 2x playback."
    }

@app.get("/replay/{gpu}/{test_id}/stream")
async def replay_stream(gpu: str, test_id: str, speed: float = 1.0):
    if gpu not in ["a100", "h100"]:
        raise HTTPException(status_code=400, detail="gpu must be a100 or h100")
    data, _ = load_csv_for_plot(gpu, test_id)
    if data is None or not data.get("timestamps"):
        raise HTTPException(status_code=404, detail=f"No data for {gpu}/{test_id}")
    async def stream():
        n = len(data["timestamps"])
        delay = max(0.05, 1.0 / max(0.1, speed))
        yield f"data: {json.dumps({'type': 'start', 'gpu': gpu, 'test_id': test_id, 'total_samples': n})}\n\n"
        for i in range(n):
            row = {
                "type": "telemetry", "sample": i, "total": n,
                "power_w": data["power"][i],
                "utilization_pct": data["utilization"][i],
                "temperature_c": data["temperature"][i],
                "ghost_power": data["utilization"][i] == 0 and data["power"][i] > 80,
                "progress_pct": round((i / n) * 100, 1)
            }
            yield f"data: {json.dumps(row)}\n\n"
            await asyncio.sleep(delay)
        yield f"data: {json.dumps({'type': 'end', 'samples_sent': n})}\n\n"
    return StreamingResponse(stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# ========== GRAFANA DASHBOARD ==========
GRAFANA_DASHBOARD = {
    "title": "GPU Energy Observability Platform",
    "uid": "gpu-energy-obs",
    "schemaVersion": 38,
    "version": 1,
    "refresh": "10s",
    "panels": [
        {"id": 1, "title": "Live Power (W)", "type": "timeseries", "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
         "targets": [{"expr": "gpu_live_power_watts", "legendFormat": "{{cluster}}"}],
         "fieldConfig": {"defaults": {"unit": "watt", "color": {"fixedColor": "#ff6b35", "mode": "fixed"}}}},
        {"id": 2, "title": "Live Utilization (%)", "type": "timeseries", "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
         "targets": [{"expr": "gpu_live_utilization_percent", "legendFormat": "{{cluster}}"}],
         "fieldConfig": {"defaults": {"unit": "percent", "max": 100, "color": {"fixedColor": "#4ecdc4", "mode": "fixed"}}}},
        {"id": 3, "title": "Ghost Power Events", "type": "stat", "gridPos": {"x": 0, "y": 8, "w": 6, "h": 4},
         "targets": [{"expr": "gpu_ghost_power_events_total", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"thresholds": {"steps": [{"color": "green", "value": 0}, {"color": "red", "value": 1}]}}}},
        {"id": 4, "title": "Idle Power Floor (W)", "type": "stat", "gridPos": {"x": 6, "y": 8, "w": 6, "h": 4},
         "targets": [{"expr": "gpu_idle_power_floor_watts", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "watt"}}},
        {"id": 5, "title": "Peak FP32 TFLOPS", "type": "stat", "gridPos": {"x": 12, "y": 8, "w": 6, "h": 4},
         "targets": [{"expr": "gpu_fp32_peak_tflops", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "short"}}},
        {"id": 6, "title": "Efficiency (GFLOPS/W)", "type": "stat", "gridPos": {"x": 18, "y": 8, "w": 6, "h": 4},
         "targets": [{"expr": "gpu_efficiency_gflops_per_watt", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "short"}}},
        {"id": 7, "title": "Live Temperature (C)", "type": "timeseries", "gridPos": {"x": 0, "y": 12, "w": 24, "h": 8},
         "targets": [{"expr": "gpu_live_temperature_celsius", "legendFormat": "{{cluster}}"}],
         "fieldConfig": {"defaults": {"unit": "celsius", "color": {"fixedColor": "#ffe66d", "mode": "fixed"},
             "thresholds": {"steps": [{"color": "green", "value": 0}, {"color": "yellow", "value": 70}, {"color": "red", "value": 85}]}}}}
    ]
}

@app.get("/grafana/dashboard")
def get_grafana_dashboard():
    return {"dashboard": GRAFANA_DASHBOARD, "overwrite": True, "folderId": 0}

@app.get("/grafana/dashboard/download", response_class=PlainTextResponse)
def download_grafana_dashboard():
    content = json.dumps({"dashboard": GRAFANA_DASHBOARD, "overwrite": True, "folderId": 0}, indent=2)
    return PlainTextResponse(content, media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=gpu-energy-dashboard.json"})

# ========== SLURM JOB HOOKS ==========
JOB_LOG_FILE = os.path.join(DATA_DIR, "slurm_jobs.json")

def load_jobs():
    if os.path.exists(JOB_LOG_FILE):
        try:
            with open(JOB_LOG_FILE) as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_jobs(jobs):
    try:
        with open(JOB_LOG_FILE, "w") as f:
            json.dump(jobs, f, indent=2)
    except:
        pass

@app.post("/job/start")
async def job_start(payload: dict):
    job_id = payload.get("job_id", f"job_{int(time.time())}")
    jobs = load_jobs()
    jobs[job_id] = {
        "job_id": job_id,
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "gpu_type": payload.get("gpu_type", "unknown"),
        "nodes": payload.get("nodes", 1),
        "user": payload.get("user", "unknown"),
        "status": "running",
        "metrics_at_start": {k: v[-1] if v else {} for k, v in metrics_store.items()}
    }
    save_jobs(jobs)
    return {"status": "ok", "job_id": job_id, "message": "Job start recorded"}

@app.post("/job/end")
async def job_end(payload: dict):
    job_id = payload.get("job_id")
    if not job_id:
        raise HTTPException(status_code=400, detail="job_id required")
    jobs = load_jobs()
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    jobs[job_id]["end_time"] = datetime.now().isoformat()
    jobs[job_id]["status"] = "complete"
    jobs[job_id]["metrics_at_end"] = {k: v[-1] if v else {} for k, v in metrics_store.items()}
    try:
        start = datetime.fromisoformat(jobs[job_id]["start_time"])
        end = datetime.fromisoformat(jobs[job_id]["end_time"])
        jobs[job_id]["duration_seconds"] = (end - start).total_seconds()
    except:
        jobs[job_id]["duration_seconds"] = None
    save_jobs(jobs)
    return {"status": "ok", "job_id": job_id, "duration_seconds": jobs[job_id].get("duration_seconds")}

@app.get("/jobs")
def list_jobs():
    return load_jobs()

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    jobs = load_jobs()
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return jobs[job_id]


# ========== CEI STANDARD DEFINITION ==========

CEI_STANDARD = {
    "standard": "Compute Energy Intensity (CEI)",
    "version": "1.0",
    "author": "Manmohan Bains",
    "contact": "mikebains41@gmail.com",
    "published": "2026-05-14",
    "definition": "CEI measures the number of floating-point operations delivered per joule of energy consumed during a sustained workload.",
    "formula": "CEI = Total_FLOPs / Total_Energy_Joules",
    "units": "FLOPs/J",
    "methodology": {
        "workload": "Continuous matrix multiplication (torch.matmul) at specified precision and matrix size",
        "minimum_duration_seconds": 900,
        "sampling_rate_hz": 1,
        "warm_up_iterations": "First iteration excluded (CUDA warm-up)",
        "power_measurement": "NVML via nvidia-smi, 1Hz sampling",
        "energy_calculation": "Trapezoidal integration of power over time",
        "utilization_measurement": "NVML GPU utilization percent, 1Hz sampling"
    },
    "benchmark_conditions": {
        "matrix_size": "2048x2048 (reference), 4096x4096 (extended)",
        "precision_classes": ["FP32", "FP16", "FP8 (H100 only)"],
        "idle_subtraction": False,
        "ambient_temperature_c": "recorded but not normalized",
        "persistence_mode": "as-found (hypervisor controlled)"
    },
    "reporting_format": {
        "required_fields": ["gpu_model", "platform", "matrix_size", "precision", "duration_sec", "total_flops", "total_energy_j", "cei_flops_per_joule"],
        "optional_fields": ["mean_power_w", "peak_power_w", "idle_power_w", "temperature_peak_c"]
    },
    "reference_values": {
        "a100_sxm_fp32_2048": {"cei": 5.68e9, "duration_sec": 900, "platform": "RunPod"},
        "a100_sxm_fp16_2048": {"cei": 3.56e9, "duration_sec": 600, "platform": "RunPod"},
        "h100_sxm_fp32_2048": {"cei": "pending_sustained_test", "platform": "RunPod"}
    },
    "known_limitations": [
        "NVML utilization may report 0% during active compute (telemetry desynchronization)",
        "Power cap and persistence mode may be blocked at hypervisor level",
        "CEI varies with thermal state — sustained tests more representative than burst"
    ],
    "citation": "Bains, M. (2026). GPU Telemetry Desynchronization and Idle Power Persistence Across NVIDIA AI Accelerators. github.com/mikebains41-debug/ai-gpu-energy-optimizer-"
}

@app.get("/standards/cei")
def get_cei_standard():
    return CEI_STANDARD

@app.get("/standards")
def list_standards():
    return {
        "standards": ["cei"],
        "note": "CEI — Compute Energy Intensity — is the primary efficiency metric of this platform.",
        "endpoint": "/standards/cei"
    }

# ========== AUTOMATED DETECTION ENGINE ==========

def load_csv_for_plot(gpu: str, test_id: str):
    base = f"get_data_dir()/tests/{gpu}"
    if not os.path.isdir(base):
        return None, None
    for folder in os.listdir(base):
        if test_id in folder:
            csv_path = os.path.join(base, folder, "data.csv")
            if os.path.exists(csv_path):
                import pandas as pd
                df = pd.read_csv(csv_path)
                df.columns = [c.strip() for c in df.columns]
                power_col = next((c for c in df.columns if 'power' in c.lower()), None)
                util_col = next((c for c in df.columns if 'util' in c.lower()), None)
                if power_col and util_col:
                    power_vals = df[power_col].astype(str).str.replace(' W', '', regex=False).astype(float)
                    util_vals = df[util_col].astype(str).str.replace(' %', '', regex=False).astype(float)
                    return {"power": power_vals.tolist(), "utilization": util_vals.tolist()}, folder
    return None, None


def run_detection(gpu: str, test_id: str):
    data, folder = load_csv_for_plot(gpu, test_id)
    events = []
    if data is None:
        return {"error": f"Test {test_id} not found for {gpu}"}
    power = data.get("power", [])
    util = data.get("utilization", [])
    # Clean string values (e.g., "75.61 W" -> 75.61)
    if power and isinstance(power[0], str):
        power = [float(p.split()[0]) for p in power]
    if util and isinstance(util[0], str):
        util = [float(u.split()[0]) for u in util]
    n = min(len(power), len(util))
    if n == 0:
        # Fallback to summary.json
        base = f"get_data_dir()/tests/{gpu}"
        path = find_test_result(base, test_id)
        if path:
            with open(path) as f:
                s = json.load(f)
            if s.get("ghost_power_detected"):
                events.append({"event": "ghost_power_detected", "severity": "HIGH", "evidence": f"Ghost power confirmed: {s.get('ghost_power_w', '?')}W at 0% utilization", "source": "summary.json"})
        return {"gpu": gpu, "test_id": test_id, "events": events, "note": "No data.csv — detection from summary.json only"}
    # ---- Adaptive baseline detection ----
    # Take first 10 idle samples (util < 0.1%) as baseline
    initial_idle = [power[i] for i in range(min(10, n)) if util[i] < 0.1]
    if not initial_idle:
        initial_idle = [min(power)]  # fallback
    import statistics
    baseline_idle = statistics.median(initial_idle)
    ghost_threshold = baseline_idle + 5.0   # 5W above median idle
    # Detection 1: Ghost Power (idle but power > threshold)
    ghost_samples = [(i, power[i]) for i in range(n) if util[i] < 0.1 and power[i] > ghost_threshold]
    if ghost_samples:
        max_ghost = max(p for _, p in ghost_samples)
        events.append({
            "event": "ghost_power_detected",
            "severity": "HIGH",
            "samples": len(ghost_samples),
            "peak_watts": round(max_ghost, 1),
            "baseline_idle_w": round(baseline_idle, 2),
            "threshold_w": round(ghost_threshold, 2),
            "evidence": f"{len(ghost_samples)} samples with power >{ghost_threshold:.1f}W at <0.1% utilization",
            "impact": "Standard monitoring tools would report this GPU as idle while it draws significant power"
        })
    # Detection 2: Cooldown Anomaly (last 25% of test, idle but power elevated)
    if n > 60:
        cooldown_start = int(n * 0.75)
        cooldown_power = [power[i] for i in range(cooldown_start, n) if util[i] < 0.1]
        if cooldown_power and max(cooldown_power) > ghost_threshold:
            events.append({
                "event": "cooldown_anomaly_detected",
                "severity": "MEDIUM",
                "samples": len([p for p in cooldown_power if p > ghost_threshold]),
                "mean_power_w": round(sum(cooldown_power)/len(cooldown_power), 1),
                "evidence": f"GPU maintained >{ghost_threshold:.0f}W during final 25% of test at 0% utilization",
                "impact": "P0 state retention — GPU not returning to low-power idle between workloads"
            })
    # Detection 3: Telemetry Desync (power jump >30W while util <5%)
    desync_samples = []
    for i in range(1, n):
        if power[i] - power[i-1] > 30 and util[i] < 5:
            desync_samples.append(i)
    if desync_samples:
        events.append({
            "event": "telemetry_desync_detected",
            "severity": "HIGH",
            "samples": len(desync_samples),
            "evidence": f"Power rose >30W while utilization stayed <5% — {len(desync_samples)} occurrences",
            "impact": "Utilization metric lags or fails to reflect actual compute activity"
        })
    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    events.sort(key=lambda e: severity_order.get(e.get("severity", "LOW"), 2))
    return {
        "gpu": gpu,
        "test_id": test_id,
        "samples_analyzed": n,
        "events_detected": len(events),
        "events": events,
        "status": "ANOMALOUS" if any(e["severity"] == "HIGH" for e in events) else "WARNING" if events else "NOMINAL"
    }


# ========== MULTI-PROVIDER FRAMEWORK ==========

PROVIDER_DATA = {
    "runpod": {
        "name": "RunPod",
        "url": "https://runpod.io",
        "gpus_tested": ["A100 SXM", "H100 SXM"],
        "status": "validated",
        "findings": {
            "ghost_power": True,
            "persistence_mode_controllable": False,
            "power_cap_controllable": False,
            "telemetry_desync": True,
            "hypervisor_restrictions": True
        },
        "a100_idle_w": 67.1,
        "h100_idle_w": 69.5,
        "a100_cei": 5.68e9,
        "notes": "Hypervisor blocks nvidia-smi power management. Ghost power confirmed on A100 SXM, absent on H100 SXM."
    },
    "aws": {
        "name": "Amazon Web Services (EC2)",
        "url": "https://aws.amazon.com",
        "gpus_tested": [],
        "status": "pending",
        "notes": "Validation planned. Expected instances: p4d.24xlarge (A100), p5.48xlarge (H100)."
    },
    "coreweave": {
        "name": "CoreWeave",
        "url": "https://coreweave.com",
        "gpus_tested": [],
        "status": "pending",
        "notes": "Validation planned. Bare-metal GPU access may allow persistence mode control."
    },
    "lambda": {
        "name": "Lambda Labs",
        "url": "https://lambdalabs.com",
        "gpus_tested": [],
        "status": "pending",
        "notes": "Validation planned."
    },
    "vast": {
        "name": "Vast.ai",
        "url": "https://vast.ai",
        "gpus_tested": [],
        "status": "pending",
        "notes": "Validation planned. Variable hardware may show broader ghost power distribution."
    }
}

@app.get("/providers")
def list_providers():
    return {
        "validated": [k for k, v in PROVIDER_DATA.items() if v["status"] == "validated"],
        "pending": [k for k, v in PROVIDER_DATA.items() if v["status"] == "pending"],
        "providers": PROVIDER_DATA
    }

@app.get("/providers/{provider_id}")
def get_provider(provider_id: str):
    if provider_id not in PROVIDER_DATA:
        raise HTTPException(status_code=404, detail=f"Provider {provider_id} not found. Available: {list(PROVIDER_DATA.keys())}")
    return PROVIDER_DATA[provider_id]

# ========== ENHANCED GRAFANA DASHBOARD ==========

GRAFANA_DASHBOARD = {
    "title": "GPU Energy Observability Platform — Telemetry Intelligence",
    "uid": "gpu-energy-obs-v2",
    "schemaVersion": 38,
    "version": 2,
    "refresh": "10s",
    "tags": ["gpu", "energy", "observability", "ai-infrastructure"],
    "panels": [
        {"id": 1, "title": "Live Board Power (W)", "type": "timeseries",
         "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
         "targets": [{"expr": "gpu_live_power_watts", "legendFormat": "{{cluster}} Power"}],
         "fieldConfig": {"defaults": {"unit": "watt", "color": {"fixedColor": "#ff6b35", "mode": "fixed"},
             "thresholds": {"steps": [{"color": "green", "value": 0}, {"color": "yellow", "value": 300}, {"color": "red", "value": 450}]}}}},
        {"id": 2, "title": "Live GPU Utilization (%)", "type": "timeseries",
         "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
         "targets": [{"expr": "gpu_live_utilization_percent", "legendFormat": "{{cluster}} Util"}],
         "fieldConfig": {"defaults": {"unit": "percent", "max": 100, "color": {"fixedColor": "#4ecdc4", "mode": "fixed"}}}},
        {"id": 3, "title": "Ghost Power Events (Total)", "type": "stat",
         "gridPos": {"x": 0, "y": 8, "w": 4, "h": 4},
         "targets": [{"expr": "gpu_ghost_power_events_total", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"thresholds": {"steps": [{"color": "green", "value": 0}, {"color": "red", "value": 1}]}, "mappings": [{"type": "value", "options": {"0": {"text": "NONE", "color": "green"}}}]}}},
        {"id": 4, "title": "Idle Power Floor (W)", "type": "stat",
         "gridPos": {"x": 4, "y": 8, "w": 4, "h": 4},
         "targets": [{"expr": "gpu_idle_power_floor_watts", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "watt", "thresholds": {"steps": [{"color": "green", "value": 0}, {"color": "yellow", "value": 70}, {"color": "red", "value": 100}]}}}},
        {"id": 5, "title": "CEI (FLOPs/J)", "type": "stat",
         "gridPos": {"x": 8, "y": 8, "w": 4, "h": 4},
         "targets": [{"expr": "gpu_cei_flops_per_joule", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "short", "color": {"mode": "thresholds"},
             "thresholds": {"steps": [{"color": "red", "value": 0}, {"color": "yellow", "value": 3e9}, {"color": "green", "value": 5e9}]}}}},
        {"id": 6, "title": "FP32 Peak TFLOPS", "type": "stat",
         "gridPos": {"x": 12, "y": 8, "w": 4, "h": 4},
         "targets": [{"expr": "gpu_fp32_peak_tflops", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "short"}}},
        {"id": 7, "title": "FP16 Peak TFLOPS", "type": "stat",
         "gridPos": {"x": 16, "y": 8, "w": 4, "h": 4},
         "targets": [{"expr": "gpu_fp16_peak_tflops", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "short", "color": {"fixedColor": "#a78bfa", "mode": "fixed"}}}},
        {"id": 8, "title": "Efficiency (GFLOPS/W)", "type": "stat",
         "gridPos": {"x": 20, "y": 8, "w": 4, "h": 4},
         "targets": [{"expr": "gpu_efficiency_gflops_per_watt", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "short", "color": {"mode": "thresholds"},
             "thresholds": {"steps": [{"color": "red", "value": 0}, {"color": "yellow", "value": 50}, {"color": "green", "value": 70}]}}}},
        {"id": 9, "title": "Live Temperature (°C)", "type": "timeseries",
         "gridPos": {"x": 0, "y": 12, "w": 12, "h": 8},
         "targets": [{"expr": "gpu_live_temperature_celsius", "legendFormat": "{{cluster}} Temp"}],
         "fieldConfig": {"defaults": {"unit": "celsius", "color": {"fixedColor": "#ffe66d", "mode": "fixed"},
             "thresholds": {"steps": [{"color": "green", "value": 0}, {"color": "yellow", "value": 70}, {"color": "red", "value": 85}]}}}},
        {"id": 10, "title": "Tests Completed per GPU", "type": "bargauge",
         "gridPos": {"x": 12, "y": 12, "w": 12, "h": 8},
         "targets": [{"expr": "gpu_tests_completed", "legendFormat": "{{gpu}}"}],
         "fieldConfig": {"defaults": {"unit": "short", "color": {"mode": "thresholds"},
             "thresholds": {"steps": [{"color": "blue", "value": 0}, {"color": "green", "value": 20}]}}}}
    ],
    "annotations": {"list": [{"name": "Ghost Power Events", "enable": True, "iconColor": "red"}]},
    "links": [
        {"title": "API Documentation", "url": "https://ai-gpu-brain-v3.onrender.com/docs", "type": "link"},
        {"title": "GitHub Repository", "url": "https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-", "type": "link"},
        {"title": "CEI Standard", "url": "https://ai-gpu-brain-v3.onrender.com/standards/cei", "type": "link"}
    ]
}




# ========== DETECTION ROUTES ==========

@app.get("/detect/{gpu}/{test_id}")
def detect_test(gpu: str, test_id: str):
    if gpu not in ["a100", "h100"]:
        raise HTTPException(status_code=400, detail="gpu must be a100 or h100")
    return run_detection(gpu, test_id)

@app.get("/detect/{gpu}")
def detect_all(gpu: str):
    if gpu not in ["a100", "h100"]:
        raise HTTPException(status_code=400, detail="gpu must be a100 or h100")
    base = f"get_data_dir()/tests/{gpu}"
    if not os.path.isdir(base):
        raise HTTPException(status_code=404, detail=f"No data for {gpu}")
    results = []
    for folder in sort_by_test_number(os.listdir(base)):
        spath = os.path.join(base, folder, "summary.json")
        if not os.path.exists(spath):
            continue
        with open(spath) as sf:
            s = json.load(sf)
        tid = s.get("test_id", folder)
        result = run_detection(gpu, tid)
        results.append({
            "test_id": tid,
            "name": s.get("name", ""),
            "events_detected": result.get("events_detected", 0),
            "status": result.get("status", "UNKNOWN"),
            "high_severity": sum(1 for e in result.get("events", []) if e.get("severity") == "HIGH")
        })
    total_anomalous = sum(1 for r in results if r["status"] == "ANOMALOUS")
    return {
        "gpu": gpu,
        "tests_scanned": len(results),
        "anomalous_tests": total_anomalous,
        "summary": results
    }




# ========== DETECTION ROUTES ==========

@app.get("/detect/{gpu}/{test_id}")
def detect_test(gpu: str, test_id: str):
    if gpu not in ["a100", "h100"]:
        raise HTTPException(status_code=400, detail="gpu must be a100 or h100")
    return run_detection(gpu, test_id)

@app.get("/detect/{gpu}")
def detect_all(gpu: str):
    if gpu not in ["a100", "h100"]:
        raise HTTPException(status_code=400, detail="gpu must be a100 or h100")
    base = f"get_data_dir()/tests/{gpu}"
    if not os.path.isdir(base):
        raise HTTPException(status_code=404, detail=f"No data for {gpu}")
    results = []
    for folder in sort_by_test_number(os.listdir(base)):
        spath = os.path.join(base, folder, "summary.json")
        if not os.path.exists(spath):
            continue
        with open(spath) as sf:
            s = json.load(sf)
        tid = s.get("test_id", folder)
        result = run_detection(gpu, tid)
        results.append({
            "test_id": tid,
            "name": s.get("name", ""),
            "events_detected": result.get("events_detected", 0),
            "status": result.get("status", "UNKNOWN"),
            "high_severity": sum(1 for e in result.get("events", []) if e.get("severity") == "HIGH")
        })
    total_anomalous = sum(1 for r in results if r["status"] == "ANOMALOUS")
    return {
        "gpu": gpu,
        "tests_scanned": len(results),
        "anomalous_tests": total_anomalous,
        "summary": results
    }



@app.on_event("startup")
def startup_check():
    """Ensure data directories exist (for fallback)."""
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    tests_dir = os.path.join(data_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

@app.get("/debug/path")
def debug_path():
    import os
    data_dir = get_data_dir()
    tests_dir = os.path.join(data_dir, "tests", "a100", "test-02_ghost_power_test")
    csv_path = os.path.join(tests_dir, "data.csv")
    return {
        "data_dir": data_dir,
        "tests_dir": tests_dir,
        "csv_exists": os.path.exists(csv_path),
        "cwd": os.getcwd(),
        "dir_listing": os.listdir(data_dir) if os.path.exists(data_dir) else None
    }
