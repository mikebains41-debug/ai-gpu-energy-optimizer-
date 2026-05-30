# B200 Test 08 — VRAM Workload
**Date:** 2026-05-30 | **GPU:** B200 x2

## Result: CRITICAL

| Phase | memory.used | util.memory | Power |
|---|---|---|---|
| Idle | 0 MB | 0% | 146W |
| Loaded | 1,010 MB | 0% | 198-206W |
| After clear | 628 MB | 0% | 198-206W |

## Key Findings
1. NVML reports 0% while 1010MB loaded
2. 382MB residual after empty_cache
3. Power stays elevated at 198-206W after clear — unlike A100
