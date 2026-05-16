"""
GPU Energy Optimizer — CEI Reference Implementation
====================================================
CEI = Total FLOPs / Total Joules

Minimal public script for independent verification.
Full production engine is proprietary.

Requirements: torch, pynvml
Usage: python cei_reference.py
"""

import time
import torch
import pynvml

def measure_cei(matrix_size=4096, duration_seconds=60, sample_interval=0.1):
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)

    power_samples = []
    start_time = time.time()

    A = torch.randn(matrix_size, matrix_size, device='cuda', dtype=torch.float32)
    B = torch.randn(matrix_size, matrix_size, device='cuda', dtype=torch.float32)

    flops_per_matmul = 2 * (matrix_size ** 3)
    total_flops = 0
    iterations = 0

    while time.time() - start_time < duration_seconds:
        torch.matmul(A, B)
        torch.cuda.synchronize()
        iterations += 1
        total_flops += flops_per_matmul
        power_mw = pynvml.nvmlDeviceGetPowerUsage(handle)
        power_samples.append(power_mw / 1000.0)
        time.sleep(sample_interval)

    elapsed = time.time() - start_time
    avg_power_w = sum(power_samples) / len(power_samples)
    total_joules = avg_power_w * elapsed
    cei = total_flops / total_joules

    print(f"Matrix size:  {matrix_size}x{matrix_size}")
    print(f"Duration:     {elapsed:.1f}s")
    print(f"Iterations:   {iterations}")
    print(f"Total FLOPs:  {total_flops:.2e}")
    print(f"Avg Power:    {avg_power_w:.1f}W")
    print(f"Total Joules: {total_joules:.1f}J")
    print(f"CEI:          {cei:.3e} FLOPs/J")

    pynvml.nvmlShutdown()
    return cei

if __name__ == "__main__":
    measure_cei()
