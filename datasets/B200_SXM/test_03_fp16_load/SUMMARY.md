# B200 2x GPU Test 03 — FP16 Tensor Core Load Test Executive Summary

## Configuration
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Pod ID: aee29124a02b
Provider: RunPod
Date: 2026-05-28

## One Line Finding
Both B200 GPUs draw 195-202W at 0% reported utilization during FP16 compute.
Complete telemetry blackout — utilization never registers despite active compute.

## Test Details
Workload: FP16 tensor core matrix multiply 4096x4096
Framework: PyTorch 2.11.0+cu128
Both GPUs loaded simultaneously
Start: 2026/05/28 19:50:51 UTC
End: 2026/05/28 19:59:03 UTC
Duration: 8 minutes 12 seconds

## Key Numbers
GPU 0 sustained power: 195-199W at 0% utilization
GPU 1 sustained power: 197-202W at 0% utilization
SM clock: 1965 MHz throughout entire test
P-state: P0 maintained
Temperature: 31-35C
Combined FP16 power: 393-401W at 0% util

## Critical DESYNC Finding
Utilization reported 0% for entire 8 minute test
GPU clearly executing FP16 compute throughout
SM clock at 1965 MHz confirms active compute
Power elevated at 195-202W confirms active compute
Yet NVML reports 0% utilization consistently
This is complete telemetry blackout on B200 FP16

## FP16 vs FP32 Comparison
FP32 power: 237-239W at 7-9% util
FP16 power: 195-202W at 0% util
FP16 draws less power than FP32 on B200
FP16 has worse telemetry than FP32 on B200

## Status
COMPLETE — FP16 telemetry blackout confirmed
Most severe DESYNC finding yet on B200
Next: Test 04 Cooldown Profile

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28
