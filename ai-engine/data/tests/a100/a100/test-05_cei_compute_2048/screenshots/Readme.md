=== TEST 5: A100 CEI COMPUTE (2048x2048 FP32) RESULTS ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure the A100 GPU's raw compute performance in FLOPs per second using FP32 precision on a 2048x2048 matrix multiplication.

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Matrix Size | 2048 x 2048 |
| Precision | FP32 |
| Iterations | 30 |
| Warm-up iterations | 10 |

================================================================================
RESULTS:

| Metric | Value |
|--------|-------|
| Mean Kernel Time | 1.1970 ms |
| Standard Deviation | 0.0018 ms |
| CEI | 1.435e+13 FLOP/s |
| TFLOPS | 14.35 |
| Relative Error | 0.15% |

================================================================================
CALCULATIONS:

CEI = (2 × N³) / t = 1.718e+10 / 0.001197 = 1.435e+13 FLOP/s
Error = (Std Dev / Mean) × 100 = (0.0018 / 1.1970) × 100 = 0.15%

================================================================================
KEY FINDINGS:

1. A100 FP32 compute: 14.35 TFLOPS
2. Extremely stable performance (0.15% variation)
3. No thermal throttling detected

================================================================================
CONCLUSION:

The A100 GPU achieves 14.35 TFLOPS FP32 performance on 2048x2048 matrix multiplication with 0.15% variation across 30 iterations.

================================================================================
SCREENSHOTS:
- a100_test5_cei_compute.png

================================================================================
STATUS: TEST 5 COMPLETE ✅
================================================================================
