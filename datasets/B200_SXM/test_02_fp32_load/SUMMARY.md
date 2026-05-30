# B200 Test 02 — FP32 Load
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM |
|---|---|---|---|
| Baseline | 144.40W | 148.17W | 0 MB |
| FP32 Peak | 549.76W | 542.02W | 1,874 MB |
| Post Load | 196.60W | 202.69W | 1,874 MB |
| Cooldown | 196.73W | 202.76W | 728 MB |

## Conclusion
FP32 peak 549W. Power never returns to baseline. NVML blind throughout.
