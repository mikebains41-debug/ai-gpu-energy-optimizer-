#!/usr/bin/env python3
"""
FINAL PROOF TEST - Synchronized Nsight + Power/Utilization Logging
Run with: nsys profile --trace=cuda,nvtx --output=final_proof python3 final_proof_test.py
"""

import torch
import time
import pynvml

pynvml.nvmlInit()
h = pynvml.nvmlDeviceGetHandleByIndex(0)

print("timestamp,util,power")

for i in range(50):
    u = pynvml.nvmlDeviceGetUtilizationRates(h).gpu
    p = pynvml.nvmlDeviceGetPowerUsage(h) / 1000
    print(f"{time.time()},{u},{p:.1f}")
    
    # Sustained workload - 4096 matmul, 10 iterations
    a = torch.randn(4096, 4096, device='cuda')
    b = torch.randn(4096, 4096, device='cuda')
    for _ in range(10):
        c = torch.matmul(a, b)
    torch.cuda.synchronize()
    
    time.sleep(0.2)

print("DONE")
