#!/usr/bin/env python3
"""
M11 - Mixed Workload
Duration: 25 minutes
GPUs: 2
What: GPU0 FP32 active, GPU1 idle with ghost
Pass: CEI scored on GPU0, ghost on GPU1
"""
import sys, os, time, threading
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result
try:
    import torch
except ImportError:
    os.system("pip install torch -q")
    import torch

DURATION = 1500
MATRIX_SIZE = 4096
GHOST_W = 90.0
CEI_REFERENCE = 5.68e9
gpu0_cei = [0]
gpu1_ghost = [0]

def run_gpu0(duration):
    device = torch.device("cuda:0")
    a = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
    b = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
    total_flops = 0
    total_joules = 0
    start = time.time()
    while time.time() - start < duration:
        t0 = time.time()
        torch.matmul(a, b)
        torch.cuda.synchronize()
        t1 = time.time()
        s = get_gpu_stats(0)
        total_flops += 2 * MATRIX_SIZE**3
        total_joules += s["power_watts"] * (t1 - t0)
    if total_joules > 0:
        gpu0_cei[0] = total_flops / total_joules

def monitor_gpu1(duration):
    start = time.time()
    while time.time() - start < duration:
        s = get_gpu_stats(1)
        if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
            gpu1_ghost[0] += 1
            print(f"[GHOST] GPU1 {s['power_watts']:.2f}W @ {s['gpu_util']}%")
        time.sleep(1)

def main():
    print("="*55)
    print("M11: Mixed Workload")
    count = get_gpu_count()
    print(f"GPUs found: {count}")
    print("="*55)
    if count < 2:
        print("SKIP: Need 2 GPUs")
        sys.exit(0)
    start = time.time()
    t0 = threading.Thread(target=run_gpu0, args=(DURATION,))
    t1 = threading.Thread(target=monitor_gpu1, args=(DURATION,))
    t0.start()
    t1.start()
    t0.join()
    t1.join()
    duration = int(time.time() - start)
    cei = gpu0_cei[0]
    passed = cei > 5e9 and gpu1_ghost[0] >= 1
    save_result("M11", "Mixed Workload", passed,
        {"gpu0_cei": cei, "gpu1_ghost_events": gpu1_ghost[0]}, duration)
    print(f"\nM11: {'PASS' if passed else 'FAIL'}")
    print(f"GPU0 CEI: {cei:.3e} | GPU1 Ghost: {gpu1_ghost[0]}")
    sys.exit(0 if passed else 1)

main()
