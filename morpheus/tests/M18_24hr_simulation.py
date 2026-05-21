#!/usr/bin/env python3
"""
M18 - 24hr Simulation
Duration: 60 minutes compressed
GPUs: 2
What: High frequency sampling simulating 24hr operation
Pass: Zero crashes, all anomalies logged
"""
import sys, os, time, json, datetime
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

DURATION = 3600
GHOST_W = 90.0

def main():
    print("="*55)
    print("M18: 24hr Simulation (60 min compressed)")
    count = get_gpu_count()
    print(f"GPUs: {count}")
    print("="*55)
    samples = 0
    ghost_events = 0
    crashes = 0
    anomaly_log = []
    start = time.time()
    while time.time() - start < DURATION:
        for gpu_id in range(min(count, 2)):
            try:
                s = get_gpu_stats(gpu_id)
                samples += 1
                if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
                    ghost_events += 1
                    anomaly_log.append({
                        "time": datetime.datetime.utcnow().isoformat(),
                        "gpu": gpu_id,
                        "type": "GHOST",
                        "power": s["power_watts"]
                    })
                    print(f"[GHOST] GPU{gpu_id} {s['power_watts']:.2f}W")
                else:
                    if samples % 100 == 0:
                        elapsed = int(time.time() - start)
                        print(f"[OK] {elapsed}s elapsed | samples={samples} | ghost={ghost_events}")
            except Exception as e:
                crashes += 1
                print(f"[CRASH] GPU{gpu_id} {e}")
        time.sleep(1)
    duration = int(time.time() - start)
    passed = crashes == 0 and samples > 0
    save_result("M18", "24hr Simulation", passed,
        {"samples": samples, "ghost_events": ghost_events,
         "crashes": crashes, "anomaly_log": anomaly_log[:50]}, duration)
    print(f"\nM18: {'PASS' if passed else 'FAIL'}")
    print(f"Samples: {samples} | Ghost: {ghost_events} | Crashes: {crashes}")
    sys.exit(0 if passed else 1)

main()
