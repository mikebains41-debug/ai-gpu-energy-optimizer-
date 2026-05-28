# B200 Test 01 — Idle Baseline
## Status: COMPLETE — GHOST POWER CONFIRMED FROM COLD BOOT

---

## Hardware Configuration
| Field | Value |
|---|---|
| GPU Model | NVIDIA B200 |
| GPU Count | 2x |
| Driver Version | 580.126.20 |
| CUDA Version | 13.0 |
| VRAM Per GPU | 183,359 MiB (180GB) |
| Power Limit Per GPU | 1000W |
| Pod ID | aee29124a02b |
| Provider | RunPod |
| Test Date | 2026-05-28 |

---

## Test Configuration
| Field | Value |
|---|---|
| Test Type | Cold boot idle baseline |
| Total Duration | 65 minutes |
| Total Samples | 148 per GPU |
| Workloads Running | Zero |
| Processes Found | None |
| VRAM Used | 0 MiB |
| Sampling Interval | 10 seconds |
| Time Start | 17:18:11 UTC |
| Time End | 18:24:05 UTC |

---

## GPU 0 Results
| Metric | Value |
|---|---|
| UUID | GPU-220239ae-d503-df2c-f752-ed7360dc183e |
| Power Min | 143.20W |
| Power Max | 145.67W |
| Power Average | 143.47W |
| Utilization | 0% — sustained entire test |
| Temperature | 29-30C |
| SM Clock | 120 MHz |
| Memory Clock | 3996 MHz |
| P-State | P0 — locked from boot |
| VRAM Used | 0 MiB |

---

## GPU 1 Results
| Metric | Value |
|---|---|
| UUID | GPU-77df8266-a91d-541d-67f8-9807ff7075d1 |
| Power Min | 144.91W |
| Power Max | 147.04W |
| Power Average | 145.24W |
| Utilization | 0% — sustained entire test |
| Temperature | 30-31C |
| SM Clock | 120 MHz |
| Memory Clock | 3996 MHz |
| P-State | P0 — locked from boot |
| VRAM Used | 0 MiB |

---

## Key Findings

### FINDING 1 — B200 Ghost Power From Cold Boot
B200 draws 143-145W at 0% utilization from first boot.
No workload ever ran on this pod before measurement.
A100 SXM required a prior workload to trigger ghost power.
B200 ghost power is present from the moment the GPU powers on.

### FINDING 2 — Memory Subsystem Active At Idle
Memory clock running at 3996 MHz at zero utilization.
This explains the elevated idle power draw.
The entire memory subsystem is active with no compute activity.

### FINDING 3 — P0 State Locked From Boot
Both GPUs locked in maximum performance state from cold boot.
No trigger required. No workload needed.
This is different from A100 SXM behaviour.

### FINDING 4 — Power Stable Over 65 Minutes
GPU 0 variance: 2.47W over 65 minutes
GPU 1 variance: 2.13W over 65 minutes
This is not a boot transient. This is stable baseline behaviour.

### FINDING 5 — PyTorch Does Not Support B200
PyTorch 2.4.1 does not support CUDA sm_100.
B200 Blackwell requires sm_100.
Compute load tests require nightly PyTorch build.
The B200 software ecosystem is not yet mature for general use.

### FINDING 6 — Inter-GPU Power Differential
GPU 0 averages 143.47W
GPU 1 averages 145.24W
Consistent 1.77W differential between the two GPUs.
Same architecture — different power draw at idle.

---

## Architecture Comparison
| GPU | Idle Floor | Ghost Trigger | Ghost Power | P0 From Boot |
|---|---|---|---|---|
| T4 | 9.5W | None | None | No |
| RTX 4090 | 20W | None | None | No |
| A40 | 30.4W | None | None | No |
| A100 PCIe | 47W | None | None | No |
| H100 SXM | 69.5W | None | None | No |
| A100 SXM | 67.1W | Post workload | 146W | No |
| B200 | 143-145W | Cold boot | 143-145W | YES |

---

## Financial Impact
| Fleet Size | Annual kWh Wasted | Annual USD |
|---|---|---|
| 1 GPU | 1,256 kWh | $125.60 |
| 10 GPUs | 12,560 kWh | $1,256 |
| 100 GPUs | 125,600 kWh | $12,560 |
| 1,000 GPUs | 1,256,000 kWh | $125,600 |
| 10,000 GPUs | 12,560,000 kWh | $1,256,000 |
| 100,000 GPUs | 125,600,000 kWh | $12,560,000 |

---

## Carbon Impact Per GPU Per Year
| Grid | CO2 kg/year |
|---|---|
| BC Canada hydro | 15.1 kg |
| Portugal solar | 60.3 kg |
| California | 26.4 kg |
| EU average | 370.5 kg |
| USA average | 484.8 kg |
| Global average | 502.4 kg |
| China | 729.7 kg |

---

## Evidence Files
| File | Description |
|---|---|
| b200_test01_raw_data.csv | All raw nvidia-smi readings |
| metrics.json | Structured key metrics |
| SUMMARY.md | Executive summary |
| README.md | This document |
| Screenshots | Captured in RunPod terminal |

---

## Pending Tests
| Test | Status | Blocker |
|---|---|---|
| Test 02 FP32 Load | PENDING | PyTorch sm_100 support |
| Test 03 FP16 Load | PENDING | PyTorch sm_100 support |
| Test 04 Cooldown | PENDING | Compute test required first |
| Test 05 Post Load Ghost | PENDING | Compute test required first |
| Test 06 Multi GPU | PENDING | PyTorch sm_100 support |

---

## Conclusion
The NVIDIA B200 Blackwell GPU exhibits persistent ghost power
from cold boot at 143-145W with zero utilization and zero
processes running. This is a more severe finding than the
A100 SXM where ghost power required a prior workload trigger.

The B200 idle floor IS the ghost power floor. The memory
subsystem runs at 3996 MHz continuously regardless of compute
activity. Both GPUs lock into P0 state from boot.

Additionally PyTorch 2.4.1 does not support B200 Blackwell
architecture confirming the software ecosystem has not yet
matured for this generation of hardware.

This is the first publicly documented hardware-attested
B200 idle power measurement on record.

---

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28

## Project
GPU Energy Optimizer v2.0
https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
