# B200_VRAM_TEST_01_BASELINE
**Date:** 2026-05-30 | **GPU:** B200 SXM x2

## Purpose
Establish B200 VRAM baseline and measure residual after graceful cleanup.

## Key Findings
- VRAM total: 183,359 MB per GPU
- Baseline: 0 MB
- After load: 1,010 MB
- After cleanup: 628 MB residual
- Power never returns to 144W baseline — stuck at 197W

## Security Issues
1. HIGH: 628 MB uncleared after graceful exit
2. HIGH: Power permanently elevated +52W above baseline
