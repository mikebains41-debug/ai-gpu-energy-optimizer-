# H200 VRAM Test 04 - Detailed FP16
**Researcher:** Mike Bains | mikebains41@gmail.com
**Date:** 2026-05-31
**GPU:** NVIDIA H200 SXM 141GB x2 | **Provider:** RunPod

## Key Numbers
- Baseline GPU0 = 73.92W | GPU1 = 76.38W
- VRAM loaded = 1,040 MB
- VRAM after compute = 2,166 MB
- VRAM residual = 630 MB
- util.memory = 0% throughout (NVML lie)
- VRAM growth during compute = 1,126 MB
- FP16 peak power = 694W both GPUs
- Power after clear = 120W stays elevated
- Memory clock = 3,201 MHz locked all phases

## Conclusion
H200 FP16 residual 630MB confirmed.
Power never returns to baseline after clear (74W to 120W).
NVML blind throughout all phases.
