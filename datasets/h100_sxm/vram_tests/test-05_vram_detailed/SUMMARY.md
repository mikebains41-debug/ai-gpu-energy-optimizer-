# H100 Test 05 — VRAM Detailed Full Profile
**Date:** 2026-05-30 | **GPU:** H100 SXM x2

## Result: CRITICAL

## Phase Profile
| Phase | GPU0 Power | GPU1 Power | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 77.65W | 75.54W | 0 MB | 0% |
| VRAM Loaded | 119.08W | 117.54W | 909 MB | 0% |
| Post Compute | 114.65W | 113.55W | 1,771 MB | 0% |
| After Clear | 114.62W | 113.16W | 625 MB | 0% |

## Key Findings
1. Ghost power 75-78W at 0MB VRAM
2. NVML reports 0% while 909MB loaded
3. VRAM grew 862MB during compute
4. 625MB residual after empty_cache
5. Power stays at 114W after clear

## Cross-Architecture Residual
| GPU | Residual |
|---|---|
| A100 SXM | 455 MB |
| H100 SXM | 625 MB |
| H200 SXM | 382 MB |
| B200 | 716 MB |
