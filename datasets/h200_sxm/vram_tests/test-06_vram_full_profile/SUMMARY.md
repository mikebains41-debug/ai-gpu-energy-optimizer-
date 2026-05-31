# H200 VRAM TEST 06 - FULL PROFILE - SUMMARY
**Date:** 2026-05-31 | **GPU:** H200 SXM 141GB x2 | **Researcher:** Mike Bains

## Phase Results
| Phase | GPU0 | GPU1 | VRAM GPU0 | VRAM GPU1 |
|-------|------|------|-----------|----------|
| Baseline | 74.41W | 72.51W | 1 MB | 1 MB |
| VRAM Loaded | 118.38W | 115.21W | 18,168 MB | 910 MB |
| FP32 Compute | 653W | 115W | 19,030 MB | 910 MB |
| Post FP32 | 120W | 115W | 19,030 MB | 910 MB |
| FP16 Done | 117W | 115W | 19,162 MB | 910 MB |
| After Clear | 119W | 115W | 1,102 MB | 528 MB |

## Security Issues
| Severity | Issue |
|----------|-------|
| CRITICAL | 1,630 MB total residual after standard cleanup |
| CRITICAL | NVML blind at 19 GB - util.memory = 0% |
| HIGH | Cross-GPU isolation failure - GPU1 528 MB no compute |
| HIGH | False clear signal - app exits 0, 1.6 GB exposed |
| HIGH | Residual scales with compute - full profile 2.6x single |
| MEDIUM | FP16 phase invisible - completes under 10s poll |
| MEDIUM | Ghost power 119W vs 74W baseline |
