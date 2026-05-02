#!/usr/bin/env python3
"""
Experiment 3: Load Ramp Test
Ramps workload from 0% to 100% to test physical causality
"""

import time
import json
import torch
import pynvml
from datetime import datetime

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

def get_metrics():
    util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
    return util, power

def run_workload(load_percent, duration=10):
    scale = load_percent / 100.0
    size = int(512 + (8192 - 512) * scale)
    a = torch.randn(size, size, device='cuda')
    b = torch.randn(size, size, device='cuda')
    start_time = time.time()
    iterations = 0
    while time.time() - start_time < duration:
        c = torch.matmul(a, b)
        torch.cuda.synchronize()
        iterations += 1
    return size, iterations

def main():
    print("=" * 60)
    print("EXPERIMENT 3: Load Ramp Test (0% → 100%)")
    print("=" * 60)
    
    load_levels = [0, 10, 25, 50, 75, 90, 100]
    results = {"timestamp": datetime.now().isoformat(), "loads": []}
    
    for load in load_levels:
        print(f"\n📊 Running at {load}% load...")
        util_before, power_before = get_metrics()
        size, iterations = run_workload(load, duration=15)
        util_during, power_during = get_metrics()
        
        results["loads"].append({
            "load_percent": load,
            "matrix_size": size,
            "iterations": iterations,
            "util_before": util_before,
            "power_before": power_before,
            "util_during": util_during,
            "power_during": power_during
        })
        
        print(f"   Size: {size}x{size}")
        print(f"   Util: {util_before}% → {util_during}%")
        print(f"   Power: {power_before:.1f}W → {power_during:.1f}W")
        print(f"   Iterations: {iterations}")
        time.sleep(2)
    
    with open("experiment3_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Saved to experiment3_results.json")

if __name__ == "__main__":
    main()
