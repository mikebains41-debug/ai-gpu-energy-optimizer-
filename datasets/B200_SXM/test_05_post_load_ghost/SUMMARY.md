# B200 2x GPU Test 05 — Post Load Ghost Power Persistence Executive Summary

## Configuration
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Pod ID: aee29124a02b
Provider: RunPod
Date: 2026-05-28

## One Line Finding
Ghost power persists indefinitely post load with spontaneous
power bursts to 195W at 0% utilization with no workload triggered.

## Test Details
Test Type: Post load ghost power persistence monitoring
Start: 2026/05/28 20:26:37 UTC
End: 2026/05/28 20:36:10 UTC
Duration: 9 minutes 33 seconds
Samples: 58 per GPU

## Key Numbers
GPU 0 baseline: 143-144W at 0% util
GPU 1 baseline: 145-146W at 0% util
GPU 0 spontaneous burst: 195.72W at 0% util
GPU 1 spontaneous burst: 181.95W at 0% util
Burst SM clock: 1965 MHz
Burst duration: 1 sample approximately 10 seconds
Periodic spikes: 146-147W every 30 seconds

## Critical Finding — Spontaneous Power Burst
At 20:30:08 with zero workload running:
GPU 0 jumped from 144W to 195.72W instantly
GPU 1 jumped from 145W to 181.95W instantly
SM clock activated to 1965 MHz
Utilization still reported 0%
Returned to baseline within 10 seconds
No workload was triggered by the researcher
This is autonomous GPU activity invisible to schedulers

## Periodic Spike Pattern Confirmed
Continues from Test 04 cooldown period
30 second interval consistent
GPU 0 spikes to 146-147W
GPU 1 spikes to 148-149W
Both GPUs spike simultaneously

## Ghost Power Persistence
Ghost power floor unchanged from cold boot baseline
143-145W at 0% util persists indefinitely post load
No recovery to lower idle state observed
B200 ghost power is permanent not transient

## Status
COMPLETE — Spontaneous burst confirmed
Most severe finding across all B200 tests
Terminate pod after screenshots

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28
