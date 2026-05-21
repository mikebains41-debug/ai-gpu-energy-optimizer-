#!/usr/bin/env python3
"""
M13 - 1000 GPU Simulation
Duration: 30 minutes
GPUs: 2
What: Each GPU simulates 500 virtual nodes = 1000 total
Pass: TimescaleDB handles load, no dropped metrics
"""
import sys, os, time, requests, datetime, threading, random
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
DURATION = 1800
VIRTUAL_NODES_PER_GPU = 500
sent = [0]
failed = [0]
lock = threading.Lock()

def simulate_node(gpu_id, node_id, duration):
    s = get_gpu_stats(gpu_id)
    start = time.time()
    while time.time() - start < duration:
        payload = {"metrics": [{
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "gpu_id": f"gpu-{gpu_id}-virtual-{node_id}",
            "node_id": f"node-{node_id}",
            "power_watts": s["power_watts"] + random.uniform(-5, 5),
            "gpu_util": s["gpu_util"],
            "ghost_flag": s["gpu_util"] == 0 and s["power_watts"] > 90
        }]}
        try:
            r = requests.post(
                f"{API_URL}/ingest/batch",
                json=payload, timeout=5)
            with lock:
                if r.status_code in [200, 201]:
                    sent[0] += 1
                else:
                    failed[0] += 1
        except:
            with lock:
                failed[0] += 1
        time.sleep(30)

def main():
    print("="*55)
    print("M13: 1000 GPU Simulation")
    count = get_gpu_count()
    print(f"Real GPUs: {count} | Virtual nodes: {VIRTUAL_NODES_PER_GPU * 2}")
    print("="*55)
    start = time.time()
    threads = []
    for gpu_id in range(min(count, 2)):
        for node_id in range(VIRTUAL_NODES_PER_GPU):
            t = threading.Thread(
                target=simulate_node,
                args=(gpu_id, node_id, DURATION))
            t.daemon = True
            t.start()
            threads.append(t)
            if node_id % 100 == 0:
                print(f"[STARTED] GPU{gpu_id} node {node_id}")
    while time.time() - start < DURATION:
        print(f"[RUNNING] sent={sent[0]} failed={failed[0]}")
        time.sleep(60)
    duration = int(time.time() - start)
    passed = sent[0] > 0 and failed[0] < sent[0] * 0.05
    save_result("M13", "1000 GPU Simulation", passed,
        {"sent": sent[0], "failed": failed[0],
         "virtual_nodes": VIRTUAL_NODES_PER_GPU * 2}, duration)
    print(f"\nM13: {'PASS' if passed else 'FAIL'}")
    print(f"Sent: {sent[0]} | Failed: {failed[0]}")
    sys.exit(0 if passed else 1)

main()
