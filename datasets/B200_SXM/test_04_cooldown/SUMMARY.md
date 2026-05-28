# B200 2x GPU Test 04 — Cooldown Profile Executive Summary

## Configuration
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Pod ID: aee29124a02b
Provider: RunPod
Date: 2026-05-28

## One Line Finding
B200 returns to ghost power floor immediately after FP16 load stops.
No cooldown period. Periodic power spikes at 30 second intervals confirmed.

## Test Details
Test Type: Post-load cooldown monitoring
Previous test: FP16 tensor core load Test 03
Start: 2026/05/28 20:05:27 UTC
End: 2026/05/28 20:14:19 UTC
Duration: 8 minutes 52 seconds
Samples: 54 per GPU

## Key Numbers
GPU 0 baseline: 143-144W at 0% util 120 MHz
GPU 1 baseline: 145-146W at 0% util 120 MHz
GPU 0 spike: 146-147W periodic every 30 seconds
GPU 1 spike: 147-148W periodic every 30 seconds
SM clock: immediately returned to 120 MHz
P-state: P0 maintained throughout

## Critical Finding — No Cooldown
B200 returned to ghost power floor immediately.
No gradual decay observed.
No elevated post-load power retention.
Power dropped from 195-202W FP16 load to 143-145W instantly.
This differs from A100 SXM which retained elevated power post-load.

## New Finding — Periodic Power Spikes
Power spikes observed every approximately 30 seconds.
GPU 0 spikes: 146.05W to 146.63W
GPU 1 spikes: 147.79W to 148.54W
Spikes last approximately 1 sample then return to baseline.
Cause unknown — possibly background GPU management activity.

## Status
COMPLETE — Cooldown profile documented
No cooldown period on B200
Periodic spike pattern discovered
Next: Test 05 Post Load Ghost Power Comparison

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28
