# H100 Test 01 — VRAM Baseline
**Date:** 2026-05-30 | **GPU:** H100 SXM x2

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 78.09W | 75.82W | 0 MB | 0% |
| VRAM Loaded | 120.27W | 118.41W | 909 MB | 0% |
| After Clear | 119.61W | 118.33W | 527 MB | 0% |

## Conclusion
527MB residual. NVML blind. Power stays elevated.
