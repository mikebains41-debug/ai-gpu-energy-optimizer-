=== TEST 10: A100 LOG-LOG SCALING TEST ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure A100 FP32 compute performance across different matrix sizes (512 to 4096)
and observe scaling behavior using log-log analysis.

================================================================================
WHY WE DID THIS TEST:

Log-log scaling reveals how efficiently the GPU utilizes larger matrix sizes.
The slope indicates performance scaling relative to theoretical FLOPs increase.
This helps identify optimal matrix size for A100 workloads.

================================================================================
FORMULAS USED:

CEI (Compute) = (2 × N³) / time
where N = matrix size, 2 × N³ = FLOPs per matrix multiplication

Log(Size) = log10(N)
Log(CEI) = log10(CEI)

Theoretical scaling: CEI ∝ N³ (if perfect efficiency)

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Precision | FP32 |
| Matrix sizes | 512, 1024, 2048, 4096 |
| Warm-up iterations | 10 per size |
| Timing Method | CUDA Events |

================================================================================
RESULTS:

| Matrix Size | Time (s) | CEI (FLOPs/sec) | Log(Size) | Log(CEI) |
|-------------|----------|-----------------|-----------|----------|
| 512 | 0.000057 | 4.673e+12 | 2.709 | 12.670 |
| 1024 | 0.000179 | 1.198e+13 | 3.010 | 13.079 |
| 2048 | 0.001208 | 1.423e+13 | 3.311 | 13.153 |
| 4096 | 0.007726 | 1.779e+13 | 3.612 | 13.250 |

================================================================================
CALCULATIONS:

For 512:  2 × 512³ = 2.68e+08 FLOPs / 0.000057s = 4.673e+12 FLOP/s
For 1024: 2 × 1024³ = 2.15e+09 FLOPs / 0.000179s = 1.198e+13 FLOP/s
For 2048: 2 × 2048³ = 1.72e+10 FLOPs / 0.001208s = 1.423e+13 FLOP/s
For 4096: 2 × 4096³ = 1.37e+11 FLOPs / 0.007726s = 1.779e+13 FLOP/s

================================================================================
SCALING ANALYSIS:

| Size Transition | Theoretical Ratio | Actual CEI Ratio | Efficiency |
|-----------------|-------------------|------------------|------------|
| 512 → 1024 | 8.0x | 2.56x | 32.0% |
| 1024 → 2048 | 8.0x | 1.19x | 14.9% |
| 2048 → 4096 | 8.0x | 1.25x | 15.6% |

================================================================================
KEY FINDINGS:

1. CEI increases with matrix size (4.67e+12 → 1.78e+13 FLOP/s)
2. Largest gain: 512 → 1024 (2.56x increase)
3. Peak performance: 17.79 TFLOPS at 4096x4096
4. Performance plateaus beyond 1024 due to memory bandwidth limits

================================================================================
CONCLUSION:

The A100 GPU achieves peak FP32 performance of 17.79 TFLOPS at 4096x4096 matrix size.
Performance scales well from 512 to 1024, with diminishing returns beyond.

================================================================================
SCREENSHOTS:
- a100_test10_loglog_scaling.png

================================================================================
STATUS: TEST 10 COMPLETE ✅
================================================================================
