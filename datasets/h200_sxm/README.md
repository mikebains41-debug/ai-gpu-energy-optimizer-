# H200 SXM — VRAM Test Reports
**Date:** 2026-05-30 | **Pod:** 6e7fb4e76def
**GPU:** H200 SXM x2 | **VRAM per GPU:** 143,156 MB

## Test Results
| Test | Result | Residual | Security |
|---|---|---|---|
| test-01 baseline | RESIDUAL | **529 MB** | HIGH |
| test-02 workload | RESIDUAL | **629 MB** | HIGH |
| test-03 residual | RESIDUAL + GHOST STATE 2 | **629 MB** | HIGH + MEDIUM |

## Cross-Architecture Comparison
| GPU | HBM | Residual |
|---|---|---|
| A100 SXM | HBM2e | 457-465 MB |
| H200 SXM | HBM3e | **529-629 MB** |

H200 HBM3e leaves significantly more data uncleared than A100 HBM2e.

## Security Findings
1. HIGH: 529-629 MB VRAM residual after every graceful PyTorch exit
2. MEDIUM: Ghost power state 2 confirmed — power 56W above baseline post-load
3. H200 util.memory underreports — shows 0 pct with 911 MB loaded

## Ghost Power State 2 on H200
- Baseline: 79.51W
- Post-load: 136W
- Elevation: +56W permanently
