# B200 Test 03 — FP16 Load
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM |
|---|---|---|---|
| Baseline | 144.61W | 149.23W | 0 MB |
| FP16 Peak | 196.72W | 202.27W | 1,302 MB |
| Cooldown | 197.01W | 202.31W | 726 MB |

## FP32 vs FP16
| Type | Peak Power | Ratio |
|---|---|---|
| FP32 | 549.76W | 2.79x |
| FP16 | 196.72W | 1x |

## Conclusion
FP16 peak 197W. FP32 draws 2.79x more power. Power never returns to baseline.
