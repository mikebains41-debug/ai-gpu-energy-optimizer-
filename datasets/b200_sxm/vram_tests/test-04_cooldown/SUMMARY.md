# B200_VRAM_TEST_04_COOLDOWN
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: POWER AND VRAM STUCK POST-LOAD

| Phase | VRAM | GPU0 | GPU1 | Util |
|---|---|---|---|---|
| Baseline | 0 MB | 144.38W | 148.52W | 0 pct |
| FP32 Load | 1,874 MB | 549.76W | - | - |
| Cooldown Start | 728 MB | **684.71W** | **700.74W** | **48 pct** |
| Cooldown Done | 728 MB | 196W | 202W | 0 pct |
| Post Cooldown | 728 MB | 196W | 202W | 0 pct |

## Key Finding
B200 has NO recovery path. Power never returns to 144W baseline.
Unlike A100 which oscillates between State 1 and State 2.

## Security Issues
1. HIGH: 728 MB permanent VRAM residual
2. HIGH: +52W permanent power elevation — no recovery state
