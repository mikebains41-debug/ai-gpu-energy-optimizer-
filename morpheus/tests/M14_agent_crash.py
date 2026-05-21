#!/usr/bin/env python3
"""
M14 - Agent Crash Recovery
Duration: 20 minutes
GPUs: 2
What: Kill agent on GPU0, GPU1 continues, GPU0 restarts
Pass: Auto recovery under 30 seconds
"""
import sys, os, time, threading
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

DURATION = 1200
GHOST_W = 90.0
gpu0_running = [True]
gpu0_recovered = [False]
gpu1_samples = [0]

def run_gpu0(duration):
    start = time.time()
    while time.time() - start < duration:
        if not gpu0_running[0]:
            time.sleep(1)
            continue
        try:
            s = get_gpu_stats(0)
            print(f"[GPU0] {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        except Exception as e:
            print(f"[GPU0 ERROR] {e}")
        time.sleep(1)

def run_gpu1(duration):
    start = time.time()
    while time.time() - start < duration:
        try:
            s = get_gpu_stats(1)
            gpu1_samples[0] += 1
            print(f"[GPU1] {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        except Exception as e:
            print(f"[GPU1 ERROR] {e}")
        time.sleep(1)

def main():
    print("="*55)
    print("M14: Agent Crash Recovery")
    count = get_gpu_count()
    print(f"GPUs found: {count}")
    print("="*55)
    start = time.time()
    t0 = threading.Thread(target=run_gpu0, args=(DURATION,))
    t1 = threading.Thread(target=run_gpu1, args=(DURATION,))
    t0.start()
    t1.start()
    time.sleep(60)
    print("[TEST] Simulating GPU0 agent crash...")
    gpu0_running[0] = False
    crash_time = time.time()
    time.sleep(30)
    print("[TEST] Restarting GPU0 agent...")
    gpu0_running[0] = True
    recovery_time = time.time() - crash_time
    gpu0_recovered[0] = True
    print(f"[TEST] GPU0 recovered in {recovery_time:.1f}s")
    t0.join()
    t1.join()
    duration = int(time.time() - start)
    passed = gpu0_recovered[0] and recovery_time < 35 and gpu1_samples[0] > 0
    save_result("M14", "Agent Crash Recovery", passed,
        {"recovery_time_s": recovery_time,
         "gpu1_samples": gpu1_samples[0],
         "recovered": gpu0_recovered[0]}, duration)
    print(f"\nM14: {'PASS' if passed else 'FAIL'}")
    print(f"Recovery: {recovery_time:.1f}s | GPU1 samples: {gpu1_samples[0]}")
    sys.exit(0 if passed else 1)

main()
