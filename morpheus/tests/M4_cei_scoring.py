#!/usr/bin/env python3
"""
M4 - CEI Scoring
Duration: 20 minutes
GPUs: 1
What: FP32 workload, score CEI vs 5.68B FLOPs/J reference
Pass: GOOD or EXCELLENT tier
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
CEI_REFERENCE = 5.68e9
MATRIX_SIZE = 4096

def main():
    print("="*55)
    print("M4: CEI Scoring")
    print(f"GPU: {get_gpu_name(0)}")
    print("="*55)
    device = torch.device("cuda:0")
    a = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
    b = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device=device)
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
    if cei > 10e9: tier = "EXCELLENT"
    elif cei > 5e9: tier = "GOOD"
    elif cei > 1e9: tier = "MODERATE"
    else: tier = "POOR"
    duration = int(time.time() - start)
    passed = tier in ["EXCELLENT", "GOOD"]
    save_result("M4", "CEI Scoring", passed,
        {"cei": cei, "tier": tier, "vs_reference": cei/CEI_REFERENCE,
         "iterations": iterations}, duration)
    print(f"\nM4: {'PASS' if passed else 'FAIL'}")
    print(f"CEI: {cei:.3e} FLOPs/J | Tier: {tier}")
    print(f"vs Reference: {cei/CEI_REFERENCE:.2f}x")
    sys.exit(0 if passed else 1)

main()
