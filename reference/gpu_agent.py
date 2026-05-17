"""
GPU Energy Optimizer — Full Test Agent
=======================================
Runs complete test suite on your GPU:
1. Idle baseline
2. Ghost power detection
3. CEI benchmark (FP32)
4. FP16 vs FP32 comparison

Requirements: torch, pynvml, requests
Usage: python gpu_agent.py --api-key YOUR_KEY
"""

import time
import json
import argparse
import requests
import torch
import pynvml

API_URL = "https://ai-gpu-brain-v2.onrender.com"

def get_gpu_info(handle):
    name = pynvml.nvmlDeviceGetName(handle)
    if isinstance(name, bytes):
        name = name.decode()
    return name

def sample_power(handle):
    return pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0

def sample_utilization(handle):
    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
    return util.gpu

def run_idle_baseline(handle, duration=60):
    print(f"[1/4] Running idle baseline ({duration}s)...")
    samples = []
    for _ in range(duration):
        samples.append({
            "power_w": sample_power(handle),
            "utilization_pct": sample_utilization(handle)
        })
        time.sleep(1)
    avg_power = sum(s["power_w"] for s in samples) / len(samples)
    min_power = min(s["power_w"] for s in samples)
    max_power = max(s["power_w"] for s in samples)
    print(f"    Idle avg: {avg_power:.1f}W  min: {min_power:.1f}W  max: {max_power:.1f}W")
    return {
        "test": "idle_baseline",
        "duration_sec": duration,
        "avg_power_w": round(avg_power, 2),
        "min_power_w": round(min_power, 2),
        "max_power_w": round(max_power, 2),
        "samples": len(samples)
    }

