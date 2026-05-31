# A100_MEMORY_CLOCK_TEST_01_IDLE
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: PASS

| Metric | GPU0 | GPU1 |
|---|---|---|
| SM Clock | 210 MHz | 210 MHz |
| MEM Clock | **1593 MHz** | **1593 MHz** |
| pstate | P0 | P0 |
| VRAM used | 0 MB | 0 MB |
| Power | 65.73W | 68.12W |

## Key Finding
HBM memory clock = 1593 MHz with 0 MB VRAM used. Locked at full speed.

## Security Issues
None.

## Conclusion
Root cause of ghost power: HBM subsystem active at 1593 MHz with nothing to process.
