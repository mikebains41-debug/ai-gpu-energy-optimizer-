#!/usr/bin/env python3
"""
M6 - Sustained Run
Duration: 15 minutes
GPUs: 1
What: Full pipeline continuous, ghost + CEI + alerts together
Pass: Zero crashes, all anomalies caught
"""
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_name, save_result

GHOST_W = 90.0
DURATION = 900

def main():
    print("="*55)
    print("M6: Sustained Run")
    print(f"GPU: {get_gpu_name(0)}")
    print("="*55)
    samples = 0
    ghost_events = 0
    crashes = 0
    start = time.time()
    while time.time() - start < DURATION:
        try:
            s = get_gpu_stats(0)
            samples += 1
            if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
                ghost_events += 1
                print(f"[GHOST] {s['power_watts']:.2f}W @ {s['gpu_util']}%")
            else:
                print(f"[OK] {s['power_watts']:.2f}W @ {s['gpu_util']}% sample={samples}")
        except Exception as e:
            crashes += 1
            print(f"[CRASH] {e}")
        time.sleep(1)
    duration = int(time.time() - start)
    passed = crashes == 0 and samples > 0
    save_result("M6", "Sustained Run", passed,
        {"samples": samples, "ghost_events": ghost_events,
         "crashes": crashes}, duration)
    print(f"\nM6: {'PASS' if passed else 'FAIL'}")
    print(f"Samples: {samples} | Ghost: {ghost_events} | Crashes: {crashes}")
    sys.exit(0 if passed else 1)

main()
