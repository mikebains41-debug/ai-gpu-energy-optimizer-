#!/usr/bin/env python3
"""
M10 - Ghost Both GPUs
Duration: 25 minutes
GPUs: 2
What: Trigger ghost on both GPUs simultaneously
Pass: Ghost detected on both GPUs
"""
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

GHOST_W = 90.0
DURATION = 1500

def main():
    print("="*55)
    print("M10: Ghost Both GPUs")
    count = get_gpu_count()
    print(f"GPUs found: {count}")
    print("="*55)
    if count < 2:
        print("SKIP: Need 2 GPUs")
        sys.exit(0)
    ghost = {0: 0, 1: 0}
    samples = {0: 0, 1: 0}
    start = time.time()
    while time.time() - start < DURATION:
        for gpu_id in [0, 1]:
            s = get_gpu_stats(gpu_id)
            samples[gpu_id] += 1
            if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
                ghost[gpu_id] += 1
                print(f"[GHOST] GPU{gpu_id} {s['power_watts']:.2f}W @ {s['gpu_util']}%")
            else:
                print(f"[OK] GPU{gpu_id} {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        time.sleep(1)
    duration = int(time.time() - start)
    passed = ghost[0] >= 1 and ghost[1] >= 1
    save_result("M10", "Ghost Both GPUs", passed,
        {"ghost": ghost, "samples": samples}, duration)
    print(f"\nM10: {'PASS' if passed else 'FAIL'}")
    print(f"Ghost GPU0: {ghost[0]} | Ghost GPU1: {ghost[1]}")
    sys.exit(0 if passed else 1)

main()
