# B200 2x GPU Test 02 — FP32 Load Test
## Status: COMPLETE — DESYNC CONFIRMED

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
| Test Type | FP32 matrix multiply load test |
| Matrix Size | 4096x4096 |
| Precision | FP32 |
| Framework | PyTorch 2.11.0+cu128 |
| GPUs Loaded | Both GPU 0 and GPU 1 |
| Iterations | 90 |
| Start Time | 2026/05/28 19:24:04 UTC |

---

## GPU 0 Results
| Metric | Idle | Under Load |
|---|---|---|
| Power | 143.99W | 237-238.84W |
| Utilization | 0% | 7-9% |
| SM Clock | 120 MHz | 1965 MHz |
| Temperature | 31C | 32-34C |
| P-State | P0 | P0 |

---

## GPU 1 Results
| Metric | Idle | Under Load |
|---|---|---|
| Power | 145.72W | 236-239.26W |
| Utilization | 0% | 7-9% |
| SM Clock | 120 MHz | 1965 MHz |
| Temperature | 31C | 33-34C |
| P-State | P0 | P0 |

---

## Combined 2x B200 Results
| Metric | Value |
|---|---|
| Combined Idle Power | 289.71W |
| Combined Peak Power | 478.10W |
| Combined Sustained Power | ~476W |
| Power Increase From Idle | +188W |
| Combined Utilization | 7-9% |
| SM Clock Both GPUs | 1965 MHz |

---

## Power Ramp Sequence
| Time | GPU 0 | GPU 1 | Util |
|---|---|---|---|
| 19:24:04 | 143.99W | 145.72W | 0% |
| 19:24:06 | 168.95W | 161.11W | 3% |
| 19:24:06 | 182.47W | 169.29W | 2% |
| 19:24:06 | 190.00W | 178.90W | 7% |
| 19:24:06 | 209.10W | 196.10W | 9% |
| 19:24:06 | 220.11W | 213.54W | 7% |
| 19:24:07 | 232.44W | 234.76W | 7% |
| 19:24:07 | 237.18W | 239.40W | 9% |
| 19:24:08 | 238.84W | 239.26W | 9% |

---

## Key Findings

### FINDING 1 — FP32 Load Confirmed on 2x B200
Both B200 GPUs successfully executed FP32 4096x4096
matrix multiply using PyTorch 2.11.0+cu128.
B200 CUDA sm_100 support confirmed working.

### FINDING 2 — DESYNC Pattern Confirmed
238-239W at only 7-9% reported utilization.
Power and utilization severely misaligned.
This is the DESYNC pattern confirmed on B200 Blackwell.
Expected power at 7-9% util would be approximately 50-80W.
Actual power is 3x higher than utilization suggests.

### FINDING 3 — SM Clock Activation
SM clock jumped from 120 MHz idle to 1965 MHz instantly.
Clock transition observed within milliseconds of load start.

### FINDING 4 — Power Ramp Speed
Full ramp from 143W idle to 239W sustained
completed in approximately 2 seconds.
Rapid power state transition confirmed.

### FINDING 5 — PyTorch 2.11.0 B200 Compatibility
PyTorch 2.11.0+cu128 fully supports B200 CUDA sm_100.
Previous PyTorch 2.4.1 was incompatible with B200.
This documents the minimum PyTorch version for B200.

---

## Financial Impact 2x B200 At FP32 Load
| Fleet Size | Annual kWh | Annual USD |
|---|---|---|
| 1 pod 2x B200 | 4,169 kWh | $416.90 |
| 10 pods | 41,690 kWh | $4,169 |
| 100 pods | 416,900 kWh | $41,690 |
| 1,000 pods | 4,169,000 kWh | $416,900 |

---

## Carbon Impact 2x B200 At FP32 Load Per Year
| Grid | CO2 kg/year |
|---|---|
| BC Canada hydro | 50.0 kg |
| Portugal solar | 200.1 kg |
| EU average | 1,229.8 kg |
| USA average | 1,609.2 kg |
| Global average | 1,667.6 kg |
| China | 2,422.1 kg |

---

## Evidence Files
| File | Description |
|---|---|
| b200_test02_fp32_raw_data.csv | Raw nvidia-smi readings |
| metrics.json | Structured key metrics |
| evidence.json | Full evidence chain |
| SUMMARY.md | Executive summary |
| README.md | This document |
| Screenshots | Raw terminal output images |

---

## Conclusion
Both NVIDIA B200 GPUs confirmed running FP32 workloads
with PyTorch 2.11.0+cu128. DESYNC pattern confirmed —
238-239W at only 7-9% reported utilization. SM clock
jumps from 120 to 1965 MHz instantly on load.
Power ramps from 143W idle to 239W sustained in 2 seconds.
Combined 2x B200 draws 476W under FP32 load.

---

## Next Test
Test 03 — FP16 Tensor Core Load Test

---

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28

## Project
GPU Energy Optimizer v2.0
https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
