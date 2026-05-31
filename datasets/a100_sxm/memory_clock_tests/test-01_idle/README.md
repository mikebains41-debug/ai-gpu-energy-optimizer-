# A100_MEMORY_CLOCK_TEST_01_IDLE
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2

## Purpose
Measure memory clock at idle with no tensors loaded.

## Key Finding
MEM clock = 1593 MHz at idle. Locked. Never reduces.
SM clock = 210 MHz. pstate = P0.

## Conclusion
HBM subsystem locked at full clock speed 24/7 regardless of VRAM usage.
