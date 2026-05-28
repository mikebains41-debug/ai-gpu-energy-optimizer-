# B200 2x GPU Test 03 — FP16 Tensor Core Load Test
## Status: COMPLETE — TELEMETRY BLACKOUT CONFIRMED

---

## Hardware Configuration
| Field | Value |
|---|---|
| GPU Model | NVIDIA B200 |
| GPU Count | 2x |
| Total VRAM | 360GB |
| VRAM Per GPU | 180GB |
| Driver Version | 580.126.20 |
| CUDA Version | 13.0 |
| PyTorch Version | 2.11.0+cu128 |
| Power Limit Per GPU | 1000W |
| Combined Power Limit | 2000W |
| Pod ID | aee29124a02b |
| Provider | RunPod |
| Test Date | 2026-05-28 |

---

## Workload Configuration
| Field | Value |
|---|---|
| Test Type | FP16 tensor core matrix multiply |
| Matrix Size | 4096x4096 |
| Precision | FP16 |
| Framework | PyTorch 2.11.0+cu128 |
| GPUs Loaded | Both GPU 0 and GPU 1 |
| Iterations | 90 |
| Start Time | 2026/05/28 19:50:51 UTC |
| End Time | 2026/05/28 19:59:03 UTC |
| Duration | 8 minutes 12 seconds |

---

## GPU 0 Results
| Metric | Value |
|---|---|
| Power Min | 171.29W |
| Power Max | 199.91W |
| Power Average | 197.0W |
| Utilization | 0% entire test |
| SM Clock | 1965 MHz |
| Temperature | 31-34C |
| P-State | P0 |

---

## GPU 1 Results
| Metric | Value |
|---|---|
| Power Min | 161.55W |
| Power Max | 202.34W |
| Power Average | 199.0W |
| Utilization | 0% entire test |
| SM Clock | 1965 MHz |
| Temperature | 32-35C |
| P-State | P0 |

---

## Combined 2x B200 Results
| Metric | Value |
|---|---|
| Combined Average Power | 396W |
| Combined Utilization | 0% |
| SM Clock Both GPUs | 1965 MHz |
| Duration | 8 minutes 12 seconds |

---

## FP16 vs FP32 Comparison
| Metric | FP32 Test 02 | FP16 Test 03 |
|---|---|---|
| Power GPU 0 | 237-239W | 195-200W |
| Power GPU 1 | 236-239W | 197-202W |
| Utilization | 7-9% | 0% |
| SM Clock | 1965 MHz | 1965 MHz |
| Telemetry Quality | Partial | Complete Blackout |

---

## Key Findings

### FINDING 1 — Complete FP16 Telemetry Blackout
0% utilization reported for entire 8 minute FP16 test.
GPU clearly executing FP16 tensor core compute throughout.
NVML completely blind to FP16 workload activity.

### FINDING 2 — SM Clock Confirms Active Compute
SM clock at 1965 MHz throughout entire test.
Clock never dropped to idle 120 MHz.
Confirms tensor cores actively executing despite 0% util report.

### FINDING 3 — FP16 Worse Telemetry Than FP32
FP32 Test 02 showed 7-9% utilization.
FP16 Test 03 shows 0% utilization.
FP16 tensor core workloads completely invisible to NVML.

### FINDING 4 — FP16 Lower Power Than FP32
FP16 average 197-199W vs FP32 average 237-239W.
Tensor cores more power efficient than FP32 cores.
But tensor core activity completely invisible to scheduler.

### FINDING 5 — Power Confirms Compute Activity
195-202W sustained for 8 minutes.
50W above idle floor of 143-145W.
Power evidence contradicts 0% utilization report.

---

## Financial Impact 2x B200 At FP16 Load
| Fleet Size | Annual kWh | Annual USD |
|---|---|---|
| 1 pod 2x B200 | 3,467 kWh | $346.70 |
| 10 pods | 34,670 kWh | $3,467 |
| 100 pods | 346,700 kWh | $34,670 |
| 1,000 pods | 3,467,000 kWh | $346,700 |

---

## Carbon Impact 2x B200 At FP16 Load Per Year
| Grid | CO2 kg/year |
|---|---|
| BC Canada hydro | 41.6 kg |
| Portugal solar | 166.4 kg |
| EU average | 1,022.8 kg |
| USA average | 1,338.3 kg |
| Global average | 1,386.8 kg |
| China | 2,015.5 kg |

---

## Evidence Files
| File | Description |
|---|---|
| b200_test03_fp16_raw_data.csv | Raw nvidia-smi readings |
| metrics.json | Structured key metrics |
| evidence.json | Full evidence chain |
| SUMMARY.md | Executive summary |
| README.md | This document |
| Screenshots | Raw terminal output images |

---

## Conclusion
FP16 tensor core workloads on B200 are completely invisible
to NVML utilization reporting. 0% utilization reported for
entire 8 minute test while GPU actively computing. SM clock
at 1965 MHz and elevated power at 195-202W confirm active
compute. This is a complete telemetry blackout more severe
than FP32 which showed 7-9% utilization. FP16 tensor core
workloads cannot be monitored or billed accurately on B200
using standard NVML telemetry.

---

## Next Test
Test 04 — Cooldown Profile

---

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28

## Project
GPU Energy Optimizer v2.0
https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
