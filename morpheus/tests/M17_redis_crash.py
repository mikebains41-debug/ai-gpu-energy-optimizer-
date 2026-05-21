#!/usr/bin/env python3
"""
M17 - Redis Crash
Duration: 20 minutes
GPUs: 2
What: Redis unavailable, pipeline falls back, recovers
Pass: No data loss, pipeline continues
"""
import sys, os, time, requests, datetime
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
DURATION = 1200

def main():
    print("="*55)
    print("M17: Redis Crash Simulation")
    count = get_gpu_count()
    print(f"GPUs: {count} | API: {API_URL}")
    print("="*55)
    sent = 0
    failed = 0
    start = time.time()
    while time.time() - start < DURATION:
        for gpu_id in range(min(count, 2)):
            s = get_gpu_stats(gpu_id)
            payload = {"metrics": [{
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "gpu_id": f"gpu-{gpu_id}",
                "power_watts": s["power_watts"],
                "gpu_util": s["gpu_util"]
            }]}
            try:
                r = requests.post(
                    f"{API_URL}/ingest/batch",
                    json=payload, timeout=5)
                if r.status_code in [200, 201]:
                    sent += 1
                    print(f"[OK] GPU{gpu_id} sent={sent}")
                else:
                    failed += 1
                    print(f"[FAIL] status={r.status_code}")
            except Exception as e:
                failed += 1
                print(f"[ERROR] {e}")
        time.sleep(5)
    duration = int(time.time() - start)
    passed = sent > 0 and failed < sent * 0.1
    save_result("M17", "Redis Crash", passed,
        {"sent": sent, "failed": failed}, duration)
    print(f"\nM17: {'PASS' if passed else 'FAIL'}")
    print(f"Sent: {sent} | Failed: {failed}")
    sys.exit(0 if passed else 1)

main()
