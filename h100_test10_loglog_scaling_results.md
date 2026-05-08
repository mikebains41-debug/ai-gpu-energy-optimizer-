=== TEST 10: H100 LOG-LOG SCALING TEST RESULTS ===
=== Manmohan Bains | May 7, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure H100 FP32 compute performance across different matrix sizes (512 to 4096)
and observe scaling behavior using log-log analysis.

================================================================================
WHY WE DID THIS TEST:

Log-log scaling reveals how efficiently the GPU utilizes larger matrix sizes.
The slope indicates performance scaling relative to theoretical FLOPs increase.

================================================================================
FORMULAS USED:

CEI (Compute) = (2 × N³) / time
where N = matrix size, 2 × N³ = FLOPs per matrix multiplication

Log(Size) = log10(N)
Log(CEI) = log10(CEI)

Theoretical scaling: CEI ∝ N³ (if perfect efficiency)
Actual slope < 3 indicates efficiency loss at larger sizes

================================================================================
TEST CONFIGURATION:

Parameter              Value
---------------------  -------------------------
GPU                    NVIDIA H100 (RunPod)
Precision              FP32
Matrix sizes           512, 1024, 2048, 4096
Warm-up iterations     10 per size
Timing Method          CUDA Events

================================================================================
RAW RESULTS:

| Matrix Size | Time (s) | CEI (FLOPs/sec) | Log(Size) | Log(CEI) |
|-------------|----------|-----------------|-----------|----------|
| 512         | 0.000038 | 7.14e+12        | 2.709     | 12.854   |
| 1024        | 0.000071 | 3.01e+13        | 3.010     | 13.478   |
| 2048        | 0.000353 | 4.86e+13        | 3.311     | 13.687   |
| 4096        | 0.002660 | 5.17e+13        | 3.612     | 13.713   |

================================================================================
CALCULATIONS:

For 512:  2 × 512³ = 2.68e+08 FLOPs / 0.000038s = 7.14e+12 FLOP/s
For 1024: 2 × 1024³ = 2.15e+09 FLOPs / 0.000071s = 3.01e+13 FLOP/s
For 2048: 2 × 2048³ = 1.72e+10 FLOPs / 0.000353s = 4.86e+13 FLOP/s
For 4096: 2 × 4096³ = 1.37e+11 FLOPs / 0.002660s = 5.17e+13 FLOP/s

================================================================================
SCALING ANALYSIS:

Size Ratio    Theoretical FLOPs Ratio    Actual CEI Ratio    Efficiency
512→1024     8.0x                       4.21x               52.6%
1024→2048    8.0x                       1.61x               20.1%
2048→4096    8.0x                       1.06x               13.3%

================================================================================
KEY FINDINGS:

1. CEI increases with matrix size (7.14e+12 → 5.17e+13 FLOP/s)
2. Largest gain: 512 → 1024 (4.21x increase)
3. Performance plateaus beyond 2048 (only 6% gain from 2048→4096)
4. Log-Log slope is less than theoretical (efficiency drops at larger sizes)

================================================================================
CONCLUSION:

✅ H100 FP32 performance scales with matrix size
✅ Peak performance: 51.7 TFLOPS at 4096x4096
✅ Larger matrices show diminishing returns due to memory bandwidth limits
✅ Log-Log scaling confirms good utilization at moderate sizes (1024-2048)

================================================================================
Screenshot: h100_test10_loglog_scaling.png

================================================================================
STATUS: TEST 10 COMPLETE ✅
================================================================================
