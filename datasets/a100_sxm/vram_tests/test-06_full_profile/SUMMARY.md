# A100_VRAM_TEST_06_DETAILED_FULL_PROFILE
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: RESIDUAL DETECTED + ASYMMETRIC LOAD

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 64.14W | 66.27W |
| VRAM Loaded | 809 MB | 84.51W | 87.21W |
| FP32 Peak | 19,939 MB | 356.39W 100pct | 7.48W |
| FP16 Peak | 19,947 MB | 112.21W | 88.50W |
| After Clear | **465 MB** | 85.44W | 88.68W |

## Security Issue 1 HIGH
465 MB mixed-precision data left. Highest residual across all tests.

## Security Issue 2 MEDIUM
Asymmetric load — FP32 ran only on GPU0. GPU1 near idle at 7.48W.

## Full Residual Table
| Test | Compute | Residual |
|---|---|---|
| TEST_03 | SIGKILL | 0 MB |
| TEST_02 | Workload | 457 MB |
| TEST_04 | FP32 | 457 MB |
| TEST_05 | FP16 | 463 MB |
| TEST_06 | FP32+FP16 | **465 MB** |
