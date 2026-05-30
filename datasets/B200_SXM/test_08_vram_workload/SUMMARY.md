# B200 Test 08 — VRAM Workload
**Date:** 2026-05-30 | **GPU:** B200 x2 | **Pod:** 79bf58714a0c

## Result: CRITICAL

## Phase Profile
| Phase | GPU0 Power | GPU1 Power | VRAM | util.memory |
|---|---|---|---|---|
| Baseline | 190.14W | 188.11W | 0 MB | 0% |
| VRAM Loaded | 238.52W | 234.97W | 1,010 MB | 0% |
| Post Compute | 239.05W | 235.63W | 1,862 MB | 0% |

## Key Findings
1. NVML reports 0% while 1010MB loaded on both GPUs
2. VRAM grew 852MB during compute
3. Power stays elevated after compute
4. GPU0 consistently 3.42W higher than GPU1

## Conclusion
NVML memory desync confirmed on B200 2x GPU.
VRAM grows during compute and does not clear.
