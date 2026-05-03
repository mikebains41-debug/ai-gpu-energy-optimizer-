=== TEST 9: A100 NORMALITY TEST (Shapiro-Wilk) RESULTS ===
=== Manmohan Bains | May 2, 2026 ===

================================================================================

WHAT THIS TEST WAS FOR:

To determine if the CEI (Compute Execution Index) values from Test 7 follow a
normal (bell curve) statistical distribution. This helps determine whether
parametric statistics (mean, standard deviation) or non-parametric statistics
(median, percentiles) should be used for analysis.

================================================================================

WHY WE DID THIS TEST:

- GPU workloads often produce non-normal distributions due to:
  - Warm-up effects (first runs slower)
  - Thermal throttling transitions
  - Power state changes
  - GPU clock speed variations

- Understanding distribution shape validates our statistical approach
- Confidence intervals remain valid at n≥30 regardless of distribution

================================================================================

TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Data Source | Test 7 CEI values (4096x4096 FP32) |
| Samples | 58 |
| Test Type | Shapiro-Wilk Normality Test |
| Duration | ~30 seconds |

================================================================================

FORMULAS USED:

Shapiro-Wilk Test:
W = (Σ a_i × x_(i))² / Σ (x_i - x̄)²
p-value < 0.05 = NOT normally distributed

Skewness:
Skewness = Σ (x_i - x̄)³ / (n × σ³)
0 = symmetric | Positive = right skew | Negative = left skew

================================================================================

RESULTS:

| Metric | Value |
|--------|-------|
| Samples | 58 |
| Mean CEI | 1.510e+13 FLOPs/sec |
| Median CEI | 1.513e+13 FLOPs/sec |
| Standard Deviation | 1.760e+11 |
| Shapiro-Wilk p-value | 0.000000 |
| Skewness | -5.0295 |

================================================================================

INTERPRETATION:

p-value (0.000000) < 0.05 → Data is NOT normally distributed

Skewness (-5.0295) → Strong negative skew (left tail)
- Most values are clustered at the high end
- Few outliers on the low end (warm-up, thermal events)

================================================================================

WHAT THIS MEANS:

For GPU burst workloads (matrix multiplication), CEI values are NOT normally
distributed. This is EXPECTED and NOT an error.

Reasons for non-normal distribution:

| Cause | Explanation |
|-------|-------------|
| Warm-up effects | First iterations are slower |
| Thermal throttling | Performance drops at temperature thresholds |
| Power state changes | GPU transitions between power states |
| Clock speed variations | Boosting and throttling cause variance |

================================================================================

IMPLICATION FOR CEI MEASUREMENTS:

| Implication | Recommendation |
|-------------|----------------|
| Mean is affected by outliers | Use median for central tendency |
| Standard deviation is inflated | Use percentiles for spread |
| Confidence intervals remain valid | Valid at n≥30 (Central Limit Theorem) |
| Anomaly detection | Use robust statistics (IQR, median absolute deviation) |

================================================================================

FREQUENTLY ASKED QUESTIONS:

Q: Does non-normal distribution invalidate my results?
A: No. The Central Limit Theorem states that sample means are normally
   distributed for n≥30 regardless of underlying distribution.

Q: Why is skewness negative (-5.03)?
A: Most CEI values are high (1.51e+13), with a few lower outliers
   (1.39e+13, 1.48e+13). This creates a left tail.

Q: Should I use mean or median for reporting?
A: Both. Mean for comparison with other GPUs. Median for robust
   central tendency. The small difference (1.510e+13 vs 1.513e+13)
   indicates outliers have minimal impact.

Q: Is this normal for GPU workloads?
A: Yes. GPU compute times are famously non-normal due to:
   - First-run compilation overhead
   - Thermal throttling
   - Power state transitions
   - Memory allocation delays

================================================================================

COMPARISON WITH EXPECTED DISTRIBUTION:

| Distribution Type | Characteristics | Does CEI match? |
|-------------------|----------------|-----------------|
| Normal (bell curve) | Symmetric, p>0.05 | ❌ No |
| Log-normal | Right-skewed | ❌ No |
| Left-skewed | Negative skew | ✅ Yes |

CEI values follow a left-skewed distribution, typical for GPU workloads
where most runs achieve peak performance with occasional slow outliers.

================================================================================

CONCLUSION:

✅ A100 CEI values are NOT normally distributed (p=0.000000, skew=-5.0295)
✅ This is EXPECTED for GPU workloads
✅ Does NOT invalidate CEI measurements
✅ 95% confidence intervals remain valid at n≥30
✅ Mean and median are very close (0.2% difference)

================================================================================

STATUS: TEST 9 COMPLETE ✅

================================================================================
