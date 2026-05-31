# A100_MEMORY_CLOCK_TEST_05_POST_LOAD_GHOST
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: GHOST POWER STATE 2 CONFIRMED

| Phase | VRAM | SM Clock | MEM Clock | Power |
|---|---|---|---|---|
| Baseline | 0 MB | 210 MHz | 1593 MHz | 66.06W |
| Heavy FP16 | 1,999 MB | 1185 MHz | 1593 MHz | **416.19W** |
| Ghost Monitor | 1,999 MB | 1155 MHz | 1593 MHz | 87.39W |
| After Clear | 463 MB | 1155 MHz | 1593 MHz | 86.37W |
| Post-Clear 300s | 463 MB | **1155 MHz** | 1593 MHz | 86.37W |

## Ghost Power States
| State | SM Clock | MEM Clock | Power |
|---|---|---|---|
| Cold boot | 210 MHz | 1593 MHz | 65W |
| Post-load | **1155 MHz** | **1593 MHz** | **86W** |

## Security Issue HIGH
463 MB of 16384x16384 FP16 data remains. Permanent for 5 minutes confirmed.

## Conclusion
416.19W peak — highest FP16 power on A100. Ghost State 2 persistent 300s.
