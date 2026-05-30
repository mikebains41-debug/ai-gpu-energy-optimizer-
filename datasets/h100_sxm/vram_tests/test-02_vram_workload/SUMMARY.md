# H100 Test 02 — VRAM Workload FP32
**Date:** 2026-05-30 | **GPU:** H100 SXM x2

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 77.79W | 75.60W | 0 MB | 0% |
| VRAM Loaded | 114.92W | 113.48W | 909 MB | 0% |
| Post Compute | 114.63W | 113.21W | 1,771 MB | 0% |
| After Clear | 118.73W | 117.26W | 625 MB | 0% |

## Conclusion
625MB residual. NVML blind. Power stays elevated.
