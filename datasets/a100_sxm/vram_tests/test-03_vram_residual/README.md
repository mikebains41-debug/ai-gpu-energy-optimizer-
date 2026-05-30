# VRAM Test 27 — Residual
**Researcher:** Mike Bains | mikebains41@gmail.com

## What This Proves
382MB VRAM persists after process exits and empty_cache is called.
NVML reports 0% memory utilization while 425MB is still allocated.

## Key Numbers
- VRAM loaded: 807 MB
- VRAM after clear: 425 MB
- VRAM residual: 382 MB (47.3%)
- util.memory reported: 0%
- Both GPUs: identical residual

## Security Implication
In multi-tenant cloud environments the next tenant
could access 382MB of previous tenant VRAM data.
No monitoring tool can detect this — NVML reports 0%.

## Architecture
A100 SXM4 80GB — RunPod container — Linux GPU passthrough
Verda bare metal test pending to confirm architectural origin

## Related Tests
- test-25: VRAM baseline — 0MB at idle
- test-26: VRAM workload — 807MB loaded
- test-27: VRAM residual — 382MB stuck (this test)
