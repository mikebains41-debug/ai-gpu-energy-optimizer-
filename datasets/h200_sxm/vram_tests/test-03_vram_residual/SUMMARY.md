# H200 Test 03 — VRAM Residual
**Date:** 2026-05-30 | **GPU:** H200 SXM x2

## Result: CRITICAL

| State | GPU0 | GPU1 |
|---|---|---|
| Residual after clear | 629 MB | 629 MB |
| Power after clear | 129.79W | 133.96W |
| util.memory | 0% | 0% |

## Cross-Architecture Residual
| GPU | Residual |
|---|---|
| A100 SXM | 455 MB |
| H100 SXM | 625 MB |
| H200 SXM | 629 MB |
| B200 | 716 MB |

## Conclusion
629MB residual confirmed. NVML blind. Power stays elevated.
