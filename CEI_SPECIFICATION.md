# Compute Energy Intensity (CEI) — Formal Specification
## GPU Energy Optimizer v2.0
## Author: Manmohan (Mike) Bains | mikebains41@gmail.com
## Date: 2026-05-28

---

## Definition
Compute Energy Intensity (CEI) measures the computational work
delivered per unit of energy consumed by a GPU.

CEI = Total FLOPs / Total Energy (Joules)
Unit: FLOPs/Joule or GFLOPS/Watt

---

## Standard CEI Formula
CEI = (Matrix_Size^3 × 2 × Iterations) / (Power_W × Duration_s)

Where:
- Matrix_Size = dimension of square matrix (e.g. 4096)
- 2 = multiply-add operations per element
- Iterations = number of matrix multiplications
- Power_W = average power during compute window
- Duration_s = total compute duration in seconds

---

## Ghost Power Correction
Standard CEI excludes idle and ghost power periods.
This produces artificially high efficiency figures.

True CEI includes all power consumed including:
- Ghost power at 0% utilization
- Idle floor power
- Post-workload P0 retention
- Spontaneous burst events

### A100 SXM Proven Values
Reported CEI: 5.68B FLOPs/joule
True CEI: 4.12B FLOPs/joule
Degradation: 27.5% worse than reported

### Formula
True_CEI = Total_FLOPs / (Total_Energy_Including_Ghost_J)

Total_Energy = (Compute_Power_W × Compute_Duration_s)
             + (Ghost_Power_W × Ghost_Duration_s)
             + (Idle_Power_W × Idle_Duration_s)

---

## Hardware-Attested Measurements

### A100 SXM (24 validated tests)
| Metric | Value |
|---|---|
| Idle floor | 67.1W |
| Ghost power | 146.66W at 0% util |
| FP32 CEI reported | 5.68B FLOPs/joule |
| FP32 CEI true | 4.12B FLOPs/joule |
| FP16 average power | 482.7W |
| FP32 average power | 302W |

### H100 SXM (11 validated tests)
| Metric | Value |
|---|---|
| Idle floor | 69.5W |
| Ghost power | None |
| CEI | 76.5 GFLOPS/W |
| FP32 | 47 TFLOPS |
| FP16 | 592.8 TFLOPS |

### B200 2x GPU (6 validated tests)
| Metric | Value |
|---|---|
| Idle floor | 143.47W per GPU |
| Combined idle | 288.71W |
| Ghost power | From cold boot |
| FP32 power | 237.50W at 7-9% util |
| FP16 power | 197W at 0% util |
| CEI | TBD — pending bare metal sustained test |

---

## Ghost Power Classification

### Type 1 — Post-Workload Ghost (A100 SXM)
- Trigger: After compute workload completes
- Power: 146.66W at 0% utilization
- P-State: P0 locked
- Remediation: Blocked by hypervisor

### Type 2 — Cold Boot Ghost (B200 Blackwell)
- Trigger: Present from first power-on
- Power: 143-145W per GPU from boot
- P-State: P0 locked from boot
- More severe than Type 1

### Type 3 — FP16 Telemetry Blackout (B200)
- Power: 197-202W at 0% reported utilization
- Cause: NVML blind to tensor core activity
- Duration: Entire FP16 workload invisible

### Type 4 — Spontaneous Burst (B200)
- Power: 195.72W at 0% util no workload
- Trigger: Autonomous GPU activity
- Duration: ~10 seconds
- Cause: Unknown

---

## Methodology
- Tool: nvidia-smi via Python subprocess
- Sampling: 1Hz to 100Hz
- Duration: Minimum 60 minutes per test
- Provider: RunPod cloud infrastructure
- Validation: Cross-referenced with dmon output
- Trust posture: hardware_attested

---

## References
- Public datasets: https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-/tree/main/datasets
- Live API: https://ai-gpu-brain-v3.onrender.com/docs
- Whitepaper: https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-/blob/main/WHITEPAPER.md

---

## License
Specification: Creative Commons Attribution 4.0
Code: Source Available
2026 Manmohan Bains
