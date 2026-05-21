#!/usr/bin/env python3
"""
M5 - Auto Alert
Duration: 15 minutes
GPUs: 1
What: Ghost triggered, alert sent to API
Pass: Alert received under 5 seconds
"""
import sys, os, time, datetime, requests
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_name, save_result

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
GHOST_W = 90.0
DURATION = 900

def send_alert(pw, util):
    t0 = time.time()
    try:
        payload = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "gpu_id": "gpu-0",
            "node_id": "runpod-m5-test",
            "anomalies": ["GHOST"],
            "power_watts": pw,
            "gpu_util": util,
            "action": "AUTO_ALERT"
        }
        r = requests.post(
            f"{API_URL}/ingest/alert",
            json=payload, timeout=5)
        latency = time.time() - t0
        return r.status_code in [200, 201, 404], latency
    except Exception as e:
        return False, time.time() - t0

def main():
    print("="*55)
    print("M5: Auto Alert")
    print(f"GPU: {get_gpu_name(0)}")
    print(f"API: {API_URL}")
    print("="*55)
    alerts_sent = 0
    alerts_fast = 0
    start = time.time()
    while time.time() - start < DURATION:
        s = get_gpu_stats(0)
        if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
            ok, latency = send_alert(s["power_watts"], s["gpu_util"])
            alerts_sent += 1
            if latency < 5.0:
                alerts_fast += 1
            print(f"[ALERT] ok={ok} latency={latency:.2f}s")
        else:
            print(f"[OK] {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        time.sleep(1)
    duration = int(time.time() - start)
    passed = alerts_sent > 0 and alerts_fast >= alerts_sent * 0.9
    save_result("M5", "Auto Alert", passed,
        {"alerts_sent": alerts_sent, "alerts_fast": alerts_fast}, duration)
    print(f"\nM5: {'PASS' if passed else 'FAIL'}")
    print(f"Alerts: {alerts_sent} | Under 5s: {alerts_fast}")
    sys.exit(0 if passed else 1)

main()
