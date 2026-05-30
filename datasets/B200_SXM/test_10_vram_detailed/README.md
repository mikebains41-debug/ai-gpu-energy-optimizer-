# B200 VRAM Test 10 — Detailed
**Researcher:** Mike Bains | mikebains41@gmail.com

## What This Proves
B200 VRAM residual is 716MB — larger than A100 and H200.
Power never drops after VRAM clear.
NVML blind to all memory states.

## New Findings
- VRAM grows during compute: 1010MB to 1862MB
- Residual varies by GPU count: 1x=716MB 2x=628MB
- B200 power floor 190W — higher than A100 65W
- Power stays at 239W after clear — no recovery

## Conclusion
382MB residual is NOT universal.
B200 shows larger residual than A100 and H200.
CUDA context size varies by architecture and GPU count.
