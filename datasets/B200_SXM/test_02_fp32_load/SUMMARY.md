# B200 2x GPU Test 02 — FP32 Load Test Executive Summary

## Configuration
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Pod ID: aee29124a02b
Provider: RunPod
Date: 2026-05-28

## One Line Finding
Both B200 GPUs ramp from 143W idle to 237-239W under FP32 load
at only 7-9% reported utilization — classic DESYNC pattern confirmed.

## Test Details
Workload: FP32 matrix multiply 4096x4096
Framework: PyTorch 2.11.0+cu128
Both GPUs loaded simultaneously
Start: 2026/05/28 19:24:04 UTC

## Power Ramp Sequence
Both GPUs idle: 143-145W at 0% util
Load start: 168-175W
Ramp: 190W to 209W to 220W to 230W
Sustained: 237-239W at 7-9% utilization
Combined sustained load power: ~477W

## Key Numbers
GPU 0 idle: 143.99W at 0% util
GPU 0 peak: 238.84W at 7-9% util
GPU 1 idle: 145.72W at 0% util
GPU 1 peak: 239.26W at 9% util
SM clock: jumped from 120 MHz to 1965 MHz on load
P-state: P0 maintained throughout
VRAM: active during compute

## DESYNC Finding
B200 draws 237-239W at only 7-9% reported utilization
Power increase: 94W above idle at single digit utilization
This is the DESYNC pattern — power and utilization misaligned
Full load will draw significantly more

## Combined 2x B200 Load Power
Combined idle: 288W
Combined sustained FP32: ~477W
Combined peak observed: ~478W
Power increase from idle: +189W combined

## PyTorch Version
Successfully installed PyTorch 2.11.0+cu128
B200 CUDA sm_100 now supported
Previous PyTorch 2.4.1 was incompatible

## Status
COMPLETE — FP32 load confirmed
DESYNC pattern confirmed on B200
Next: Test 03 FP16 load test

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28
