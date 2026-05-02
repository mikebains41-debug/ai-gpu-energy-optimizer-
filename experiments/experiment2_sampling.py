#!/usr/bin/env python3
"""
Experiment 2: Sampling Rate Test
Compares 1s, 100ms, and 10ms sampling resolutions
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

def run_sampler(sample_interval, duration=30, name=""):
    samples = []
    a = torch.randn(4096, 4096, device='cuda')
    b = torch.randn(4096, 4096, device='cuda')
    
    start_time = time.time()
    while time.time() - start_time < duration:
        loop_start = time.time()
        c = torch.matmul(a, b)
        torch.cuda.synchronize()
        util, power = get_metrics()
        samples.append({"time": time.time() - start_time, "util": util, "power": power})
        elapsed = time.time() - loop_start
        if elapsed < sample_interval:
            time.sleep(sample_interval - elapsed)
    return samples

def analyze_samples(samples):
    if not samples:
        return {"error": "no samples"}
    utils = [s["util"] for s in samples]
    powers = [s["power"] for s in samples]
    return {
        "count": len(samples),
        "util_mean": sum(utils) / len(utils),
        "util_min": min(utils),
        "util_max": max(utils),
        "power_mean": sum(powers) / len(powers),
        "power_min": min(powers),
        "power_max": max(powers)
    }

def main():
    print("=" * 60)
    print("EXPERIMENT 2: Sampling Rate Test")
    print("=" * 60)
    
    results = {"timestamp": datetime.now().isoformat(), "tests": {}}
    
    print("\n📊 Running 1-second sampling (60 seconds)...")
    samples_1s = run_sampler(1.0, duration=60)
    results["tests"]["1s"] = analyze_samples(samples_1s)
    print(f"   Samples collected: {len(samples_1s)}")
    
    print("\n📊 Running 100ms sampling (30 seconds)...")
    samples_100ms = run_sampler(0.1, duration=30)
    results["tests"]["100ms"] = analyze_samples(samples_100ms)
    print(f"   Samples collected: {len(samples_100ms)}")
    
    print("\n📊 Running 10ms sampling (10 seconds)...")
    samples_10ms = run_sampler(0.01, duration=10)
    results["tests"]["10ms"] = analyze_samples(samples_10ms)
    print(f"   Samples collected: {len(samples_10ms)}")
    
    with open("experiment2_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print("CLASSIFICATION:")
    c1, c2, c3 = results["tests"]["1s"], results["tests"]["100ms"], results["tests"]["10ms"]
    if c1["util_mean"] == 0 and (c2["util_mean"] > 0 or c3["util_mean"] > 0):
        print("✅ ANOMALY: Higher sampling reveals compute (aliasing issue)")
    elif c1["util_mean"] == 0 and c2["util_mean"] == 0 and c3["util_mean"] == 0:
        print("⚠️ PERSISTENT: No compute detected at any resolution")
    else:
        print("✅ NORMAL: All sampling rates consistent")
    
    print(f"\n✅ Saved to experiment2_results.json")

if __name__ == "__main__":
    main()
