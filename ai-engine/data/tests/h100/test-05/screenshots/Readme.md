=== TEST 5: H100 CEI COMPUTE (2048x2048 FP32) RESULTS ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure the H100 GPU's raw compute performance in FLOPs per second
using FP32 precision on a 2048x2048 matrix multiplication.

================================================================================
WHY WE DID THIS TEST:

- Establishes baseline FP32 performance for H100
- Provides comparison data for A100
- Enables CEI Efficiency calculation (FLOPs per Watt) in Test 6
- Validates GPU is functioning normally before other tests

================================================================================
FORMULA:

CEI (Compute) = (2 × N³) / t
where N = 2048, 2 × N³ = 1.718e+10 FLOPs, t = kernel time in seconds

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA H100 (RunPod) |
| Matrix Size | 2048 x 2048 |
| Precision | FP32 |
| Iterations | 30 |
| Warm-up iterations | 10 |
| Timing Method | CUDA Events |

================================================================================
RAW DATA (30 iterations):

Iter  1: 0.3562 ms    Iter 16: 0.3547 ms
Iter  2: 0.3516 ms    Iter 17: 0.3487 ms
Iter  3: 0.3499 ms    Iter 18: 0.3492 ms
Iter  4: 0.3499 ms    Iter 19: 0.3489 ms
Iter  5: 0.3492 ms    Iter 20: 0.3496 ms
Iter  6: 0.3497 ms    Iter 21: 0.3487 ms
Iter  7: 0.3489 ms    Iter 22: 0.3494 ms
Iter  8: 0.3501 ms    Iter 23: 0.3486 ms
Iter  9: 0.3484 ms    Iter 24: 0.3496 ms
Iter 10: 0.3495 ms    Iter 25: 0.3488 ms
Iter 11: 0.3491 ms    Iter 26: 0.3493 ms
Iter 12: 0.3500 ms    Iter 27: 0.3487 ms
Iter 13: 0.3486 ms    Iter 28: 0.3484 ms
Iter 14: 0.3500 ms    Iter 29: 0.3487 ms
Iter 15: 0.3484 ms    Iter 30: 0.3486 ms

================================================================================
STATISTICAL ANALYSIS:

| Metric | Value |
|--------|-------|
| Mean Kernel Time | 0.3496 ms |
| Standard Deviation | 0.0017 ms |
| Minimum | 0.3484 ms |
| Maximum | 0.3562 ms |
| Range | 0.0078 ms |

================================================================================
PERFORMANCE CALCULATIONS:

CEI (Compute) = (2 × N³) / t
CEI = 1.718e+10 / (0.0003496) = 4.913e+13 FLOPs/sec

TFLOPS = CEI / 1e+12 = 49.13 TFLOPS

================================================================================
COMPARISON WITH A100:

| Metric | A100 | H100 |
|--------|------|------|
| Mean Kernel Time | 1.39 ms | 0.3496 ms |
| Mean CEI | 1.24e+13 FLOP/s | 4.913e+13 FLOP/s |
| Performance (TFLOPS) | 12.4 TFLOPS | 49.13 TFLOPS |
| Speedup | - | 3.96x |

================================================================================
KEY FINDINGS:

1. H100 FP32 compute: 49.13 TFLOPS
2. Extremely stable performance (0.49% variation)
3. 3.96x faster than A100
4. No thermal throttling detected

================================================================================
CONCLUSION:

The H100 GPU achieves 4.913e+13 FLOPs/sec (49.13 TFLOPS) on 2048x2048 FP32 matrix multiplication, which is 3.96x faster than A100.

================================================================================
SCREENSHOTS:
- h100_test5_cei_compute.png

================================================================================
STATUS: TEST 5 COMPLETE ✅
================================================================================
