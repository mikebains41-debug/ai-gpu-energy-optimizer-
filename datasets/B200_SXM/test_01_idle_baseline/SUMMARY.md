# B200 Test 01 — Extended Idle Baseline
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: CRITICAL

| Metric | GPU0 | GPU1 |
|---|---|---|
| Ghost power | 144.40W | 149.12W |
| Combined | 293W | - |
| VRAM | 0 MB | 0 MB |
| util.gpu | 0% | 0% |
| Duration | 10 min | 10 min |

## Conclusion
B200 draws 293W combined at idle. GPU1 4-5W higher than GPU0. NVML blind throughout.
