#!/bin/bash
# Re-run all 3 experiments cleanly for validation

echo "=== Re-running Experiment 2: Sampling Rate Test ==="
python3 experiment2_sampling.py

echo ""
echo "=== Re-running Experiment 3: Load Ramp Test ==="
python3 experiment3_load_ramp.py

echo ""
echo "=== Re-running Experiment 1: High-Frequency Poll ==="
python3 -c "
import time, torch, pynvml
pynvml.nvmlInit()
h = pynvml.nvmlDeviceGetHandleByIndex(0)
print('HIGH-FREQUENCY POLL (10 samples)')
for i in range(10):
    u = pynvml.nvmlDeviceGetUtilizationRates(h).gpu
    p = pynvml.nvmlDeviceGetPowerUsage(h) / 1000
    a = torch.randn(4096,4096,device='cuda')
    b = torch.randn(4096,4096,device='cuda')
    c = torch.matmul(a,b)
    torch.cuda.synchronize()
    print(f'{i}: util={u}% power={p:.1f}W')
"

echo ""
echo "=== All experiments complete ==="
