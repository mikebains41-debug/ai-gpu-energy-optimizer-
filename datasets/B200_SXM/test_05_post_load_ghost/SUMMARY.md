# B200 Test 05 — Post Load Ghost Power Persistence
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: CRITICAL

| Phase | GPU0 | GPU1 | VRAM |
|---|---|---|---|
| Baseline | 144.32W | 149.38W | 0 MB |
| FP32 Peak | 549.84W | 574.91W | 728 MB |
| Ghost 10 min | 197.09W | 203.29W | 728 MB |

## Conclusion
Ghost power 197-203W persists for 10+ minutes after load. Never returns to 144W baseline. 728MB VRAM stuck.
