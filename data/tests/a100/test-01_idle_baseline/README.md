=== TEST 1: A100 IDLE BASELINE RESULTS ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To establish the baseline power draw, utilization, and temperature behavior of an idle A100 GPU over a continuous 10-minute period with no active workload. This provides a reference point for all subsequent tests.

================================================================================
WHY WE DID THIS TEST:

Without a baseline, we cannot prove that:
- Power spikes during active tests are abnormal
- Utilization reporting is accurate at idle
- The GPU is functioning normally
- Temperature behavior is within expected range

This test answers: "What does normal idle behavior look like on A100?"

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Duration | 10 minutes (600 seconds) |
| Workload | None (idle) |
| Monitoring Tool | nvidia-smi (NVML) |
| Sampling Rate | 1 second |
| Total Samples | 601 |
| Timestamp Range | 03:57:48 to 04:07:46 |

================================================================================
TIMESTAMP PROOF OF DURATION:

Start: 2026/05/09 03:57:48.161
End:   2026/05/09 04:07:46.281
Total samples: 601
Calculated duration: 600 seconds = 10 minutes ✅

================================================================================
RESULTS:

| Metric | Value |
|--------|-------|
| Power Draw Range | 62.53W - 62.87W |
| Average Power | 62.7W |
| Power Variation | ±0.17W |
| Utilization | 0% (throughout) |
| Temperature | 40°C (stable) |
| Power Spikes | None detected |

================================================================================
RAW DATA SAMPLE (first 5 lines with timestamps):

timestamp, power.draw [W], utilization.gpu [%], temperature.gpu
2026/05/09 03:57:48.161, 62.87 W, 0 %, 40
2026/05/09 03:57:49.169, 62.53 W, 0 %, 40
2026/05/09 03:57:50.169, 62.53 W, 0 %, 40
2026/05/09 03:57:51.169, 62.53 W, 0 %, 40

================================================================================
RAW DATA SAMPLE (last 5 lines with timestamps):

2026/05/09 04:07:43.281, 62.80 W, 0 %, 40
2026/05/09 04:07:44.281, 62.80 W, 0 %, 40
2026/05/09 04:07:45.281, 62.80 W, 0 %, 40
2026/05/09 04:07:46.281, 62.80 W, 0 %, 40

================================================================================
WHAT THESE RESULTS MEAN:

1. A100 idle power is stable at ~62.7W (range 62.53-62.87W)
2. Utilization correctly reports 0% when no workload is running
3. Temperature stable at 40°C
4. No ghost power anomalies present during idle (expected)
5. Power variation is minimal (±0.17W over 10 minutes)
6. The GPU is functioning normally and ready for active tests

================================================================================
FREQUENTLY ASKED QUESTIONS:

Q: Why is idle power 62.7W instead of 0W?
A: GPUs consume power even when idle due to:
   - Memory refresh cycles
   - PCIe link maintenance
   - Voltage regulators
   - Thermal monitoring

Q: Could this baseline change between tests?
A: Yes. Temperature, driver versions, and GPU state can affect idle power. This is why we establish baseline before active tests.

Q: Is 62.7W typical for A100?
A: Yes. A100 idle power typically ranges from 55W to 65W depending on configuration and ambient temperature.

Q: Why are there two screenshots?
A: First screenshot shows raw power data (no timestamps). Second screenshot shows timestamped data proving 10-minute duration.

Q: Does this prove anything about ghost power?
A: No. This test only establishes normal behavior. Ghost power requires active workloads (Tests 2-4).

================================================================================
HOW THIS BASELINE IS USED:

| Comparison Test | Purpose |
|-----------------|---------|
| Test 2 (Ghost Power) | 102W > 62.7W → Power increase proves activity |
| Test 3 (Sampling Rate) | 73W > 62.7W → Power draw despite 0% util |
| Test 4 (Load Ramp) | 357W peak vs 62.7W idle → Power scaling validated |
| Tests 5-10 (CEI) | Power measured against idle baseline for efficiency |

================================================================================
CONCLUSION:

The A100 GPU exhibits stable idle behavior with:
- Power draw: 62.7W (range 62.53-62.87W)
- Utilization: 0% (correct reporting)
- Temperature: 40°C (normal range)
- No anomalies detected
- 10-minute duration confirmed by timestamps

This baseline confirms normal GPU operation and provides a reference for detecting abnormal power/utilization patterns in active tests.

================================================================================
SCREENSHOTS:
- a100_test1_idle.png (raw power data)
- a100_test1_timestamped.png (timestamp proof)

================================================================================
STATUS: TEST 1 COMPLETE ✅
================================================================================
