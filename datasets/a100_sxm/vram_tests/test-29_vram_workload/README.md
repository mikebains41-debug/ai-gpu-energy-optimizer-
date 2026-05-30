# A100 VRAM Test 29 — Workload FP32 Load and Clear
**Researcher:** Mike Bains | mikebains41@gmail.com

## Key Numbers
- Baseline GPU0 = 63.60W | GPU1 = 60.28W
- VRAM loaded = 807 MB
- Compute peak GPU0 = 359.49W | GPU1 = 337.30W
- VRAM after compute = 1,601 MB
- VRAM residual = 455 MB
- util.memory = 0% throughout (NVML lie)
- VRAM growth during compute = 794 MB

## vs B200
- A100 power drops after clear
- B200 power stays elevated after clear
- A100 residual 455MB vs B200 716MB
