# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Manmohan Bains. All Rights Reserved.
# Contact: mikebains41@gmail.com
# Unauthorized use prohibited.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from datetime import datetime
import asyncio
import json
import os
import time
from typing import List, Dict, Optional

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

# ========== DYNAMIC TEST RESULTS SCANNER ==========
def load_test_results(gpu_type: str = "a100") -> List[Dict]:
    results = []
    base_path = f"/opt/render/project/src/data/tests/{gpu_type}"
    if not os.path.exists(base_path):
        return results
    for test_dir in sorted(os.listdir(base_path)):
        if not test_dir.startswith("test-"):
            continue
        summary_file = os.path.join(base_path, test_dir, "summary.json")
        if os.path.exists(summary_file):
            try:
                with open(summary_file, "r") as f:
                    data = json.load(f)
                    if "test_id" not in data:
                        data["test_id"] = test_dir
                    results.append(data)
            except Exception:
                pass
    return results

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

def get_metrics_list() -> List[Dict]:
    result = []
    for cluster_id, measurements in metrics_store.items():
        for m in measurements:
            m_copy = m.copy()
            m_copy['cluster_id'] = cluster_id
            result.append(m_copy)
    return result

# ========== TEST RESULTS ENDPOINTS ==========
@app.get("/results/a100")
def get_a100_results():
    return load_test_results("a100")

@app.get("/results/h100")
def get_h100_results():
    return load_test_results("h100")

@app.get("/results/a100/{test_num}")
def get_a100_test_result(test_num: str):
    base = "/opt/render/project/src/data/tests/a100"
    padded = test_num.zfill(2)
    prefix = f"test-{padded}"
    if os.path.exists(base):
        for folder in sorted(os.listdir(base)):
            if folder == prefix or folder.startswith(prefix):
                path = os.path.join(base, folder, "summary.json")
                if os.path.exists(path):
                    with open(path) as f:
                        return json.load(f)
    raise HTTPException(status_code=404, detail=f"Test {test_num} not found. Valid range: 1-24")

@app.get("/results/h100/{test_num}")
def get_h100_test_result(test_num: str):
    base = "/opt/render/project/src/data/tests/h100"
    padded = test_num.zfill(2)
    prefix = f"test-{padded}"
    if os.path.exists(base):
        for folder in sorted(os.listdir(base)):
            if folder == prefix or folder.startswith(prefix):
                path = os.path.join(base, folder, "summary.json")
                if os.path.exists(path):
                    with open(path) as f:
                        return json.load(f)
    raise HTTPException(status_code=404, detail=f"Test {test_num} not found. Valid range: 1-11")

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

@app.get("/debug/list_tests")
def list_tests():
    import os
    base = os.path.join(os.path.dirname(__file__), "data", "tests", "a100")
    if not os.path.exists(base):
        return {"error": f"Path {base} does not exist"}
    folders = sorted([d for d in os.listdir(base) if d.startswith("test-")])
    return {"base_path": base, "folders": folders}


@app.get("/ghost-power")
def ghost_power_summary():
    return {
        "definition": "Ghost power = GPU draws significant power while NVML reports 0% utilization (telemetry desync)",
        "finding": "A100 SXM confirmed ghost power. H100 SXM not affected.",
        "peak_ghost_power_w": 146.7,
        "idle_floor_w": 67.1,
        "a100_tests_affected": 4,
        "a100_total_tests": 24,
        "h100_tests_affected": 0,
        "h100_total_tests": 11,
        "confirmed_tests": [
            {"test_id": "test-02", "ghost_power_w": 102.14, "reported_utilization_pct": 0, "duration_sec": 60},
            {"test_id": "test-13", "ghost_power_w": 146.66, "reported_utilization_pct": 0, "duration_sec": 660, "samples_affected": 17},
            {"test_id": "test-14", "ghost_power_w": 134.59, "reported_utilization_pct": 0, "duration_sec": 1200},
        ],
        "root_cause": "NVML telemetry desync - power and utilization counters update on different clocks.",
        "financial_impact_usd": {
            "per_gpu_per_year": 58.70,
            "at_1000_gpus": 58700,
            "at_1_million_gpus": 58700000,
        },
    }

@app.get("/compare")
def list_comparisons():
    return {"available": ["/compare/gpu", "/compare/precision", "/compare/matrix-size", "/compare/ghost-power", "/compare/idle"]}

