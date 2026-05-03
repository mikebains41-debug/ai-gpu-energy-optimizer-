=== TEST 1: A100 BASELINE IDLE CAPTURE RESULTS ===
=== Manmohan Bains | May 2, 2026 ===

================================================================================

WHAT THIS TEST WAS FOR:

To establish the baseline power draw and utilization behavior of an idle A100 GPU
over a continuous 10-minute period with no active workload. This provides a
reference point for all subsequent tests.

================================================================================

WHY WE DID THIS TEST:

Without a baseline, we cannot prove that:
- Power spikes during active tests are abnormal
- Utilization reporting is accurate at idle
- The GPU is functioning normally

This test answers: "What does normal idle behavior look like?"

================================================================================

TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Duration | 10 minutes (600 seconds) |
| Workload | None (idle) |
| Monitoring Tool | nvidia-smi (NVML) |
| Sampling Rate | 1 second |
| Total Samples | ~600 |

================================================================================

RESULTS:

| Metric | Value |
|--------|-------|
| Power Draw Range | 57.8W - 58.1W |
| Average Power | 58.1W |
| Utilization | 0% (throughout) |
| Power Spikes | None detected |
| Temperature | Normal range |

================================================================================

RAW DATA SAMPLE (first 10 seconds):

timestamp,utilization,power
1777742997.0975347,0,58.1
1777742998.0976555,0,58.1
1777742999.0978323,0,58.1
1777743000.0980172,0,58.1
1777743001.0981104,0,58.1
...

================================================================================

WHAT THESE RESULTS MEAN:

1. GPU idle power is stable at 58.1W (expected range: 55-65W for A100)

2. Utilization correctly reports 0% when no workload is running

3. No ghost power anomalies present during idle (expected)

4. The GPU is functioning normally and ready for active tests

================================================================================

FREQUENTLY ASKED QUESTIONS:

Q: Why is idle power 58W instead of 0W?
A: GPUs consume power even when idle due to:
   - Memory refresh cycles
   - PCIe link maintenance
   - Voltage regulators
   - Thermal monitoring

Q: Could this baseline change between tests?
A: Yes. Temperature, driver versions, and GPU state can affect idle power.
   This is why we establish baseline before active tests.

Q: Is 58W typical for A100?
A: Yes. A100 idle power typically ranges from 55W to 65W depending on
   configuration and ambient temperature.

Q: Does this prove anything about ghost power?
A: No. This test only establishes normal behavior. Ghost power requires
   active workloads (Tests 2-4).

Q: How do I know the GPU was truly idle?
A: nvidia-smi showed no active processes. Utilization was 0% for 10 minutes.
   No workload was submitted during this test.

================================================================================

HOW THIS BASELINE IS USED:

| Comparison Test | Purpose |
|-----------------|---------|
| Test 2 (Ghost Power) | 102.3W > 58.1W → Power increase proves activity |
| Test 3 (Sampling Rate) | 86.8W > 58.1W → Power draw despite 0% util |
| Test 4 (Load Ramp) | 344W peak vs 58.1W idle → Power scaling validated |
| Tests 5-10 (CEI) | Power measured against idle baseline for efficiency |

================================================================================

SCREENSHOTS:

See GitHub repository:
- test1_baseline_idle_capture_1.jpg through _8.jpg

================================================================================

CONCLUSION:

The A100 GPU exhibits stable idle behavior with:
- Power draw: 58.1W (typical range 57.8W - 58.1W)
- Utilization: 0% (correct reporting)
- No anomalies detected

This baseline confirms normal GPU operation and provides a reference
for detecting abnormal power/utilization patterns in active tests.

================================================================================

STATUS: TEST 1 COMPLETE ✅

================================================================================
