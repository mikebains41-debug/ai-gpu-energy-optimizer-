# B200_VRAM_TEST_02_FP32_LOAD
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: RESIDUAL DETECTED + ANOMALOUS COOLDOWN

| Phase | VRAM | GPU0 | GPU1 | Util |
|---|---|---|---|---|
| Baseline | 0 MB | 144.49W | 148.40W | 0 pct |
| FP32 Load | 1,874 MB | 549.76W | 542.02W | - |
| Cooldown Start | 728 MB | **684.71W** | **700.74W** | **45-48 pct** |
| Cooldown Done | 728 MB | 196W | 202W | 0 pct |

## Security Issue 1 HIGH — VRAM Residual
728 MB FP32 data remains. 271 MB more than A100.

## Security Issue 2 HIGH — Anomalous Cooldown Spike
684-700W at only 45-48 pct util during cooldown.
Normal compute = 100 pct util. This is undocumented background activity.

## Power Never Recovers
- Baseline: 144.49W
- Post-clear: 196W
- Elevation: +51.5W permanent
