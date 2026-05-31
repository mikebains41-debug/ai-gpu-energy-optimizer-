# B200_VRAM_TEST_05_POST_LOAD_GHOST
**Date:** 2026-05-30 | **GPU:** B200 SXM x2

## Purpose
Monitor ghost power for 600s after FP32 load exits.

## Critical Findings
- Ghost spike: 549.84W GPU0 + 574.84W GPU1 at 0 pct util
- Exceeds A100 max desync (357W) by 217W
- NVML completely blind — reports 0 pct util throughout
- 728 MB VRAM permanent for 600 seconds

## Security Issues
1. CRITICAL: 549-574W ghost spike — NVML cannot detect
2. HIGH: NVML blind — all conventional monitoring useless on B200
3. HIGH: 728 MB permanent VRAM residual
