#!/usr/bin/env python3
"""
M9 - 2 GPU Load Test
Duration: 20 minutes
GPUs: 2
What: Both GPUs under load, no data loss
Pass: Zero errors across both GPUs
"""
import sys, os, time, threading
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_name, get_gpu_count, save_result
try:
    import torch
except ImportError:
    os.system("pip install torch -q")
    import torch

DURATION = 1200
MATRIX_SIZE = 4096

results = {0: [], 1: []}
errors = {0: 0, 1: 0}

def load_gpu(gpu_id, duration):
    try:
        device = torch.device(f"cuda:{gpu_id}")
        a = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
        b = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
        start = time.time()
        while time.time() - start < duration:
            torch.matmul(a, b)
            torch.cuda.synchronize()
            s = get_gpu_stats(gpu_id)
            results[gpu_id].append(s["power_watts"])
    except Exception as e:
        errors[gpu_id] += 1
        print(f"[ERROR] GPU{gpu_id} {e}")

def main():
    print("="*55)
    print("M9: 2 GPU Load Test")
    count = get_gpu_count()
    print(f"GPUs found: {count}")
    print("="*55)
    if count < 2:
        print("SKIP: Need 2 GPUs")
        sys.exit(0)
    start = time.time()
    t0 = threading.Thread(target=load_gpu, args=(0, DURATION))
    t1 = threading.Thread(target=load_gpu, args=(1, DURATION))
    t0.start()
    t1.start()
    while time.time() - start < DURATION:
        print(f"[RUNNING] GPU0 samples={len(results[0])} GPU1 samples={len(results[1])}")
        time.sleep(10)
    t0.join()
    t1.join()
    duration = int(time.time() - start)
    passed = len(results[0]) > 0 and len(results[1]) > 0 and errors[0] == 0 and errors[1] == 0
    save_result("M9", "2 GPU Load Test", passed,
        {"gpu0_samples": len(results[0]), "gpu1_samples": len(results[1]),
         "errors": errors}, duration)
    print(f"\nM9: {'PASS' if passed else 'FAIL'}")
    print(f"GPU0: {len(results[0])} | GPU1: {len(results[1])} | Errors: {errors}")
    sys.exit(0 if passed else 1)

main()
