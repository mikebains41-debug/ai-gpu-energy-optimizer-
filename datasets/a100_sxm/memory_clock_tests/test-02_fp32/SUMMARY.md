# A100_MEMORY_CLOCK_TEST_02_FP32
**Date:** 2026-05-30 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: RESIDUAL DETECTED

| Phase | VRAM | SM Clock | MEM Clock | Power |
|---|---|---|---|---|
| Baseline | 0 MB | 210 MHz | **1593 MHz** | 65.73W |
| FP32 Load | 1,603 MB | 1410 MHz | **1593 MHz** | 367.89W |
| Post Load | 1,603 MB | 1155 MHz | **1593 MHz** | 88.87W |
| After Clear | 457 MB | 1155 MHz | **1593 MHz** | 86.13W |

## Key Finding
MEM clock = 1593 MHz across ALL phases. Never changes.
SM clock changes with workload. MEM clock does not.

## Security Issue HIGH
457 MB FP32 data remains after graceful cleanup.
