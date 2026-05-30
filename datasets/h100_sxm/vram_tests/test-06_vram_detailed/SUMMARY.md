# H100 Test 06 — VRAM Detailed Full Profile
**Date:** 2026-05-30 | **GPU:** H100 SXM x2

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 78.11W | 75.99W | 0 MB | 0% |
| VRAM Loaded | 115.15W | 113.72W | 909 MB | 0% |
| Post Compute | 119.23W | 117.63W | 1,771 MB | 0% |
| After Clear | 119.06W | 117.50W | 625 MB | 0% |

## Key Findings
1. Ghost power 75-78W at 0MB VRAM
2. NVML reports 0% while 909MB loaded
3. VRAM grew 862MB during compute
4. 625MB residual after empty_cache
5. Power stays at 119W after clear

## Cross-Architecture Residual
| GPU | Residual |
|---|---|
| A100 SXM | 455 MB |
| H100 SXM | 625 MB |
| H200 SXM | 629 MB |
| B200 | 716 MB |
