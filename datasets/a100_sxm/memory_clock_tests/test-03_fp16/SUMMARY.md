# A100_MEMORY_CLOCK_TEST_03_FP16
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: RESIDUAL DETECTED

| Phase | VRAM | SM Clock | MEM Clock | Power |
|---|---|---|---|---|
| Baseline | 0 MB | 210 MHz | **1593 MHz** | 65.46W |
| FP16 Load | 1,039 MB | 1155 MHz | **1593 MHz** | 85.77W |
| After Clear | 463 MB | 1155 MHz | **1593 MHz** | 86.04W |

## FP16 vs FP32
| Compute | SM Peak | MEM Clock | Residual |
|---|---|---|---|
| FP32 | 1410 MHz | 1593 MHz | 457 MB |
| FP16 | 1155 MHz | 1593 MHz | 463 MB |

## Security Issue HIGH
463 MB FP16 residual — 6 MB more than FP32.
