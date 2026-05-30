# B200 Test 10 — VRAM Detailed
**Date:** 2026-05-30 | **GPU:** B200 1x | **Pod:** c61621b362d6

## Result: CRITICAL

## Phase Profile
| Phase | Power | VRAM | util.memory |
|---|---|---|---|
| Baseline | 190W | 0 MB | 0% |
| VRAM Loaded | 238W | 1,010 MB | 0% |
| Post Compute | 239W | 1,862 MB | 0% |
| After Clear | 239W | 716 MB | 0% |

## Key Findings
1. Ghost power 190W at 0MB VRAM from cold boot
2. NVML reports 0% while 1010MB loaded
3. VRAM grew 852MB during compute
4. 716MB residual after empty_cache
5. Power never drops after clear

## Cross-Architecture Residual
| GPU | Residual |
|---|---|
| A100 SXM | 382 MB |
| H200 SXM | 382 MB |
| B200 2x GPU | 628 MB |
| B200 1x GPU | 716 MB |
