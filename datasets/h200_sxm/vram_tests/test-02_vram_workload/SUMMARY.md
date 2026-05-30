# H200 Test 02 — VRAM Workload
**Date:** 2026-05-30 | **GPU:** H200 SXM x2

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 79.85W | 80.97W | 0 MB | 0% |
| VRAM Loaded | 125.06W | 128.08W | 2,055 MB | 0% |
| Compute | 700.34W | 699.66W | 5,207 MB | 23% |
| Post Compute | 137.25W | 698W | 5,207 MB | 0% |

## Key Finding
H200 util.memory shows 20-23% during compute.
More honest than A100 and B200 which report 0%.
VRAM grew 3,152MB during compute.
