=== TEST 6: H100 CEI EFFICIENCY RESULTS ===
=== Manmohan Bains | May 7, 2026 ===

================================================================================
WHAT THIS TEST DOES:

Measures H100 power efficiency in FLOPs per Watt.
Combines compute performance (FLOPs/sec) with power draw (Watts).

================================================================================
FORMULAS USED:

CEI (Compute) = (2 × N³) / kernel_time
CEI_efficiency = CEI / power_Watts

Where:
N = 2048
2 × N³ = 1.718e+10 FLOPs per matrix multiplication

================================================================================
TEST CONFIGURATION:

Parameter              Value
---------------------  -------------------------
GPU                    NVIDIA H100 (RunPod)
Matrix Size            2048 x 2048
Precision              FP32
Compute Duration       5 minutes (300 seconds)
Power Sampling         1 second intervals

================================================================================
RESULTS:

Metric                 Value
---------------------  -------------------------
Mean CEI (Compute)     4.92e+13 FLOPs/sec
Mean Power Draw        635.28 W
Mean CEI Efficiency    7.74e+10 FLOPs/Watt

================================================================================
PROOF OF 5-MINUTE DURATION:

Total lines: 305 seconds
First power reading: 75.65 W (idle)
Last power reading: 642.29 W (under load)

================================================================================
KEY FINDINGS:

- H100 FP32 compute: 49.2 TFLOPS
- H100 power draw under load: 635W
- H100 efficiency: 77.4 GFLOPS per Watt

================================================================================
CONCLUSION:

✅ H100 FP32 compute: 49.2 TFLOPS
✅ H100 power draw: 635W at full load
✅ H100 efficiency: 7.74e+10 FLOPs/Watt

================================================================================
Screenshot: h100_test6_power_proof.png

================================================================================
STATUS: TEST 6 COMPLETE ✅
================================================================================
