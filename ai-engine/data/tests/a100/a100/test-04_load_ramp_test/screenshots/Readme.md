=== TEST 4: A100 LOAD RAMP TEST RESULTS ===
=== Manmohan Bains | May 8, 2026 ===

================================================================================
WHAT THIS TEST WAS FOR:

To measure how A100 power draw and utilization scale with increasing compute load,
from 0% to 100% load.

================================================================================
TEST CONFIGURATION:

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100 (RunPod) |
| Load Levels | 0%, 10%, 25%, 50%, 75%, 100% |
| Workload | Matrix multiplication (varying sizes) |
| Monitoring | nvidia-smi (subprocess) |

================================================================================
RESULTS:

| Load % | Before Power | Before Util | After Power | After Util |
|--------|--------------|-------------|-------------|-------------|
| 0% | 62.8W | 0% | 73.2W | 0% |
| 10% | 73.2W | 0% | 73.2W | 0% |
| 25% | 73.2W | 0% | 72.9W | 0% |
| 50% | 73.3W | 0% | 197.1W | 0% |
| 75% | 92.5W | 0% | 357.7W | 0% |
| 100% | 92.9W | 0% | 334.0W | 100% |

================================================================================
KEY FINDINGS:

1. GHOST POWER AT LOW LOADS: 0% utilization with 73W power draw (10-50% loads)
2. SEVERE LAG AT 75% LOAD: 357.7W power draw but 0% utilization reported
3. NORMAL AT 100% LOAD: 334W power, 100% utilization
4. Power spikes BEFORE utilization registers

================================================================================
CONCLUSION:

A100 exhibits severe telemetry desynchronization:
- Ghost power at low loads (73W at 0% util)
- Severe lag at 75% load (357W at 0% util)
- Monitoring tools miss real compute activity

================================================================================
SCREENSHOTS:
- a100_test4_load_ramp.png

================================================================================
STATUS: TEST 4 COMPLETE ✅
================================================================================
