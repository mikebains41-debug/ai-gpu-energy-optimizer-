# H200 VRAM TEST 04 - DETAILED FP16 - SUMMARY
**Date:** 2026-05-31 | **GPU:** H200 SXM 141GB x2 | **Researcher:** Mike Bains

## Phase Results
| Phase | GPU0 | GPU1 | VRAM | SM Clock |
|-------|------|------|------|----------|
| Baseline | 73.92W | 76.38W | 1 MB | 345 MHz |
| FP16 Loaded | 113.51W | 114.86W | 1,040 MB | 1,980 MHz |
| FP16 Compute | 694W | 694W | 2,166 MB | 1,380-1,425 MHz |
| Cooldown | 115-120W | 115-120W | 2,166 MB | 1,980 MHz |
| After Clear | 120W | 120W | 630 MB | 1,980 MHz |

## Security Issues
| Severity | Issue |
|----------|-------|
| HIGH | 630 MB FP16 data readable by next tenant |
| HIGH | NVML util.memory = 0% - infrastructure blind |
| MEDIUM | Ghost power 120W vs 74W baseline |
| MEDIUM | SM clock 1,980 MHz post-clear vs 345 MHz |
