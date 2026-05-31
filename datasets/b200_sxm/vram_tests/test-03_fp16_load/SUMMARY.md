# B200_VRAM_TEST_03_FP16_LOAD
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: RESIDUAL DETECTED

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 144.61W | 148.45W |
| FP16 Load | 1,302 MB | 196.51W | 201.59W |
| Cooldown | **726 MB** | 196.82W | 202.33W |

## B200 FP16 vs FP32 Residual
| Compute | B200 Residual |
|---|---|
| FP32 | 728 MB |
| FP16 | **726 MB** |

Nearly identical — B200 residual NOT precision-dependent. Unlike A100 (457 vs 463 MB).

## Security Issue HIGH
726 MB FP16 data uncleared. 269 MB more than A100 FP16.
