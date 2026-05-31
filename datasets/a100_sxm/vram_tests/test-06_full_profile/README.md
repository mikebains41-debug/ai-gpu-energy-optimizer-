# A100_VRAM_TEST_06_DETAILED_FULL_PROFILE
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2

## Purpose
Full profile — FP32 compute, FP16 compute, ghost monitor, clear, residual check.

## Key Findings
- FP32 peak: 356.39W GPU0 100pct — GPU1 7.48W asymmetric
- FP16 peak: 112.21W
- Peak VRAM: 19,947 MB
- After cleanup: 465 MB residual

## Security Issues
1. HIGH: 465 MB mixed-precision data left after graceful exit
2. MEDIUM: Asymmetric load — FP32 ran only on GPU0

## Pattern
More compute = more VRAM residual. SIGKILL = only safe method.
