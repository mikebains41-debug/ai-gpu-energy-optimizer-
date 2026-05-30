# B200 Test 09 — VRAM Residual
**Date:** 2026-05-30 | **GPU:** B200 x2

## Result: CRITICAL

| State | GPU0 | GPU1 |
|---|---|---|
| Loaded | 1,010 MB | 1,010 MB |
| After clear | 628 MB | 628 MB |
| Residual | 382 MB | 382 MB |

## Cross-Architecture Finding
A100 SXM residual: 382 MB
B200 residual: 382 MB
Identical — CUDA runtime level not architecture specific.
