#!/usr/bin/env python3
"""
M7 - FP16 CEI Score
Duration: 20 minutes
GPUs: 1
What: FP16 workload CEI vs FP32 baseline
Pass: EXCELLENT tier and faster than FP32
"""
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_name, save_result
try:
    import torch
except ImportError:
    os.system("pip install torch -q")
    import torch

DURATION = 1200
MATRIX_SIZE = 4096
FP32_REFERENCE = 5.68e9

def main():
    print("="*55)
    print("M7: FP16 CEI Score")
    print(f"GPU: {get_gpu_name(0)}")
    print("="*55)
    device = torch.device("cuda:0")
    a = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device, dtype=torch.float16)
    b = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device, dtype=torch.float16)
    total_flops = 0
    total_joules = 0
    iterations = 0
    start = time.time()
    while time.time() - start < DURATION:
        t0 = time.time()
        torch.matmul(a, b)
        torch.cuda.synchronize()
        t1 = time.time()
        s = get_gpu_stats(0)
        flops = 2 * MATRIX_SIZE**3
        joules = s["power_watts"] * (t1 - t0)
        total_flops += flops
        total_joules += joules
        iterations += 1
        if iterations % 100 == 0:
            print(f"[OK] iter={iterations} power={s['power_watts']:.1f}W")
    cei = total_flops / total_joules if total_joules > 0 else 0
    speedup = cei / FP32_REFERENCE
    if cei > 10e9: tier = "EXCELLENT"
    elif cei > 5e9: tier = "GOOD"
    else: tier = "BELOW"
    duration = int(time.time() - start)
    passed = tier == "EXCELLENT" and speedup > 2.0
    save_result("M7", "FP16 CEI Score", passed,
        {"cei": cei, "tier": tier, "speedup_vs_fp32": speedup,
         "iterations": iterations}, duration)
    print(f"\nM7: {'PASS' if passed else 'FAIL'}")
    print(f"FP16 CEI: {cei:.3e} | Tier: {tier} | Speedup: {speedup:.2f}x")
    sys.exit(0 if passed else 1)

main()
