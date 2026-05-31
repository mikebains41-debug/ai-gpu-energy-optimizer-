# H200 VRAM Test 05 - Detailed FP16
**Researcher:** Mike Bains | mikebains41@gmail.com
**Date:** 2026-05-31
**GPU:** NVIDIA H200 SXM 141GB x2 | **Provider:** RunPod

## Key Numbers
- Baseline GPU0 = 75.21W | GPU1 = 72.22W
- VRAM loaded = 1 MB cold start
- VRAM during FP16 = 6,006 MB
- VRAM residual = 628 MB
- util.memory = 0% throughout (NVML lie)
- VRAM growth during compute = 6,005 MB
- FP16 peak power GPU0 = 157.82W
- SM clock during compute = 1,980 MHz
- Power after clear = 116-119W stays elevated
- Memory clock = 3,201 MHz locked all phases

## Conclusion
H200 FP16 residual 628MB confirmed.
Power never returns to baseline after clear (75W to 119W).
NVML blind throughout all phases.
