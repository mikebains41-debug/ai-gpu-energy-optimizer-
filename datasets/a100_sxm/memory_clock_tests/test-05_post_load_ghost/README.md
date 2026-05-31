# A100_MEMORY_CLOCK_TEST_05_POST_LOAD_GHOST
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2

## Purpose
Heavy FP16 load then 300 second ghost monitoring.

## Key Findings
- Peak: 416.19W at 100pct util (16384x16384 FP16)
- Ghost State 2: SM 1155 MHz, 86W, 0pct util for 300s after load
- MEM clock: 1593 MHz throughout
- VRAM residual: 463 MB permanent until pod restart

## Security Issue HIGH
463 MB heavy FP16 tensor data. Permanent for 5 minutes confirmed.
