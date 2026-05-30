# B200 Test 09 — VRAM Residual
**Date:** 2026-05-30 | **GPU:** B200 x2 | **Pod:** 79bf58714a0c

## Result: CRITICAL

| State | GPU0 | GPU1 |
|---|---|---|
| Residual after clear | 716 MB | 716 MB |
| Power after clear | 239.25W | 235.68W |
| util.memory | 0% | 0% |

## Cross-Architecture Comparison
| GPU | Residual |
|---|---|
| A100 SXM | 382 MB |
| H200 SXM | 382 MB |
| B200 2x GPU | 716 MB |

## Conclusion
716MB residual confirmed on B200 2x GPU.
Power never drops after clear.
NVML completely blind to residual.
Security risk confirmed.
