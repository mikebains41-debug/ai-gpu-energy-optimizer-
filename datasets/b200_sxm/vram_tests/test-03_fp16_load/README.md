# B200_VRAM_TEST_03_FP16_LOAD
**Date:** 2026-05-30 | **GPU:** B200 SXM x2

## Purpose
FP16 tensor core load with cooldown. Measure VRAM residual vs FP32.

## Key Finding
726 MB residual — nearly same as FP32 728 MB.
B200 residual is NOT precision-dependent.

## Security Issue HIGH
726 MB FP16 data left after cleanup.
269 MB more than A100 FP16 residual.
