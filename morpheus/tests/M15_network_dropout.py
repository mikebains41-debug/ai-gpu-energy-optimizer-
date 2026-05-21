#!/usr/bin/env python3
"""
M15 - Network Dropout
Duration: 20 minutes
GPUs: 2
What: Cut API connection 60 seconds, buffer holds, reconnects
Pass: No data lost on reconnect
"""
import sys, os, time, requests, datetime, threading
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
DURATION = 1200
buffer = []
sent = [0]
failed = [0]
network_up = [True]
lock = threading.Lock()

def collect(duration):
    start = time.time()
    while time.time() - start < duration:
        for gpu_id in range(2):
            s = get_gpu_stats(gpu_id)
            with lock:
                buffer.append({
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "gpu_id": f"gpu-{gpu_id}",
                    "power_watts": s["power_watts"],
                    "gpu_util": s["gpu_util"]
                })
        time.sleep(5)

def flush(duration):
    start = time.time()
    while time.time() - start < duration:
        if not network_up[0]:
            print(f"[BUFFER] network down, holding {len(buffer)} metrics")
            time.sleep(5)
            continue
        with lock:
            if buffer:
                try:
                    r = requests.post(
                        f"{API_URL}/ingest/batch",
                        json={"metrics": buffer.copy()},
                        timeout=5)
                    if r.status_code in [200, 201]:
                        sent[0] += len(buffer)
                        buffer.clear()
                        print(f"[FLUSH] sent {sent[0]} total")
                    else:
                        failed[0] += 1
                except:
                    failed[0] += 1
        time.sleep(5)

def main():
    print("="*55)
    print("M15: Network Dropout")
    count = get_gpu_count()
    print(f"GPUs: {count} | API: {API_URL}")
    print("="*55)
    start = time.time()
    tc = threading.Thread(target=collect, args=(DURATION,))
    tf = threading.Thread(target=flush, args=(DURATION,))
    tc.start()
    tf.start()
    time.sleep(60)
    print("[TEST] Simulating network dropout...")
    network_up[0] = False
    time.sleep(60)
    print("[TEST] Restoring network...")
    network_up[0] = True
    tc.join()
    tf.join()
    duration = int(time.time() - start)
    passed = sent[0] > 0 and len(buffer) == 0
    save_result("M15", "Network Dropout", passed,
        {"sent": sent[0], "failed": failed[0],
         "buffer_remaining": len(buffer)}, duration)
    print(f"\nM15: {'PASS' if passed else 'FAIL'}")
    print(f"Sent: {sent[0]} | Failed: {failed[0]} | Buffer: {len(buffer)}")
    sys.exit(0 if passed else 1)

main()
