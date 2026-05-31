# B200_VRAM_TEST_06_DETAILED_FULL_PROFILE
**Date:** 2026-05-30 | **GPU:** B200 SXM x2

## Purpose
Full profile — load, compute, ghost monitor, clear, residual check.

## Key Findings
- Load: 1,010 MB
- Post compute: 1,874 MB
- After cleanup: 728 MB fixed residual
- Power: never drops to 144W baseline
- NVML: blind throughout

## Security Issues
1. HIGH: 728 MB fixed residual regardless of compute type
2. HIGH: +52W permanent power elevation
3. HIGH: NVML completely blind on B200
