#!/bin/bash
# Nsight Systems Test for A100 Ghost Power Validation

echo "=== Nsight Systems Test ==="
echo "Running matrix multiplication workload with Nsight tracing..."

nsys profile \
  --trace=cuda,nvtx,osrt \
  --output=a100_ghost_trace \
  --force-overwrite=true \
  python3 -c "
import torch
print('Running 100 matrix multiplications...')
x = torch.randn(4096, 4096, device='cuda')
y = torch.randn(4096, 4096, device='cuda')
for i in range(100):
    z = torch.matmul(x, y)
    torch.cuda.synchronize()
    if (i+1) % 20 == 0:
        print(f'  Completed {i+1}/100')
print('Done. Check a100_ghost_trace.nsys-rep')
"

echo "Trace saved to a100_ghost_trace.nsys-rep"
