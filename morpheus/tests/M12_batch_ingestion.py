#!/usr/bin/env python3
"""
M12 - Batch Ingestion
Duration: 30 minutes
GPUs: 2
What: Both GPUs sending metrics to API simultaneously
Pass: Zero data loss, API handles load
"""
import sys, os, time, requests, datetime, threading
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
DURATION = 1800
sent = {0: 0, 1: 0}
failed = {0: 0, 1: 0}

def ingest_gpu(gpu_id, duration):
    start = time.time()
    while time.time() - start < duration:
        s = get_gpu_stats(gpu_id)
        payload = {"metrics": [{
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "gpu_id": f"gpu-{gpu_id}",
            "node_id": "runpod-m12",
            "power_watts": s["power_watts"],
            "gpu_util": s["gpu_util"],
            "ghost_flag": s["gpu_util"] == 0 and s["power_watts"] > 90
        }]}
        try:
            r = requests.post(
                f"{API_URL}/ingest/batch",
                json=payload, timeout=5)
            if r.status_code in [200, 201]:
                sent[gpu_id] += 1
            else:
                failed[gpu_id] += 1
        except:
            failed[gpu_id] += 1
        time.sleep(5)

def main():
    print("="*55)
    print("M12: Batch Ingestion")
    count = get_gpu_count()
    print(f"GPUs: {count} | API: {API_URL}")
    print("="*55)
    start = time.time()
    threads = []
    for gpu_id in range(min(count, 2)):
        t = threading.Thread(target=ingest_gpu, args=(gpu_id, DURATION))
        t.start()
        threads.append(t)
    while time.time() - start < DURATION:
        print(f"[RUNNING] sent={sent} failed={failed}")
        time.sleep(30)
    for t in threads:
        t.join()
    duration = int(time.time() - start)
    total_sent = sum(sent.values())
    total_failed = sum(failed.values())
    passed = total_sent > 0 and total_failed == 0
    save_result("M12", "Batch Ingestion", passed,
        {"sent": sent, "failed": failed}, duration)
    print(f"\nM12: {'PASS' if passed else 'FAIL'}")
    print(f"Sent: {total_sent} | Failed: {total_failed}")
    sys.exit(0 if passed else 1)

main()
