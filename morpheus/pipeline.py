#!/usr/bin/env python3
"""
Morpheus GPU Telemetry Pipeline
Full pipeline: Detection + CEI scoring + Auto-alert
Author: Manmohan Bains
"""
import asyncio, aiohttp, json, os, datetime

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
ALERT_URL = f"{API_URL}/ingest/alert"
METRICS_URL = f"{API_URL}/ingest/batch"
GHOST_W = float(os.getenv("GHOST_POWER_THRESHOLD_W", 90))
DESYNC_W = float(os.getenv("DESYNC_POWER_THRESHOLD_W", 100))
DESYNC_PCT = float(os.getenv("DESYNC_UTIL_THRESHOLD_PCT", 5))
CEI_REFERENCE = 5.68e9  # A100 SXM FP32 baseline

def score_cei(flops, joules):
    if joules <= 0:
        return 0.0
    cei = flops / joules
    if cei > 10e9: tier = "EXCELLENT"
    elif cei > 5e9: tier = "GOOD"
    elif cei > 1e9: tier = "MODERATE"
    else: tier = "POOR"
    return {"cei": cei, "tier": tier, "vs_reference": cei / CEI_REFERENCE}

def detect(metric):
    pw = metric.get("power_watts", 0)
    util = metric.get("gpu_util", 0)
    anomalies = []
    if util == 0 and pw > GHOST_W:
        anomalies.append("GHOST")
    if util < DESYNC_PCT and pw > DESYNC_W:
        anomalies.append("DESYNC")
    return anomalies

async def alert(session, metric, anomalies, cei_result):
    payload = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "gpu_id": metric.get("gpu_id"),
        "node_id": metric.get("node_id"),
        "anomalies": anomalies,
        "power_watts": metric.get("power_watts"),
        "gpu_util": metric.get("gpu_util"),
        "cei": cei_result,
        "action": "AUTO_ALERT"
    }
    try:
        async with session.post(ALERT_URL, json=payload,
            timeout=aiohttp.ClientTimeout(total=5)) as r:
            if r.status == 200:
                print(f"[ALERT SENT] {anomalies} on {metric.get('gpu_id')}")
    except Exception as e:
        print(f"[ALERT FAILED] {e}")

async def process_stream(metrics, session):
    for metric in metrics:
        anomalies = detect(metric)
        flops = metric.get("flops", 0)
        joules = metric.get("joules", 0)
        cei_result = score_cei(flops, joules) if flops > 0 else None
        if anomalies:
            print(f"[ANOMALY] {anomalies} | {metric.get('gpu_id')} | {metric.get('power_watts')}W @ {metric.get('gpu_util')}%")
            await alert(session, metric, anomalies, cei_result)
        else:
            print(f"[OK] {metric.get('gpu_id')} | {metric.get('power_watts')}W @ {metric.get('gpu_util')}%")

async def main():
    print("="*60)
    print("  MORPHEUS GPU PIPELINE — Ghost + CEI + Auto-Alert")
    print(f"  API: {API_URL}")
    print("="*60)
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(
                    f"{API_URL}/metrics/a100",
                    timeout=aiohttp.ClientTimeout(total=10)) as r:
                    if r.status == 200:
                        data = await r.json()
                        metrics = []
                        for gpu_list in data.values():
                            for entry in gpu_list:
                                for gpu in entry.get("gpus", []):
                                    metrics.append({
                                        "gpu_id": gpu.get("id", "gpu-0"),
                                        "node_id": "runpod",
                                        "power_watts": gpu.get("power_draw_watts", 0),
                                        "gpu_util": gpu.get("utilization_percent", 0),
                                    })
                        await process_stream(metrics, session)
            except Exception as e:
                print(f"[ERROR] {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
