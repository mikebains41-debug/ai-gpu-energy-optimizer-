# VRAM Test 26 — Workload
**Researcher:** Mike Bains | mikebains41@gmail.com

## What This Proves
NVML reports 0% memory utilization with 807MB loaded.
VRAM clears immediately after process exits.

## Key Numbers
- memory.used during workload = 807 MB
- util.memory during workload = 0% (NVML lie)
- VRAM clear time after exit = immediate (1 sample)
- Ghost power unchanged = 65.84W before and after

## Next
- test-27: VRAM residual 100Hz poll
