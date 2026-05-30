# H200 Test 01 — VRAM Baseline
**Date:** 2026-05-30 | **GPU:** H200 SXM x2 | **Pod:** e6e7fb4e76def

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 79.85W | 80.52W | 0 MB | 0% |
| VRAM Loaded | 125.04W | 129.50W | 911 MB | 0% |
| After Clear | 127.00W | 132.00W | 529 MB | 0% |

## Conclusion
529MB residual. NVML blind. Power stays elevated.
