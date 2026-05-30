# H100 VRAM Test 05 — Detailed Full Profile
**Researcher:** Mike Bains | mikebains41@gmail.com

## Key Numbers
- Baseline GPU0 = 77.65W | GPU1 = 75.54W
- VRAM loaded = 909 MB
- VRAM after compute = 1,771 MB
- VRAM residual = 625 MB
- util.memory = 0% throughout (NVML lie)
- VRAM growth during compute = 862 MB
- Power after clear = 114W stays elevated

## Conclusion
H100 VRAM residual 625MB confirmed.
Power never returns to baseline after clear.
NVML blind throughout all phases.
