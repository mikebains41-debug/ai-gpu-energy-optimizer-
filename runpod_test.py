# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.
# Contact: Mikebains41@gmail.com
# Unauthorized use prohibited.

#!/usr/bin/env python3
import torch
import requests
import time
import pynvml

pynvml.nvmlInit()
h = pynvml.nvmlDeviceGetHandleByIndex(0)
url = "https://ai-gpu-brain-v3.onrender.com/api/v1/metrics"
headers = {"Authorization": "Bearer test_key_123"}

print("BASELINE (5 samples)...")
for i in range(5):
    util = pynvml.nvmlDeviceGetUtilizationRates(h).gpu
    power = pynvml.nvmlDeviceGetPowerUsage(h) / 1000
    data = {"cluster_id": "runpod-a100", "timestamp": time.time(), "gpus": [{"gpu_id": 0, "utilization_percent": util, "kernel_time_ms": 0, "memory_used_gb": 0, "memory_total_gb": 80, "temperature_celsius": 0, "power_draw_watts": power}]}
    requests.post(url, json=data, headers=headers)
    print(f"B{i}: util={util}% power={power:.0f}W")
    time.sleep(2)

print("WORKLOAD (20 kernels)...")
device = "cuda"
x = torch.randn(4096, 4096, device=device)
y = torch.randn(4096, 4096, device=device)

for i in range(20):
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    z = torch.matmul(x, y)
    end.record()
    torch.cuda.synchronize()
    ms = start.elapsed_time(end)
    util = pynvml.nvmlDeviceGetUtilizationRates(h).gpu
    power = pynvml.nvmlDeviceGetPowerUsage(h) / 1000
    data = {"cluster_id": "runpod-a100", "timestamp": time.time(), "gpus": [{"gpu_id": 0, "utilization_percent": util, "kernel_time_ms": ms, "memory_used_gb": 0, "memory_total_gb": 80, "temperature_celsius": 0, "power_draw_watts": power}]}
    requests.post(url, json=data, headers=headers)
    print(f"K{i}: {ms:.0f}ms util={util}% power={power:.0f}W")
    time.sleep(1)

print("DONE")