def run_ghost_power(handle, duration=120):
    print(f"[2/4] Running ghost power test ({duration}s load + cooldown)...")
    A = torch.randn(4096, 4096, device='cuda', dtype=torch.float32)
    B = torch.randn(4096, 4096, device='cuda', dtype=torch.float32)

    load_samples = []
    for _ in range(duration // 2):
        torch.matmul(A, B)
        torch.cuda.synchronize()
        load_samples.append({
            "power_w": sample_power(handle),
            "utilization_pct": sample_utilization(handle)
        })
        time.sleep(1)

    del A, B
    torch.cuda.empty_cache()

    cooldown_samples = []
    for _ in range(duration // 2):
        cooldown_samples.append({
            "power_w": sample_power(handle),
            "utilization_pct": sample_utilization(handle)
        })
        time.sleep(1)

    ghost_events = [s for s in cooldown_samples
                   if s["power_w"] > 80 and s["utilization_pct"] == 0]
    peak_ghost = max((s["power_w"] for s in cooldown_samples), default=0)

    print(f"    Ghost power events: {len(ghost_events)}")
    print(f"    Peak ghost power: {peak_ghost:.1f}W")

    return {
        "test": "ghost_power",
        "ghost_power_detected": len(ghost_events) > 0,
        "ghost_power_events": len(ghost_events),
        "peak_ghost_power_w": round(peak_ghost, 2),
        "cooldown_samples": len(cooldown_samples)
    }

def run_cei_benchmark(handle, matrix_size=2048, duration=300):
    print(f"[3/4] Running CEI benchmark FP32 ({duration}s)...")
    A = torch.randn(matrix_size, matrix_size, device='cuda', dtype=torch.float32)
    B = torch.randn(matrix_size, matrix_size, device='cuda', dtype=torch.float32)
    flops_per_matmul = 2 * (matrix_size ** 3)
    total_flops = 0
    power_samples = []
    start = time.time()

    while time.time() - start < duration:
        torch.matmul(A, B)
        torch.cuda.synchronize()
        total_flops += flops_per_matmul
        power_samples.append(sample_power(handle))
        time.sleep(0.1)

    elapsed = time.time() - start
    avg_power = sum(power_samples) / len(power_samples)
    total_joules = avg_power * elapsed
    cei = total_flops / total_joules

    print(f"    CEI: {cei:.3e} FLOPs/J")
    print(f"    Avg power: {avg_power:.1f}W")

    return {
        "test": "cei_fp32",
        "matrix_size": matrix_size,
        "duration_sec": round(elapsed, 1),
        "total_flops": total_flops,
        "avg_power_w": round(avg_power, 2),
        "total_joules": round(total_joules, 2),
        "cei_flops_per_joule": round(cei, 0)
    }

def run_fp16_comparison(handle, matrix_size=2048, iterations=100):
    print(f"[4/4] Running FP32 vs FP16 comparison ({iterations} iterations each)...")

    A32 = torch.randn(matrix_size, matrix_size, device='cuda', dtype=torch.float32)
    B32 = torch.randn(matrix_size, matrix_size, device='cuda', dtype=torch.float32)
    fp32_power = []
    start = time.time()
    for _ in range(iterations):
        torch.matmul(A32, B32)
        torch.cuda.synchronize()
        fp32_power.append(sample_power(handle))
    fp32_time = time.time() - start

    A16 = A32.half()
    B16 = B32.half()
    fp16_power = []
    start = time.time()
    for _ in range(iterations):
        torch.matmul(A16, B16)
        torch.cuda.synchronize()
        fp16_power.append(sample_power(handle))
    fp16_time = time.time() - start

    avg_fp32 = sum(fp32_power) / len(fp32_power)
    avg_fp16 = sum(fp16_power) / len(fp16_power)

    print(f"    FP32 avg power: {avg_fp32:.1f}W")
    print(f"    FP16 avg power: {avg_fp16:.1f}W")
    print(f"    FP16 speedup: {fp32_time/fp16_time:.1f}x faster")

    return {
        "test": "fp16_vs_fp32",
        "matrix_size": matrix_size,
        "iterations": iterations,
        "fp32_avg_power_w": round(avg_fp32, 2),
        "fp16_avg_power_w": round(avg_fp16, 2),
        "fp32_time_s": round(fp32_time, 2),
        "fp16_time_s": round(fp16_time, 2),
        "speedup": round(fp32_time / fp16_time, 2)
    }

def submit_results(results, api_key):
    try:
        resp = requests.post(
            f"{API_URL}/api/v1/metrics",
            json=results,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        if resp.status_code == 200:
            print(f"\n✅ Results submitted successfully")
        else:
            print(f"\n⚠️  Submission returned {resp.status_code}")
    except Exception as e:
        print(f"\n⚠️  Could not submit: {e}")

def main():
    parser = argparse.ArgumentParser(description="GPU Energy Optimizer — Full Test Agent")
    parser.add_argument("--api-key", default="anonymous", help="Your API key")
    parser.add_argument("--quick", action="store_true", help="Quick mode (shorter tests)")
    args = parser.parse_args()

    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    gpu_name = get_gpu_info(handle)

    print(f"\n{'='*50}")
    print(f"GPU Energy Optimizer — Full Test Suite")
    print(f"GPU: {gpu_name}")
    print(f"API: {API_URL}")
    print(f"{'='*50}\n")

    duration = 30 if args.quick else 60

    results = {
        "gpu": gpu_name,
        "api_key": args.api_key,
        "timestamp": time.time(),
        "tests": []
    }

    results["tests"].append(run_idle_baseline(handle, duration))
    results["tests"].append(run_ghost_power(handle, duration * 2))
    results["tests"].append(run_cei_benchmark(handle, duration=duration * 5))
    results["tests"].append(run_fp16_comparison(handle))

    print(f"\n{'='*50}")
    print("RESULTS SUMMARY")
    print(f"{'='*50}")
    for test in results["tests"]:
        print(f"\n{test['test'].upper()}:")
        for k, v in test.items():
            if k != "test":
                print(f"  {k}: {v}")

    print(f"\n{'='*50}")
    submit_results(results, args.api_key)
    pynvml.nvmlShutdown()

    output_file = f"gpu_results_{int(time.time())}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
