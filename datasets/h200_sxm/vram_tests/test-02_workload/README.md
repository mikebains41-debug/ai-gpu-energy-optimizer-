# H200_VRAM_TEST_02_WORKLOAD
**Date:** 2026-05-30 | **GPU:** H200 SXM x2

## Purpose
Load VRAM, run matmul compute, gracefully clear, measure residual.

## Key Findings
- Load: 2,055 MB
- Compute peak: 698W at 100 pct util, 5,207 MB
- After cleanup: 629 MB residual
- 172 MB more than A100

## Security Issue HIGH
629 MB — highest residual across all tested architectures.
HBM3e retains more data than HBM2e after graceful exit.
