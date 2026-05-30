# B200 Test 07 — VRAM Baseline
**Date:** 2026-05-30 | **GPU:** B200 x2 | **Samples:** 12 | **Duration:** 60s

## Result: PASS

| Metric | GPU0 | GPU1 |
|---|---|---|
| memory.used | 0 MB | 0 MB |
| memory.total | 183,359 MB | 183,359 MB |
| driver reservation | 727 MB | 727 MB |
| util.memory | 0% | 0% |
| ghost power avg | 190.35W | 187.96W |
| differential | 2.39W | GPU0 higher |

## Conclusion
0MB VRAM. Ghost power 188-190W from cold boot.
GPU0 consistently 2.39W higher than GPU1.
HBM driven not VRAM content driven.
