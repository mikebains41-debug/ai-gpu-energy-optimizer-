# B200_VRAM_TEST_02_FP32_LOAD
**Date:** 2026-05-30 | **GPU:** B200 SXM x2

## Purpose
FP32 matmul load with cooldown monitoring. Measure VRAM residual.

## Key Findings
- FP32 peak: 549-684W
- Anomalous cooldown: 684-700W at 45-48 pct util (not 100 pct)
- VRAM residual: 728 MB
- Power never returns to baseline

## Security Issues
1. HIGH: 728 MB FP32 data uncleared
2. HIGH: 684-700W at sub-100 pct util — undocumented background activity
