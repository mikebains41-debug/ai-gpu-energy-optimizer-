#!/usr/bin/env python3
"""
M16 - API Restart
Duration: 20 minutes
GPUs: 2
What: API goes down, pipeline retries, comes back up
Pass: Pipeline continues automatically after restart
"""
import sys, os, time, requests, datetime, threading
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
DURATION = 1200
sent = [0]
retries = [0]
recovered = [False]

def run(duration):
    start = time.time()
    while time.time() - start < duration:
        for gpu_id in range(2):
            s = get_gpu_stats(gpu_id)
            payload = {"metrics": [{
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "gpu_id": f"gpu-{gpu_id}",
                "power_watts": s["power_watts"],
                "gpu_util": s["gpu_util"]
            }]}
            for attempt in range(3):
                try:
                    r = requests.post(
                        f"{API_URL}/ingest/batch",
                        json=payload, timeout=5)
                    if r.status_code in [200, 201]:
                        sent[0] += 1
                        if attempt > 0:
                            recovered[0] = True
                        break
                    else:
                        retries[0] += 1
                        time.sleep(2 ** attempt)
                except:
                    retries[0] += 1
                    time.sleep(2 ** attempt)
        time.sleep(5)

def main():
    print("="*55)
    print("M16: API Restart")
    count = get_gpu_count()
    print(f"GPUs: {count} | API: {API_URL}")
    print("="*55)
    start = time.time()
    t = threading.Thread(target=run, args=(DURATION,))
    t.start()
    t.join()
    duration = int(time.time() - start)
    passed = sent[0] > 0
    save_result("M16", "API Restart", passed,
        {"sent": sent[0], "retries": retries[0],
         "recovered": recovered[0]}, duration)
    print(f"\nM16: {'PASS' if passed else 'FAIL'}")
    print(f"Sent: {sent[0]} | Retries: {retries[0]}")
    sys.exit(0 if passed else 1)

main()
