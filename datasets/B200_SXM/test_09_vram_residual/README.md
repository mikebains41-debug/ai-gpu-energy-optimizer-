# B200 VRAM Test 09 — Residual
**Researcher:** Mike Bains | mikebains41@gmail.com

## Key Numbers
- Residual GPU0 = 382 MB
- Residual GPU1 = 382 MB
- A100 residual = 382 MB
- B200 residual = 382 MB

## Critical Finding
Identical 382MB residual across A100 and B200.
This is CUDA runtime level — not GPU architecture specific.
Affects all NVIDIA GPUs using CUDA.
