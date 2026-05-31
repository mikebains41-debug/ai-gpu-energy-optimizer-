# B200_VRAM_TEST_01_BASELINE
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: RESIDUAL DETECTED

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 144.50W | 149.76W |
| Loaded | 1,010 MB | 196.5W | 201.5W |
| After Clear | **628 MB** | 197.0W | 202.0W |

## Cross-Architecture Residual
| GPU | HBM | Residual |
|---|---|---|
| A100 SXM | HBM2e | 457 MB |
| H200 SXM | HBM3e | 529 MB |
| B200 SXM | HBM3e | **628 MB** |

## Security Issues
### 1. HIGH — VRAM Residual
628 MB remains after graceful cleanup. Highest residual of all tested architectures.

### 2. HIGH — Power Never Returns to Baseline
- Baseline: 144.50W
- Post-clear: 197.0W
- Elevation: +52.5W permanent

## Conclusion
B200 VRAM residual = 628 MB. Power never recovers. HBM state stuck post-load.
