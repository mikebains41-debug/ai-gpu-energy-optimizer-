#!/usr/bin/env python3
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result
try:
    import torch
except ImportError:
    os.system("pip install torch -q")
    import torch

DURATION = 1800
CEI_REFERENCE = 5.68e9
MATRIX_SIZE = 4096
TOLERANCE = 0.15

def main():
    print("M20: CEI Accuracy")
    count = get_gpu_count()
    results = {}
    for gpu_id in range(min(count, 2)):
        device = torch.device(f"cuda:{gpu_id}")
        a = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
        b = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
        total_flops = 0
        total_joules = 0
        iterations = 0
        start = time.time()
        while time.time() - start < DURATION / min(count, 2):
            t0 = time.time()
            torch.matmul(a, b)
            torch.cuda.synchronize()
            t1 = time.time()
            s = get_gpu_stats(gpu_id)
            total_flops += 2 * MATRIX_SIZE**3
            total_joules += s["power_watts"] * (t1 - t0)
            iterations += 1
        cei = total_flops / total_joules if total_joules > 0 else 0
        error = abs(cei - CEI_REFERENCE) / CEI_REFERENCE
        results[gpu_id] = {"cei": cei, "error": error}
        print(f"GPU{gpu_id} CEI: {cei:.3e} Error: {error*100:.2f}%")
    passed = all(r["error"] <= TOLERANCE for r in results.values())
    save_result("M20", "CEI Accuracy", passed,
        {"results": {str(k): v for k, v in results.items()},
         "reference": CEI_REFERENCE}, DURATION)
    print(f"M20: {'PASS' if passed else 'FAIL'}")
    sys.exit(0 if passed else 1)

main()
