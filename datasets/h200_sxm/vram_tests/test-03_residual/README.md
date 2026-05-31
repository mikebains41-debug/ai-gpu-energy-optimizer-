# H200_VRAM_TEST_03_RESIDUAL
**Date:** 2026-05-30 | **GPU:** H200 SXM x2

## Purpose
Compute workload then monitor VRAM still loaded, clear, check residual.

## Key Findings
- Compute peak: 696W, 5,207 MB
- Post-compute with VRAM loaded: 136W at 0 pct util
- After clear: 629 MB residual permanent
- Ghost power state 2 confirmed: +56W above baseline

## Security Issues
1. HIGH: 629 MB data left after graceful exit
2. MEDIUM: Ghost power state 2 — power 56W above baseline permanently
