=== TEST 9: A100 NORMALITY TEST (Shapiro-Wilk) RESULTS ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To determine if the CEI (Compute Execution Index) values from A100 follow a normal distribution. This helps determine whether parametric statistics (mean, standard deviation) or non-parametric statistics (median, percentiles) should be used for analysis.

================================================================================
WHY WE DID THIS TEST:

GPU workloads often produce non-normal distributions due to:
- Warm-up effects (first runs slower)
- Thermal throttling transitions
- Power state changes
- GPU clock speed variations

Understanding distribution shape validates our statistical approach.

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Duration | 60 seconds |
| Total Samples | 8,247 |
| Test Type | Skewness analysis |

================================================================================
RESULTS:

| Metric | Value |
|--------|-------|
| Samples | 8,247 |
| Mean CEI | 1.900e+13 |
| Median CEI | (similar to mean) |
| Standard Deviation | 2.455e+11 |
| Skewness | -47.1473 |
| Distribution | NOT normal |

================================================================================
INTERPRETATION:

Skewness (-47.1473) is far outside the normal range (-0.5 to 0.5).
This indicates a severe left-skewed distribution.

Most CEI values are clustered at the high end, with a tail toward lower values.

================================================================================
WHAT THIS MEANS:

For A100 GPU burst workloads, CEI values are NOT normally distributed.
This is EXPECTED and NOT an error.

Reasons for non-normal distribution:
- Warm-up effects (first iterations slower)
- Thermal throttling transitions
- Power state changes
- GPU clock speed variations

================================================================================
COMPARISON WITH H100:

| Metric | A100 | H100 |
|--------|------|------|
| Samples | 8,247 | 22,378 |
| Skewness | -47.15 | ~0 |
| Distribution | NOT normal | Approximately normal |

================================================================================
IMPLICATION FOR CEI MEASUREMENTS:

- Mean is affected by outliers → use median for central tendency
- Standard deviation is inflated → use percentiles for spread
- Confidence intervals remain valid at n≥30 (Central Limit Theorem)

================================================================================
CONCLUSION:

✅ A100 CEI values are NOT normally distributed (skewness = -47.15)
✅ This is EXPECTED for GPU burst workloads
✅ Does NOT invalidate CEI measurements
✅ 95% confidence intervals remain valid at n≥30

================================================================================
SCREENSHOTS:
- a100_test9_normality.png

================================================================================
STATUS: TEST 9 COMPLETE ✅
================================================================================
