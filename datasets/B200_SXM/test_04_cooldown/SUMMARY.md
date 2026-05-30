# B200 Test 04 — Cooldown Profile
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM |
|---|---|---|---|
| Baseline | 144.38W | 149.30W | 0 MB |
| FP32 Peak | 684.71W | 700.74W | 728 MB |
| Cooldown Start | 197.34W | 203.17W | 728 MB |
| After 5 Min | 196.68W | 202.18W | 728 MB |

## Conclusion
Power never returns to 144W baseline after 5 minute cooldown. 728MB VRAM stuck.
