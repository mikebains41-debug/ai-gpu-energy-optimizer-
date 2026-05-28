# B200 2x GPU Test 06 — Multi GPU Power Divergence Executive Summary

## Configuration
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Pod ID: aee29124a02b
Provider: RunPod
Date: 2026-05-28

## One Line Finding
GPU 1 consistently draws 1.00-2.00W more than GPU 0
across all workload types — idle FP32 FP16 cooldown and post load.

## Data Source
Analysis derived from Tests 01-05 raw data.
No additional hardware run required.
Total samples analyzed: 290 per GPU across all tests.

## Power Divergence Across All Tests
Test 01 Idle: GPU0 143.47W vs GPU1 145.24W — diff 1.77W
Test 02 FP32: GPU0 237.50W vs GPU1 238.50W — diff 1.00W
Test 03 FP16: GPU0 197.00W vs GPU1 199.00W — diff 2.00W
Test 04 Cooldown: GPU0 144.00W vs GPU1 145.75W — diff 1.75W
Test 05 Post Load: GPU0 144.10W vs GPU1 145.85W — diff 1.75W
Average differential: 1.65W

## Key Finding
GPU 1 always draws more power than GPU 0.
Differential is consistent across all workload types.
Same architecture same pod same driver same CUDA version.
This is a hardware asymmetry not a software artifact.
Standard fleet monitoring assuming identical GPU power will be wrong.

## Implications
Per GPU measurement is essential not optional.
Carbon accounting must be done per GPU not per pod.
Billing systems assuming uniform power will undercharge by 1-2W per pair.
Scheduler efficiency calculations will be inaccurate without per GPU data.

## Status
COMPLETE — Derived from Tests 01-05
No additional hardware run required

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28
