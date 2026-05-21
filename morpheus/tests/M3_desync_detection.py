#!/usr/bin/env python3
"""
M3 - DESYNC Detection
Duration: 15 minutes
GPUs: 1
What: High power low util scenario
Pass: At least 1 DESYNC event detected
"""
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_name, save_result

DESYNC_W = 100.0
DESYNC_PCT = 5.0
DURATION = 900

def main():
    print("="*55)
    print("M3: DESYNC Detection")
    print(f"GPU: {get_gpu_name(0)}")
    print("="*55)
    desync_events = 0
    samples = 0
    start = time.time()
    while time.time() - start < DURATION:
        s = get_gpu_stats(0)
        samples += 1
        if s["gpu_util"] < DESYNC_PCT and s["power_watts"] > DESYNC_W:
            desync_events += 1
            print(f"[DESYNC] {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        else:
            print(f"[OK] {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        time.sleep(1)
    duration = int(time.time() - start)
    passed = desync_events >= 1
    save_result("M3", "DESYNC Detection", passed,
        {"desync_events": desync_events, "samples": samples}, duration)
    print(f"\nM3: {'PASS' if passed else 'FAIL'}")
    print(f"DESYNC events: {desync_events} | Samples: {samples}")
    sys.exit(0 if passed else 1)

main()
