=== TEST 3: A100 SAMPLING RATE TEST RESULTS ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To determine if ghost power appears at different NVML sampling rates (1s, 100ms, 10ms)
and whether higher sampling rates reveal compute activity.

================================================================================
WHY WE DID THIS TEST:

Critics might argue ghost power is caused by insufficient sampling rate.
This test eliminates that argument by testing rates up to 100x faster than default.

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Sampling Rates | 1 second, 100ms, 10ms |
| Workload | 4096x4096 FP16 matrix multiplication |
| Monitoring | nvidia-smi (subprocess) |

================================================================================
RESULTS:

| Sampling Rate | Power | Utilization | Ghost Power? |
|---------------|-------|-------------|--------------|
| 1 second (idle) | 63.1-63.4W | 0% | No |
| 100ms (during load) | 73.2-73.9W | 0-17% | **YES** |
| 10ms (during load) | 73.5W | 0% | **YES** |

================================================================================
DETAILED RESULTS:

1 SECOND SAMPLING (5 samples):
1: 0% 63.4W
2: 0% 63.4W
3: 0% 63.1W
4: 0% 63.4W
5: 0% 63.4W

100ms SAMPLING (10 samples):
1: 73.2W
2: 73.9W
3: 17% 73.5W
4-10: 0% 73.5W

10ms SAMPLING (20 samples):
1-20: 0% 73.5W

================================================================================
KEY FINDINGS:

1. Ghost power persists at 100ms sampling (73.5W at 0% util)
2. Ghost power persists at 10ms sampling (73.5W at 0% util for ALL 20 samples)
3. Sampling rate is NOT the cause of ghost power
4. The measurement blind spot is persistent

================================================================================
CONCLUSION:

The A100 ghost power anomaly is NOT caused by sampling rate. Even at 10ms resolution (100x faster than default), the A100 continues to show 0% utilization while drawing 73.5W of power. This confirms a persistent measurement blind spot.

================================================================================
SCREENSHOTS:
- a100_test3_sampling.png

================================================================================
STATUS: TEST 3 COMPLETE ✅
================================================================================
