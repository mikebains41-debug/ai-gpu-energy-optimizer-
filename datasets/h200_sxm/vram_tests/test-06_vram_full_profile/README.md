# H200 VRAM Test 06 - Detailed Full Profile
**Researcher:** Mike Bains | mikebains41@gmail.com
**Date:** 2026-05-31
**GPU:** NVIDIA H200 SXM 141GB x2 | **Provider:** RunPod

## Key Numbers
- Baseline GPU0 = 74.41W | GPU1 = 72.51W
- VRAM loaded GPU0 = 18,168 MB | GPU1 = 910 MB
- FP32 peak GPU0 = 653W | GPU1 = 115W
- FP32 VRAM = 19,030 MB
- FP16 VRAM = 19,162 MB
- VRAM residual GPU0 = 1,102 MB | GPU1 = 528 MB
- Total residual = 1,630 MB
- util.memory = 0% throughout (NVML lie)
- Power after clear = 119W stays elevated

## Conclusion
H200 full profile leaves 1,630 MB total VRAM residual.
Cross-GPU isolation failure - GPU1 retains 528 MB without running compute.
Power never returns to baseline after clear (74W to 119W).
NVML blind throughout all phases.