@app.get("/compare/gpu")
def compare_gpu():
    return {
        "comparison": "A100 SXM vs H100 SXM",
        "platform": "RunPod",
        "a100_sxm": {"idle_power_w": 67.1, "peak_power_w": 501.86, "fp32_tflops": 14.35, "fp16_tflops": 231.08, "cei_fp32_sustained": 5.68e9, "efficiency_gflops_per_w": 52.6, "ghost_power_detected": True, "ghost_power_peak_w": 146.66, "total_tests": 24},
        "h100_sxm": {"idle_power_w": 69.5, "peak_power_w": 412.0, "fp32_tflops": 49.13, "fp16_tflops": 592.8, "cei_fp32_burst": 4.91e13, "efficiency_gflops_per_w": 76.5, "ghost_power_detected": False, "total_tests": 11},
        "key_differences": ["H100 FP32 throughput 2.8x higher (49.13 vs 17.37 TFLOPS)", "H100 FP16 throughput 2.6x higher (592.8 vs 231.08 TFLOPS)", "H100 efficiency 45% better (76.5 vs 52.6 GFLOPS/W)", "A100 ghost power confirmed - H100 shows none across all 11 tests"],
    }

@app.get("/compare/precision")
def compare_precision():
    return {
        "comparison": "FP32 vs FP16 on A100 SXM",
        "gpu": "NVIDIA A100 SXM (RunPod)",
        "matrix_size": "2048x2048",
        "fp32_sustained_15min": {"test_id": "test-24", "precision": "FP32", "duration_sec": 900, "iterations": 90000, "avg_power_w": 302.37, "tflops": 14.35, "total_energy_j": 272130, "cei_flops_per_joule": 5.68e9, "cei_class": "Good"},
        "fp16_sustained_10min": {"test_id": "test-19", "precision": "FP16", "duration_sec": 600, "iterations": 60000, "avg_power_w": 482.7, "peak_power_w": 501.86, "tflops": 231.08, "cei_flops_per_joule": 3.56e9, "cei_class": "Moderate"},
        "analysis": {"throughput_ratio": "FP16 is 16x faster in throughput", "power_ratio": "FP16 draws 60% more power (482.7W vs 302.4W)", "cei_ratio": "FP32 CEI is 1.6x better", "recommendation": "FP32 for energy efficiency. FP16 for max throughput."},
    }

@app.get("/compare/matrix-size")
def compare_matrix_size():
    return {
        "comparison": "Power vs Matrix Size - A100 SXM",
        "test_id": "test-18",
        "precision": "FP32",
        "data_points": [
            {"matrix_size": 512, "power_w": 188.95},
            {"matrix_size": 1024, "power_w": 240.0},
            {"matrix_size": 2048, "power_w": 302.4},
            {"matrix_size": 4096, "power_w": 330.0},
            {"matrix_size": 6144, "power_w": 339.1, "note": "Peak power"},
            {"matrix_size": 8192, "power_w": 327.37, "note": "Memory bandwidth saturation"},
        ],
        "conclusion": "Power peaks at 6144x6144 then drops. CEI peaks at 4096x4096.",
    }

@app.get("/compare/ghost-power")
def compare_ghost_power():
    return {
        "comparison": "Ghost Power: A100 SXM vs H100 SXM",
        "a100_sxm": {"ghost_power_detected": True, "tests_affected": 4, "total_tests": 24, "peak_ghost_power_w": 146.66, "idle_floor_w": 67.1, "pstate": "P0 persistent after load", "memory_clock_mhz": 1593},
        "h100_sxm": {"ghost_power_detected": False, "tests_affected": 0, "total_tests": 11, "idle_floor_w": 69.5, "load_scaling": "Linear - clean telemetry"},
        "conclusion": "Ghost power specific to A100 SXM on RunPod. H100 shows no desync across all 11 tests.",
    }

@app.get("/compare/idle")
def compare_idle():
    return {
        "comparison": "Idle Power Floors by GPU",
        "data": [
            {"gpu": "Tesla T4", "idle_w": 9.5, "ghost_power": False},
            {"gpu": "RTX 4090", "idle_w": 20.0, "ghost_power": False},
            {"gpu": "A40", "idle_w": 30.4, "ghost_power": False},
            {"gpu": "A100 PCIe", "idle_w": 47.0, "ghost_power": False},
            {"gpu": "A100 SXM", "idle_w": 67.1, "ghost_power": True, "source": "measured test-15 test-23"},
            {"gpu": "H100 SXM", "idle_w": 69.5, "ghost_power": False, "source": "measured h100/test-01"},
        ],
    }
