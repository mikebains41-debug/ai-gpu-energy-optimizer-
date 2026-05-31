# H200_VRAM_TEST_03_RESIDUAL
**Date:** 2026-05-30 | **GPU:** H200 SXM x2 | **Pod:** 6e7fb4e76def

## Result: RESIDUAL DETECTED + GHOST POWER STATE 2

| Phase | VRAM | Power | Util |
|---|---|---|---|
| Baseline | 0 MB | 79.51W | 0 pct |
| Compute | 5,207 MB | **696W** | 100 pct |
| VRAM Still Loaded | 5,207 MB | 136W | **0 pct** |
| After Clear | **629 MB** | 130W | 0 pct |

## Security Issue 1 HIGH
629 MB remains after graceful cleanup.
5,207 MB was fully readable post-compute at 0 pct util.

## Security Issue 2 MEDIUM
Ghost Power State 2 on H200:
- Baseline idle: 79.51W
- Post-load idle: 136W
- Elevation: +56W
- Power does not return to baseline after workload

## Cross-Architecture Residual
| GPU | Residual |
|---|---|
| A100 SXM | 457-465 MB |
| H200 SXM | **629 MB** |

## Conclusion
H200 ghost power state 2 confirmed. 629 MB residual. HBM3e architecture.
