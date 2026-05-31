# A100_MEMORY_CLOCK_TEST_03_FP16
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2

## Purpose
Measure memory and SM clocks during FP16 tensor core load.

## Key Findings
- FP16 SM clock = 1155 MHz (vs FP32 1410 MHz)
- MEM clock = 1593 MHz identical to FP32
- VRAM residual = 463 MB (6 MB more than FP32)

## Security Issue HIGH
463 MB FP16 data left after graceful cleanup.
