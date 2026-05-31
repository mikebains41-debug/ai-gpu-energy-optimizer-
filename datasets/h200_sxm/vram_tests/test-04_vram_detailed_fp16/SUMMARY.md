# A100_VRAM_TEST_06_DETAILED_FULL_PROFILE
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: RESIDUAL DETECTED + ASYMMETRIC LOAD ⚠️

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 64.14W | 66.27W |
| VRAM Loaded | 809 MB | 84.51W | 87.21W |
| FP32 Peak | 19,939 MB | **356.39W 100%** | 7.48W |
| Post FP32 | 19,939 MB | 85.77W | 87.57W |
| FP16 Peak | 19,947 MB | 112.21W | 88.50W |
| After Clear | **465 MB** | 85.44W | 88.68W |

## Complete Residual Summary
| Test | Compute | Residual |
|---|---|---|
| TEST_03 | SIGKILL | 0 MB ✅ |
| TEST_02 | Workload | 457 MB ⚠️ |
| TEST_04 | FP32 | 457 MB ⚠️ |
| TEST_05 | FP16 | 463 MB ⚠️ |
| TEST_06 | FP32 + FP16 | **465 MB** ⚠️ |

## Security Issues

### 1. VRAM Residual — HIGH ⚠️
465 MB mixed-precision data left after graceful cleanup.
Most data exposed across all tests. Full model weights readable by next tenant.

### 2. Asymmetric GPU Load — MEDIUM ⚠️
FP32 ran entirely on GPU0 (356W, 100%) — GPU1 at 7.48W.
Workload not distributed. Potential scheduling issue.

## Conclusion
More compute = more VRAM residual. SIGKILL remains the only safe cleanup method.
