# A100 VRAM Test 28 — Detailed Full Profile
**Researcher:** Mike Bains | mikebains41@gmail.com

## Key Numbers
- Baseline GPU0 = 63.54W | GPU1 = 60.49W
- VRAM loaded = 807 MB
- VRAM after compute = 1,601 MB
- VRAM residual = 455 MB
- util.memory throughout = 0% (NVML lie)
- Inter-GPU differential = 3.05W
- VRAM growth during compute = 794 MB

## vs Simple Residual Test
- Simple load + clear = 382MB residual
- Load + compute + clear = 455MB residual
- Difference = 73MB from compute buffers

## Conclusion
Residual scales with workload complexity.
NVML blind throughout all phases.
Ghost power confirmed from cold boot.
