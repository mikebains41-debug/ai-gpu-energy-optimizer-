=== TEST 1: H100 IDLE BASELINE RESULTS ===
=== Manmohan Bains | May 7, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure the H100 GPU's power draw, utilization, and temperature at idle (0% load) to establish baseline for comparison against A100.

================================================================================
WHY WE DID THIS TEST:

A100 Test 1 established idle baseline at 58.1W, 0% utilization, 28°C.
This test establishes H100 baseline for ghost power and load ramp comparisons.

================================================================================
TEST CONFIGURATION:

Parameter              Value
---------------------  -------------------------
GPU                    NVIDIA H100 (RunPod)
Duration               10 minutes
Monitoring             nvidia-smi (NVML)
Load                   0%

================================================================================
RESULTS:

Metric                 Value
---------------------  -------------------------
Power Draw             75.61W
Utilization            0%
Temperature            29°C

================================================================================
COMPARISON WITH A100:

Metric                 A100          H100
---------------------  ------------  ------------
Power Draw             58.1W         75.61W
Utilization            0%            0%
Temperature            28°C          29°C

================================================================================
SCIENTIFIC SIGNIFICANCE:

H100 idle power is 30% higher than A100 (75.6W vs 58.1W).
This means power spikes start from a higher baseline, affecting ghost power detection thresholds and power capping calculations.

================================================================================
CONCLUSION:

✅ H100 idle power: 75.61W at 0% utilization
✅ H100 idle temperature: 29°C
✅ Baseline established for Tests 2-11

================================================================================
Screenshot: h100_test1_idle.png

================================================================================
STATUS: TEST 1 COMPLETE ✅
================================================================================
