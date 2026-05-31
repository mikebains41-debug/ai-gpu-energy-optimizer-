# H200_VRAM_TEST_01_BASELINE
**Date:** 2026-05-30 | **GPU:** H200 SXM x2 | **Pod:** 6e7fb4e76def

## Result: RESIDUAL DETECTED

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 79.85W | 80.52W |
| Loaded | 911 MB | 124.5W | 129.5W |
| After Clear | **529 MB** | 127.0W | 132.0W |

## H200 vs A100 Residual
| GPU | Residual |
|---|---|
| A100 SXM | 457 MB |
| H200 SXM | **529 MB** |
| Difference | +72 MB |

## Security Issue HIGH
529 MB remains after graceful cleanup. More than A100.
H200 HBM3e leaves more data uncleared than A100 HBM2e.

## Note
util.memory = 0 pct with 911 MB loaded — H200 underreports memory utilization.
