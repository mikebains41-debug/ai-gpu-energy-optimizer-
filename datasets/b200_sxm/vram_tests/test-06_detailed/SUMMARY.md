# B200_VRAM_TEST_06_DETAILED_FULL_PROFILE
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: RESIDUAL + POWER STUCK + NVML BLIND

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 144.76W | 148.55W |
| VRAM Loaded | 1,010 MB | 196W | 201W |
| Post Compute | 1,874 MB | 197W | 202W |
| After Clear | **728 MB** | 196.5W | 202W |

## Complete Residual Comparison
| GPU | HBM | Residual |
|---|---|---|
| A100 SXM | HBM2e | 457-465 MB |
| H200 SXM | HBM3e | 529-629 MB |
| B200 SXM | HBM3e | **728 MB fixed** |

B200 residual is fixed at 728 MB regardless of compute type.
A100 varies by dtype. B200 does not.

## Security Issues
1. HIGH: 728 MB fixed residual — does not vary with compute type
2. HIGH: Power never returns to 144W baseline — stuck at 196-202W permanently
3. HIGH: NVML blind throughout — DCGM Datadog Prometheus all ineffective on B200

## Conclusion
B200 is the highest-risk architecture across all 3 security dimensions:
VRAM residual, power anomaly, and monitoring blindness.
