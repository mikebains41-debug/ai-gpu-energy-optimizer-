# A100 Test 28 — VRAM Detailed Full Profile
**Date:** 2026-05-30 | **GPU:** A100 SXM 80GB x2 | **Pod:** 039fb8547a98

## Result: CRITICAL

## Phase Profile
| Phase | GPU0 Power | GPU1 Power | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 63.54W | 60.49W | 1 MB | 0% |
| VRAM Loaded | 73.04W | 69.64W | 807 MB | 0% |
| Post Compute | 73.29W | 69.64W | 1,601 MB | 0% |
| After Clear | 73.21W | 69.57W | 455 MB | 0% |

## Key Findings
1. Ghost power 60-63W from cold boot at 1MB VRAM
2. NVML reports 0% while 807MB loaded
3. VRAM grew 794MB during compute
4. 455MB residual after empty_cache
5. GPU0 consistently 3.05W higher than GPU1

## Cross-Architecture Residual
| GPU | Config | Residual |
|---|---|---|
| A100 SXM | 2x simple | 382 MB |
| A100 SXM | 2x with compute | 455 MB |
| H200 SXM | 2x | 382 MB |
| B200 | 2x | 716 MB |
