#!/usr/bin/env python3
"""
M8 - 2 GPU Simultaneous
Duration: 20 minutes
GPUs: 2
What: Both GPUs monitored, ghost on GPU0, clean on GPU1
Pass: Both GPUs reporting correctly
"""
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_name, get_gpu_count, save_result

GHOST_W = 90.0
DURATION = 1200

def main():
    print("="*55)
    print("M8: 2 GPU Simultaneous")
    count = get_gpu_count()
    print(f"GPUs found: {count}")
    print("="*55)
    if count < 2:
        print("SKIP: Need 2 GPUs")
        sys.exit(0)
    samples = {0: 0, 1: 0}
    ghost = {0: 0, 1: 0}
    errors = {0: 0, 1: 0}
    start = time.time()
    while time.time() - start < DURATION:
        for gpu_id in [0, 1]:
            try:
                s = get_gpu_stats(gpu_id)
                samples[gpu_id] += 1
                if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
                    ghost[gpu_id] += 1
                    print(f"[GHOST] GPU{gpu_id} {s['power_watts']:.2f}W @ {s['gpu_util']}%")
                else:
                    print(f"[OK] GPU{gpu_id} {s['power_watts']:.2f}W @ {s['gpu_util']}%")
            except Exception as e:
                errors[gpu_id] += 1
                print(f"[ERROR] GPU{gpu_id} {e}")
        time.sleep(1)
    duration = int(time.time() - start)
    passed = samples[0] > 0 and samples[1] > 0 and errors[0] == 0 and errors[1] == 0
    save_result("M8", "2 GPU Simultaneous", passed,
        {"samples": samples, "ghost": ghost, "errors": errors}, duration)
    print(f"\nM8: {'PASS' if passed else 'FAIL'}")
    print(f"GPU0: {samples[0]} samples | GPU1: {samples[1]} samples")
    sys.exit(0 if passed else 1)

main()
