# B200 2x GPU Test 01 — Executive Summary

## Configuration
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Pod ID: aee29124a02b
Provider: RunPod
Date: 2026-05-28

## One Line Finding
Both B200 GPUs draw 143-145W each at 0% utilization from cold boot.
Combined idle ghost power: 288W across 2x B200 with zero workload.
No processes running. No workload ever executed.

## Test Duration
65 minutes continuous monitoring
148 total samples per GPU
296 total samples across both GPUs
Start: 2026/05/28 17:18:11 UTC
End: 2026/05/28 18:24:05 UTC

## Key Numbers Per GPU
GPU 0 average power: 143.47W at 0% utilization P0 locked
GPU 1 average power: 145.24W at 0% utilization P0 locked
GPU 0 power range: 143.20W to 145.67W
GPU 1 power range: 144.91W to 147.04W
Memory clock both GPUs: 3996 MHz at idle
SM clock both GPUs: 120 MHz at idle
VRAM used both GPUs: 0 MiB of 183,359 MiB

## Combined 2x B200 Metrics
Combined average power: 288.71W at 0% utilization
Combined power limit: 2000W
Combined VRAM: 360GB
Annual kWh wasted 2x B200: 2,527 kWh
Annual cost 2x B200: $252.70/year
Annual CO2 global grid: 1,010.8 kg
Annual CO2 Portugal solar: 121.3 kg
Annual CO2 BC Canada hydro: 30.3 kg

## Key Findings
Ghost power confirmed on B200 from cold boot
Both GPUs P0 locked from boot with zero workload
Memory subsystem active at 3996 MHz with zero compute
Power variance extremely low over 65 minutes
Inter-GPU power differential: 1.77W consistent
PyTorch 2.4.1 incompatible with B200 CUDA sm_100

## PyTorch Incompatibility
PyTorch 2.4.1 does not support B200 CUDA sm_100.
B200 requires CUDA capability sm_100.
Compute tests require nightly PyTorch build.
Software ecosystem not yet mature for B200.

## Status
CONFIRMED. 65 minutes sustained across 2x B200.
Not a transient. This is the stable B200 idle floor.

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28
