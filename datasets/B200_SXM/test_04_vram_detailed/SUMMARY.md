# B200 Test 04 — VRAM Detailed
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** 79bf58714a0c

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 190.05W | 187.94W | 0 MB | 0% |
| VRAM Loaded | 238.77W | 234.93W | 1,010 MB | 0% |
| Post Compute | 239.39W | 235.74W | 1,862 MB | 0% |
| After Clear | 239.25W | 235.68W | 716 MB | 0% |

## Key Findings
1. Ghost power 188-190W at 0MB VRAM
2. NVML reports 0% while 1010MB loaded
3. VRAM grew 852MB during compute
4. 716MB residual after empty_cache
5. Power never drops after clear
