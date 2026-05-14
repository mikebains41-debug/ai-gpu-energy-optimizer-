# Test-15 – A100 SXM Idle Baseline (15 minutes)

## Protocol
- No workload, 1 Hz sampling via nvidia-smi
- Duration: 15 minutes (900 samples)

## Results
- Mean power: ~67.1 W
- Utilisation: 0% throughout
- Temperature: 27°C steady

## Significance
Establishes idle power floor for A100 SXM on RunPod. Waste vs A40 (30.4 W) is ~36 W per GPU.
