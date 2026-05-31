# A100 SXM 80GB — Complete Test Reports
**Date:** 2026-05-29 to 2026-05-31 | **Pod:** bbcd7cb43196
**Researcher:** Manmohan (Mike) Bains | mikebains41@gmail.com

## VRAM Tests
| Test | Result | Residual | Security |
|---|---|---|---|
| test-01 baseline | PASS | 0 MB | None |
| test-02 workload | RESIDUAL | **457 MB** | HIGH |
| test-03 SIGKILL | PASS | **0 MB** | None |
| test-04 FP32 | RESIDUAL | **457 MB** | HIGH |
| test-05 FP16 | RESIDUAL | **463 MB** | HIGH |
| test-06 full profile | RESIDUAL + ASYMMETRIC | **465 MB** | HIGH |

## Memory Clock Tests
| Test | Key Finding | Security |
|---|---|---|
| test-01 idle | MEM=1593MHz locked at 0MB VRAM | None |
| test-02 FP32 | SM 210→1410MHz MEM=1593 always | HIGH |
| test-03 FP16 | SM 210→1155MHz MEM=1593 always | HIGH |
| test-04 cooldown | SM stuck at 1155MHz post-load | HIGH |
| test-05 ghost | 416W peak ghost state 2 for 300s | HIGH |

## Security Findings
1. HIGH: VRAM data persists 457-465 MB after graceful PyTorch exit
2. HIGH: SIGKILL = only safe cleanup — 0 MB residual
3. HIGH: SM clock stuck at 1155MHz post-load indefinitely
4. HIGH: HBM MEM clock locked 1593MHz 24/7
5. MEDIUM: Asymmetric GPU load in test-06

## Ghost Power States
| State | SM Clock | MEM Clock | Power |
|---|---|---|---|
| Cold boot | 210 MHz | 1593 MHz | 65W |
| Post-load | 1155 MHz | 1593 MHz | 86W |
