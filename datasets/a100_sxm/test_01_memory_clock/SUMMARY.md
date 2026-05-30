# A100 Test 01 — Memory Clock Idle
**Date:** 2026-05-30 | **GPU:** A100 SXM x2 | **Pod:** bbcd7cb43196 | **Duration:** 23 min

## Result: CRITICAL

| Metric | GPU0 | GPU1 |
|---|---|---|
| Ghost power avg | 65.14W | 67.52W |
| SM clock | 210 MHz | 210 MHz |
| HBM clock | 1,593 MHz | 1,593 MHz |
| VRAM | 0 MB | 0 MB |
| util.gpu | 0% | 0% |
| P-state | P0 | P0 |

## Spontaneous Burst — 22:30:05
| Metric | Value |
|---|---|
| GPU affected | GPU1 only |
| Power spike | 107.84W |
| SM clock | 1,350 MHz |
| HBM clock | 1,593 MHz unchanged |
| util.gpu | 0% |
| GPU0 | Unaffected |

## Cross-Architecture Correlation
| GPU | HBM MHz | Ghost Power |
|---|---|---|
| A100 SXM | 1,593 | 65W |
| B200 SXM | 3,996 | 144W |
| Ratio | 2.51x | 2.21x |

## Conclusion
Ghost power confirmed. HBM locked 1593MHz. Spontaneous burst captured on GPU1 only — NVML blind. GPU1 2-3W higher than GPU0.
