# B200 VRAM Test 08 — Workload
**Researcher:** Mike Bains | mikebains41@gmail.com

## Key Numbers
- VRAM loaded = 1,010 MB
- util.memory during load = 0% (NVML lie)
- VRAM after clear = 628 MB
- Residual = 382 MB
- Power after clear = 198-206W (stays elevated)

## New Finding vs A100
A100 power drops to 65W after clear.
B200 power stays at 198-206W after clear.
B200 ghost power more persistent than A100.
