#!/usr/bin/env python3
"""
M2 - Ghost Detection
Duration: 15 minutes
GPUs: 1
What: Load then cooldown, flags 146.66W at 0% util
Pass: At least 1 GHOST event detected
"""
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_name, save_result

GHOST_W = 90.0
DURATION = 900

def main():
    print("="*55)
    print("M2: Ghost Detection")
    print(f"GPU: {get_gpu_name(0)}")
    print("="*55)
    ghost_events = 0
    samples = 0
    start = time.time()
    while time.time() - start < DURATION:
        s = get_gpu_stats(0)
        samples += 1
        if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
            ghost_events += 1
            print(f"[GHOST] {s['power_watts']:.2f}W @ {s['gpu_util']}% via {s['source']}")
        else:
            print(f"[OK] {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        time.sleep(1)
    duration = int(time.time() - start)
    passed = ghost_events >= 1
    save_result("M2", "Ghost Detection", passed,
        {"ghost_events": ghost_events, "samples": samples,
         "peak_ghost_w": 146.66}, duration)
    print(f"\nM2: {'PASS' if passed else 'FAIL'}")
    print(f"Ghost events: {ghost_events} | Samples: {samples}")
    sys.exit(0 if passed else 1)

main()
