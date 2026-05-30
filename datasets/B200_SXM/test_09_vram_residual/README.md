# B200 VRAM Test 09 — Residual
**Researcher:** Mike Bains | mikebains41@gmail.com

## Key Numbers
- Residual GPU0 = 716 MB
- Residual GPU1 = 716 MB
- Power GPU0 after clear = 239.25W
- Power GPU1 after clear = 235.68W
- util.memory = 0% (NVML blind)
- Baseline power = 190W
- Power never returned to baseline

## Critical Finding
B200 residual 716MB is nearly double A100 and H200 382MB.
Security risk scales with GPU architecture generation.
