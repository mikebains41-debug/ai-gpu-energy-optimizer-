# H200 VRAM TEST 05 - DETAILED FP16 - SUMMARY
**Date:** 2026-05-31 | **GPU:** H200 SXM 141GB x2 | **Researcher:** Mike Bains

## Phase Results
| Phase | GPU0 | GPU1 | VRAM | SM Clock |
|-------|------|------|------|----------|
| Baseline | 75.21W | 72.22W | 1 MB | 345 MHz |
| FP16 Alloc | 79.77W | 72.22W | 912 MB | 1,980 MHz |
| FP16 Compute | 157.82W | 72.22W | 6,006 MB | 1,980 MHz |
| After Clear | 116-119W | 72.22W | 628 MB | 1,980 MHz |

## Security Issues
| Severity | Issue |
|----------|-------|
| HIGH | 628 MB FP16 data readable by next tenant |
| HIGH | NVML util.memory = 0% - infrastructure blind |
| MEDIUM | Ghost power 119W vs 75W baseline |
| MEDIUM | SM clock 1,980 MHz post-clear vs 345 MHz |
