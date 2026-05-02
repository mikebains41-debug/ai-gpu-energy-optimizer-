#!/usr/bin/env python3
import torch
print("Running matrix multiplication workload...")
x = torch.randn(4096, 4096, device='cuda')
y = torch.randn(4096, 4096, device='cuda')
for i in range(100):
    z = torch.matmul(x, y)
    torch.cuda.synchronize()
print("Done.")
