=== TEST 1: H100 IDLE BASELINE RESULTS ===
=== Manmohan Bains | May 7, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure the H100 GPU's power draw, utilization, and temperature at idle (0% load)
to establish baseline for comparison against A100.

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
Power Draw             75.39W
Utilization            0%
Temperature            29°C

================================================================================
COMPARISON WITH A100:

Metric                 A100          H100
---------------------  ------------  ------------
Power Draw             58.1W         75.39W
Utilization            0%            0%
Temperature            28°C          29°C

================================================================================
FREQUENTLY ASKED QUESTIONS:

Q: Why is H100 idle power higher than A100?
A: Larger transistor count (80B vs 54B), higher base clocks, HBM3 memory, PCIe 5.0.

Q: Does higher idle power affect ghost power detection?
A: Yes. Ghost power threshold on H100 starts at 75W vs 58W on A100.

================================================================================
SCIENTIFIC SIGNIFICANCE:

H100 idle power is 30% higher than A100 (75.4W vs 58.1W).
This means power spikes start from a higher baseline,
affecting power capping and energy cost calculations.

================================================================================
CONCLUSION:

✅ H100 idle power: 75.39W at 0% utilization
✅ H100 idle temperature: 29°C
✅ Baseline established for Tests 2-11

================================================================================
STATUS: TEST 1 COMPLETE ✅
================================================================================
