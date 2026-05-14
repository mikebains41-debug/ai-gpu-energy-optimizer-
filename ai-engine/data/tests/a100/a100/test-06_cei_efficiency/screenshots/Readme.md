=== TEST 6: A100 CEI EFFICIENCY (CORRECTED) ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure the A100 GPU's power efficiency in FLOPs per Watt using continuous sustained load (no idle gaps), correcting the previous sampling error that showed 68W.

================================================================================
WHY THIS WAS CORRECTED:

Previous Test 6 reported 68.4W power draw. This was NVML sampling error because:
- The workload was burst (compute then sleep)
- NVML sampled during idle periods
- True power during compute is much higher

This corrected version uses continuous load for 60 seconds with no idle gaps.

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Matrix Size | 2048 x 2048 |
| Precision | FP32 |
| Duration | 60 seconds continuous load |
| Power Sampling | 1 second intervals |
| Workload Type | Continuous (no sleep, no idle) |

================================================================================
RESULTS:

| Metric | Value |
|--------|-------|
| Total Iterations | 58,927 |
| Mean Kernel Time | 0.9889 ms |
| CEI (Compute) | 1.737e+13 FLOP/s |
| Mean TFLOPS | 17.37 |
| Idle Power | 63.4W |
| Load Power Range | 317W - 342W |
| Mean Power (Load) | 330W |
| Efficiency | 52.6 GFLOPS/W |

================================================================================
POWER DATA (from NVML):

First 10 lines:
power.draw [W]
63.41 W (idle)
63.41 W (idle)
63.41 W (idle)
74.21 W (ramp-up)
317.09 W (load)
324.85 W (load)
326.59 W (load)
326.92 W (load)

Last 4 lines:
341.17 W
342.37 W
340.20 W
342.29 W

================================================================================
CALCULATIONS:

CEI = (2 × N³) / t = 1.718e+10 / (0.0009889) = 1.737e+13 FLOP/s
Efficiency = CEI / Power = 1.737e+13 / 330 = 5.26e+10 FLOP/W = 52.6 GFLOPS/W

================================================================================
COMPARISON WITH PREVIOUS (WRONG) RESULT:

| Metric | Previous (Wrong) | Corrected |
|--------|-----------------|-----------|
| Power Draw | 68.4W | 330W |
| Efficiency | 184 GFLOPS/W | 52.6 GFLOPS/W |
| Error | - | 71% overestimation |

================================================================================
KEY FINDINGS:

1. A100 true power draw under sustained FP32 load is ~330W (not 68W)
2. A100 true efficiency is 52.6 GFLOPS/W (not 184)
3. Previous 68W reading was NVML sampling artifact (measured idle between bursts)
4. Continuous load testing is mandatory for accurate efficiency measurements

================================================================================
CONCLUSION:

The A100 GPU achieves 1.737e+13 FLOP/s (17.37 TFLOPS) at 330W power draw under sustained load, resulting in 52.6 GFLOPS/W efficiency. Previous 68W reading was a sampling error.

================================================================================
SCREENSHOTS:
- a100_test6_power_proof.png

================================================================================
STATUS: TEST 6 COMPLETE ✅
================================================================================
