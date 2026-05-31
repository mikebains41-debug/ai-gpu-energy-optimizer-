# A100_VRAM_TEST_04_DETAILED_FP32
**Date:** 2026-05-31 | **GPU:** A100 SXM 80GB x2 | **Pod:** bbcd7cb43196

## Result: RESIDUAL DETECTED

| Phase | VRAM | GPU0 | GPU1 |
|---|---|---|---|
| Baseline | 0 MB | 64.46W | 66.53W |
| VRAM Loaded | 809 MB | 84.84W | 87.57W |
| FP32 Peak | 1,221 MB | 113.41W | 117.28W |
| Post Compute | 1,221 MB | 85.44W | 88.68W |
| After Clear | **457 MB** | 85.77W | 88.18W |

## Security Issue HIGH
457 MB FP32 tensor data remains. Matches test-02 — fixed CUDA runtime allocation.

## Conclusion
FP32 residual = 457 MB. Residual not compute-size dependent.
