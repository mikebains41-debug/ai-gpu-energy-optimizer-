# VRAM Tests - A100 SXM
| Test | ID | Status | Finding |
|---|---|---|---|
| VRAM Baseline | test-25 | DONE | 0MB VRAM ghost power 65.84W active |
| VRAM Workload | test-26 | PENDING | FP32 load monitor VRAM fill |
| VRAM Residual | test-27 | PENDING | Does VRAM clear after exit |

## Root Cause
HBM memory clock locked 1593MHz 24/7. Ghost power not VRAM-content-driven.
57 validated tests. 7 architectures.
