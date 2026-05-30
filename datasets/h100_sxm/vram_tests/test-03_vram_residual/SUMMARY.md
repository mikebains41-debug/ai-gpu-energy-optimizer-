# H100 Test 03 — VRAM Residual
**Date:** 2026-05-30 | **GPU:** H100 SXM x2

## Result: CRITICAL

| State | GPU0 | GPU1 |
|---|---|---|
| Residual after clear | 625 MB | 625 MB |
| Power after clear | 115.99W | 114.59W |
| util.memory | 0% | 0% |

## Cross-Architecture Residual
| GPU | Residual |
|---|---|
| A100 SXM | 455 MB |
| H100 SXM | 625 MB |
| H200 SXM | 382 MB |
| B200 | 716 MB |

## Conclusion
625MB residual confirmed. NVML blind. Power stays elevated.
