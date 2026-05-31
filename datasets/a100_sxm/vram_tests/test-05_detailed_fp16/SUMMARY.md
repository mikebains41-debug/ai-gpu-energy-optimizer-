# A100_VRAM_TEST_05_DETAILED_FP16
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: RESIDUAL DETECTED

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 64.46W | 66.53W |
| VRAM Loaded | 809 MB | 84.84W | 87.48W |
| FP16 Compute | 1,229 MB | 85.44W | 88.09W |
| After Clear | **463 MB** | 85.77W | 88.41W |

## Residual Comparison
| Test | Compute | Residual |
|---|---|---|
| TEST_03 | SIGKILL | 0 MB |
| TEST_02 | Workload | 457 MB |
| TEST_04 | FP32 | 457 MB |
| TEST_05 | FP16 | **463 MB** |

## Security Issue HIGH
FP16 leaves 6 MB more than FP32. Residual tracks with precision type.
