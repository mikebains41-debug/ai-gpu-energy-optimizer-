# A100_MEMORY_CLOCK_TEST_04_COOLDOWN
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: SM CLOCK STUCK IN POST-LOAD STATE

| Phase | VRAM | SM Clock | MEM Clock | Power |
|---|---|---|---|---|
| Baseline | 0 MB | 210 MHz | 1593 MHz | 65.67W |
| FP16 Load | 847 MB | 1155 MHz | 1593 MHz | 86.04W |
| After Clear | 463 MB | **1155 MHz** | 1593 MHz | 86.04W |
| Cooldown | 463 MB | **1155 MHz** | 1593 MHz | 86.04W |

## Ghost Power State 2 Confirmed
SM clock stuck at 1155 MHz — does NOT return to idle 210 MHz.

| State | SM Clock | MEM Clock | Power |
|---|---|---|---|
| Cold boot | 210 MHz | 1593 MHz | 65W |
| Post-load | **1155 MHz** | 1593 MHz | **86W** |

## Security Issue HIGH
463 MB VRAM residual persists through entire cooldown.
