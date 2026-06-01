# A100 Test 28 — VRAM Workload FP32 Load and Clear
**Date:** 2026-05-30 | **GPU:** A100 SXM 80GB x2 | **Pod:** 039fb8547a98

## Result: CRITICAL

## Phase Profile
| Phase | GPU0 Power | GPU1 Power | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 63.60W | 60.28W | 1 MB | 0% |
| VRAM Loaded | 73.21W | 69.57W | 807 MB | 0% |
| Compute | 359.49W | 337.30W | 1,601 MB | 9% |
| Post Compute | 73.21W | 69.57W | 1,601 MB | 0% |
| After Clear | 73.29W | 69.64W | 455 MB | 0% |

## Key Findings
1. NVML reports 0% while 807MB loaded
2. FP32 compute peak 359W GPU0 337W GPU1
3. VRAM grew 794MB during compute
4. 455MB residual after empty_cache
5. Power drops after clear unlike B200
