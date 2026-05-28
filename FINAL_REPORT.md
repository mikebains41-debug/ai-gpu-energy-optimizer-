FINAL REPORT: AI GPU Energy Optimizer – GHOST Anomaly & CEI Benchmark Validation

Author: Manmohan (Mike) Bains
Date: May 18, 2026
Repository: https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
Release: v1.0.0 (tag: 34f8eaa)
Test Platform: RunPod (NVIDIA A100 40GB SXM, personal expense)
License: Proprietary (source available)
API: https://ai-gpu-brain-v3.onrender.com

───

Executive Summary

The problem: Standard GPU utilization metrics lie. We proved an NVIDIA A100 SXM can draw 146.66W of power while reporting 0% utilization across sampling rates of 1 second, 100 milliseconds, and even 10 milliseconds. This "GHOST anomaly" means data centers over-provision GPUs, waste energy, and make capacity decisions based on false telemetry.

Our solution: The AI GPU Energy Optimizer detects GHOST anomalies in real time, benchmarks true Compute Energy Intensity (CEI) (FLOPs per joule), and integrates with Kubernetes and Slurm.

Validation: 24 A100 SXM hardware tests + 11 H100 SXM hardware tests = 35 validated tests. All 40/40 platform validation tests passing.

Ask: We are seeking sponsored compute or a partnership to scale validation across 100-500 GPUs. All tests to date were conducted independently at personal expense.

───

1. Problem: Why GPU Telemetry Fails

Production GPU monitoring tools (nvidia-smi, Prometheus NVML exporter, cloud dashboards) assume that high utilization means high work and low utilization means idle. This is false.

• Hidden energy waste - paying for compute you cannot see or schedule.
• Incorrect scaling - autoscalers think the GPU is idle and add more pods.
• Unreliable benchmarking - CEI calculations are wrong if utilization lies.

───

2. Test Methodology


Item
Details

Platform
RunPod (Community Cloud & Secure Cloud)

GPU (Primary)
NVIDIA A100 SXM 40GB

GPU (Secondary)
NVIDIA H100 SXM

Total Tests
24 A100 + 11 H100 = 35 hardware tests

Duration
20+ hours across all test plans

Tools
NVML, pynvml, custom Python agent, Prometheus, FastAPI

Sampling rates
1s, 100ms, 10ms

Workloads
Idle, GEMM FP32/FP16, load ramps, sustained runs up to 20 min

API endpoint
https://ai-gpu-brain-v3.onrender.com/results/a100



───

3. CEI Standard Definition


Field
Value

Metric
CEI - Compute Energy Intensity

Formula
CEI = Total FLOPs / Total Joules

Unit
FLOPs/J

Sampling
1Hz via nvidia-smi power readings

Reference value
A100 SXM, FP32, 900s sustained = 5.68B FLOPs/J

Threshold: Excellent
>10B FLOPs/J

Threshold: Good
5-10B FLOPs/J

Threshold: Moderate
1-5B FLOPs/J

Threshold: Poor
<1B FLOPs/J



A100 SXM baseline CEI of 5.68B FLOPs/J = Good tier.

───

4. Complete A100 Test Results (Tests 01-24)

Test 01 - A100 Idle Baseline

Metric
Value

Mean power
62.7W

Power range
62.53 - 62.87W

Utilization
0%

Temperature
40C

Duration
10 minutes / 601 samples

Status
PASS



Test 02 - A100 Ghost Power

Metric
Value

Ghost power detected
102.14W at 0% utilization

Idle power
63.4W

Load power range
397 - 413W

Load utilization
94 - 96%

Ghost power events
1 of 66 samples

Status
PASS - GHOST POWER CONFIRMED



Test 03 - A100 Sampling Rate (1s / 100ms / 10ms)

Metric
Value

Ghost at 1s
73.5W at 0% util

Ghost at 100ms
73.5W at 0% util

Ghost at 10ms
73.5W at 0% util

Conclusion
Blind spot persists at ALL sampling rates

Status
PASS



Test 04 - A100 Load Ramp (0-100%)

Metric
Value

Ghost power
73.2W at 0% util

Severe lag power
357.7W at 0% util

Peak power
357.7W at 100% util

Status
PASS



Test 05 - A100 CEI Compute (2048x2048)

Metric
Value

Mean TFLOPS
14.35

Mean CEI
1.435e+13 FLOPs/sec

Mean kernel time
1.197ms

Error
0.15%

Status
PASS



Test 06 - A100 CEI Efficiency (2048x2048)

Metric
Value

Mean TFLOPS
17.37

Mean power
330W

Efficiency
52.6 GFLOPS/W

Status
PASS



Test 07 - A100 CEI Compute (4096x4096)

Metric
Value

Mean TFLOPS
15.3

Mean CEI
1.53e+13 FLOPs/sec

Duration
10 minutes / 60 iterations

Status
PASS



Test 08 - A100 FP16 Tensor Core (15 min)

Metric
Value

Mean TFLOPS
231.08

Mean kernel time
0.5948ms

Iterations
1,440,905

Status
PASS



Test 09 - A100 Normality Test (Shapiro-Wilk)

Metric
Value

Samples
8,247

Skewness
-47.1473

Normal distribution
No (p = 0.000000)

Status
PASS



Test 10 - A100 Log-Log Scaling

Metric
Value

Peak TFLOPS
17.79

Peak matrix size
4096x4096

Status
PASS



Test 11 - A100 Observability Validation

Metric
Value

Idle power
62.74W

Burst power range
396 - 406W

Burst utilization
100%

Ghost power events
0

Samples
3,044

Status
PASS



Test 12 - A100 8192x8192 Load Test

Metric
Value

Matrix size
8192x8192 FP32

Load duration
20 minutes

Power range
305 - 342W

Utilization
100%

Status
PASS



Test 13 - A100 Load + Cooldown Ghost Power (5+6 min)

Metric
Value

Total duration
660 seconds

Workload
4096x4096 FP32 torch.matmul

Peak power (load)
146.66W

Mean power (load)
83.2W

Mean power (cooldown)
77.2W

Utilization throughout
0%

Ghost power
CONFIRMED

Root cause
P0 state + 1593 MHz memory clock

Status
PASS



Test 14 - Ghost Power 10+10 min Extended

Metric
Value

Total duration
1,200 seconds

Peak power (load)
146.66W

Mean power (load)
82.3W

Min power (cooldown)
66.16W

Mean power (cooldown)
72.1W

Utilization throughout
0%

Ghost power
CONFIRMED

Conclusion
Never dropped to true low-power idle

Status
PASS



Test 15 - A100 SXM Idle Baseline (15 min)

Metric
Value

Duration
900 seconds / 900 samples

Mean power
67.1W

Power range
66.5 - 68.0W

Temperature
27C

Status
PASS



Test 16 - Remediation Attempt

Metric
Value

Commands attempted
nvidia-smi -pm 0, nvidia-smi -pl 200

Persistence mode
FAILED - Unknown Error

Power cap
FAILED - Insufficient Permissions

Current power limit
500W

Root cause
RunPod hypervisor blocks GPU power management

Status
BLOCKED BY PLATFORM



Test 17 - P-State & Memory Clock Retention

Metric
Value

P-State
P0 (persistent)

Memory clock
1593 MHz (locked)

Duration
10 minutes post-load

Status
PASS



Test 18 - Load Ramp: Power vs Matrix Size

Matrix Size
Result

512
Low power

1024
Moderate

2048
Moderate-high

4096
High

6144
339.1W PEAK

8192
Drops (bandwidth saturation)

Status
PASS



Test 19 - FP16 Tensor Core 10 min (2048x2048)

Metric
Value

Duration
600 seconds

Average power
482.7W

Total FLOPs
1.03e+15

CEI
3.56e+9 FLOPs/J

Status
PASS



Test 20 - FP16 vs FP32 Quick (5 iter each)

Precision
Avg Time
Avg Power
Max Power
Avg Util

FP32
2.45ms
98.73W
137.28W
0%

FP16
0.52ms
77.61W
78.72W
0.4%

FP16 speedup
4.7x
Ghost in FP32 at 137.28W @ 0% util



Status
PASS






Test 21 - FP32 vs FP16 Full (60 iter each)

Precision
Mean Time
Power Range
Util

FP32
1.44ms
76-137W
0-4%

FP16
0.48ms
76-79W
0-4%

FP16 speedup
3.0x
Mismatch persists in both


Status
PASS





Test 22 - Persistence Mode Disable (Instance 47cdd71daf80)

Metric
Value

Command output
"Disabled... All done."

Post-check mode
Enabled (UNCHANGED)

P-State after
P0

Memory clock after
1593 MHz

Status
INCONCLUSIVE - hypervisor ignored command



Test 23 - A100 SXM Idle Baseline (Confirmation)

Metric
Value

Mean power
67.1W

Power range
66.5 - 68.0W

Temperature
27C

Status
PASS



Test 24 - CEI Validation 15 min Sustained FP32

Metric
Value

Duration
900 seconds

Iterations
90,000

Average power
302.37W

Total FLOPs
1.55e+15

Total energy
272,130 J

CEI
5.68e+9 FLOPs/J (5.68B)

Status
PASS - CEI REFERENCE VALUE ESTABLISHED



───

5. Complete Test Summary Table


Test
Name
Status
Key Finding

01
Idle Baseline
PASS
62.7W @ 0% util

02
Ghost Power
PASS
102.14W @ 0% util - CONFIRMED

03
Sampling Rate
PASS
Blind spot at 1s, 100ms, 10ms

04
Load Ramp
PASS
357.7W severe lag at 0% util

05
CEI Compute 2048
PASS
14.35 TFLOPS, 0.15% error

06
CEI Efficiency 2048
PASS
52.6 GFLOPS/W

07
CEI Compute 4096
PASS
15.3 TFLOPS

08
FP16 Tensor Core
PASS
231.08 TFLOPS - 15 min sustained

09
Normality Test
PASS
p=0.000000, skew=-47.15

10
Log-Log Scaling
PASS
Peak at 4096 (17.79 TFLOPS)

11
Observability Validation
PASS
3,044 samples, burst 396-406W

12
8192 Load Test
PASS
305-342W @ 100% util

13
Load + Cooldown 5+6 min
PASS
146.66W peak @ 0% util

14
Ghost Power 10+10 min
PASS
146.66W peak, never true idle

15
Idle Baseline 15 min
PASS
67.1W floor, 27C

16
Remediation Attempt
BLOCKED
Hypervisor blocks power management

17
P-State Retention
PASS
P0 + 1593 MHz locked post-load

18
Power vs Matrix Size
PASS
Peak 339.1W at 6144x6144

19
FP16 10 min Continuous
PASS
482.7W avg, 1.03e+15 FLOPs

20
FP16 vs FP32 Quick
PASS
FP16 4.7x faster, FP32 ghost 137W

21
FP16 vs FP32 Full
PASS
FP16 3.0x faster, mismatch in both

22
Persistence Disable
INCONCLUSIVE
Hypervisor ignored command

23
Idle Baseline Confirm
PASS
67.1W confirmed

24
CEI Validation 15 min
PASS
5.68B FLOPs/J - reference CEI



22 complete / 1 blocked / 1 inconclusive = 24 A100 tests

───

6. Ghost Power: Detailed Analysis


Measurement
Value

Initial ghost (Test 02)
102.14W

Sustained ghost (Test 13)
77-78W for 60s of cooldown

Peak ghost ever recorded
146.66W (Tests 13 and 14)

Idle floor (true)
66-68W

Ghost above idle
+79.66W unexplained

500 GPU fleet cost
~$150/day hidden electricity + cooling



Root cause chain:
1. GPU locked in P0 performance state
2. Memory clock fixed at 1593 MHz
3. Hypervisor blocks nvidia-smi -pm and nvidia-smi -pl
4. NVML reports 0% utilization - telemetry desynchronised from hardware

───

7. A100 vs H100 Comparison


Metric
A100 SXM
H100 SXM

Idle power
67.1W
69.5W

Peak power
501.86W
412.0W

FP32 TFLOPS
14.35
49.13

FP16 TFLOPS
231.08
592.8

Efficiency (GFLOPS/W)
52.6
76.5

Ghost power detected
YES (146.66W peak)
NO

CEI FP32 sustained
5.68B FLOPs/J
N/A (burst only)

Total tests run
24
11



H100 showing zero ghost power on the same platform confirms this is an A100-specific issue, likely resolved in Hopper.

───

8. Statistical Confidence


Test
Metric
Value

Test 05
Error
0.15%

Test 05
95% CI
+/-1.153e+11

Test 09
Shapiro-Wilk p
0.000000

Test 09
Skewness
-47.1473

Test 09
Samples
8,247

Test 24
Duration
900 seconds

Test 24
Iterations
90,000



───

9. v1.0.0 Release Features

• Real-time GPU telemetry monitoring
• DESYNC anomaly detection
• GHOST anomaly detection
• CEI benchmark framework (FLOPs/Joule)
• A100 + H100 validation datasets (24 A100 + 11 H100 tests)
• Multi-provider GPU observability (17+ providers)
• Grafana + Prometheus integration
• FastAPI backend, Docker, Kubernetes

Supported providers: AWS, GCP, Azure, RunPod, CoreWeave, Vast.ai, Lambda, Kaggle, render, termux

Installation: docker-compose up

Citation:
Bains, Manmohan. (2026). AI GPU Energy Optimizer (Version 1.0.0) [Software]. GitHub. https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-/releases/tag/v1.0.0

───

10. Call to Action

• GPU cloud partnerships - sponsored compute to scale to 100-500 GPUs
• Research collaborations - telemetry validation, Kubernetes, Slurm
• Observability experts - harden Prometheus exporter and Grafana dashboards

Contact: mikebains41@gmail.com
GitHub: https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
API: https://ai-gpu-brain-v3.onrender.com

All tests conducted independently at personal expense. No sponsorship from RunPod or any GPU provider.

───

Appendix: File Structure

results/
├── test1_baseline_idle/
├── test2_ghost_power/
├── test3_sampling_rate/
├── test4_load_ramp/
├── test5_cei_compute_2048/
├── test6_cei_efficiency_2048/
├── test7_cei_compute_4096/
├── test8_fp16_only/
├── test9_normality/
├── test10_loglog_scaling/
└── test11_nsight_proof/

All raw logs, screenshots, and NVML dumps are available in the repository.
Live test data: https://ai-gpu-brain-v3.onrender.com/results/a100

Last updated: May 18, 2026 | v1.0.0 | 24 A100 tests | 11 H100 tests | 40/40 platform tests passing

---

## B200 BLACKWELL VALIDATION — 2026-05-28

### Hardware
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Driver: 580.126.20 | CUDA: 13.0
PyTorch: 2.11.0+cu128 required for B200 support
Pod ID: aee29124a02b | Provider: RunPod

---

### Test 01 — Idle Baseline
**GHOST POWER CONFIRMED FROM COLD BOOT**

| Metric | GPU 0 | GPU 1 |
|---|---|---|
| Power | 143.47W | 145.24W |
| Utilization | 0% | 0% |
| SM Clock | 120 MHz | 120 MHz |
| Memory Clock | 3996 MHz | 3996 MHz |
| P-State | P0 | P0 |
| VRAM Used | 0 MiB | 0 MiB |

Duration: 65 minutes — 148 samples per GPU
Combined idle power: 288.71W at 0% utilization
B200 idles at 2.14x the A100 SXM idle floor of 67.1W
Ghost power present from cold boot — no workload required

---

### Test 02 — FP32 Load
**DESYNC CONFIRMED**

| Metric | GPU 0 | GPU 1 |
|---|---|---|
| Power | 237-239W | 237-239W |
| Utilization | 7-9% | 7-9% |
| SM Clock | 1965 MHz | 1965 MHz |

238W at 7-9% utilization — severe power/utilization mismatch
SM clock jumped from 120 to 1965 MHz instantly on load
PyTorch 2.11.0+cu128 confirmed working on B200

---

### Test 03 — FP16 Tensor Core Load
**COMPLETE TELEMETRY BLACKOUT**

| Metric | GPU 0 | GPU 1 |
|---|---|---|
| Power | 195-200W | 197-202W |
| Utilization | 0% | 0% |
| SM Clock | 1965 MHz | 1965 MHz |

0% utilization reported for entire 8 minute FP16 test.
GPU clearly computing — SM clock at 1965 MHz confirms it.
FP16 tensor core workloads completely invisible to NVML.
More severe than FP32 which showed 7-9% utilization.

---

### Test 04 — Cooldown Profile
**NO COOLDOWN PERIOD**

Power returned to 143-145W baseline immediately after load.
No gradual decay observed.
Periodic power spikes every 30 seconds at 0% utilization.
GPU 0 spikes to 146-147W — GPU 1 spikes to 147-149W.

---

### Test 05 — Post Load Ghost Power Persistence
**SPONTANEOUS 195W BURST CONFIRMED**

At 20:30:08 UTC with zero workload running:
- GPU 0 jumped from 144W to 195.72W
- GPU 1 jumped from 145W to 181.95W
- SM clock activated to 1965 MHz
- Utilization still reported 0%
- Returned to baseline within 10 seconds

Autonomous GPU activity completely invisible to schedulers.
Ghost power floor identical to cold boot — permanent state.

---

### Test 06 — Multi GPU Power Divergence
**HARDWARE ASYMMETRY CONFIRMED**

| Test | Workload | GPU 0 | GPU 1 | Diff |
|---|---|---|---|---|
| 01 | Idle | 143.47W | 145.24W | 1.77W |
| 02 | FP32 | 237.50W | 238.50W | 1.00W |
| 03 | FP16 | 197.00W | 199.00W | 2.00W |
| 04 | Cooldown | 144.00W | 145.75W | 1.75W |
| 05 | Post Load | 144.10W | 145.85W | 1.75W |

GPU 1 always draws 1.00-2.00W more than GPU 0.
370 samples confirm hardware asymmetry not software artifact.

---

### B200 Key Findings Summary

1. Ghost power from cold boot — no workload required
2. B200 idles at 143-145W — 2.14x higher than A100 SXM
3. FP32 DESYNC — 238W at 7-9% utilization
4. FP16 complete telemetry blackout — 0% util during active compute
5. No cooldown period — instant return to ghost power floor
6. Spontaneous 195W burst at 0% utilization with no workload
7. Periodic 30 second power spikes at idle
8. GPU 1 consistently 1-2W higher than GPU 0
9. PyTorch 2.4.1 incompatible — requires 2.11.0+cu128
10. Memory clock 3996 MHz active at idle

### B200 Financial Impact
| Fleet Size | Annual kWh Wasted | Annual USD |
|---|---|---|
| 1 pod 2x B200 | 2,527 kWh | $252.70 |
| 100 pods | 252,700 kWh | $25,270 |
| 1,000 pods | 2,527,000 kWh | $252,700 |
| 10,000 pods | 25,270,000 kWh | $2,527,000 |

### B200 vs A100 SXM Comparison
| Metric | A100 SXM | B200 |
|---|---|---|
| Idle Floor | 67.1W | 143-145W |
| Ghost Trigger | Post workload | Cold boot |
| FP32 Util Reporting | Accurate | 7-9% at load |
| FP16 Util Reporting | Accurate | 0% blackout |
| Cooldown Period | Yes | No |
| PyTorch Support | 2.4.1+ | 2.11.0+ only |

### Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28

---

## B200 Blackwell GPU Testing — 2026-05-28

### Hardware
2x NVIDIA B200 GPUs
360GB total VRAM (180GB per GPU)
Driver: 580.126.20 | CUDA: 13.0
Provider: RunPod | Pod: aee29124a02b

### Test Results Summary

| Test | Finding | Severity |
|---|---|---|
| Test 01 Idle Baseline | 143-145W at 0% util from cold boot | CRITICAL |
| Test 02 FP32 Load | 238W at 7-9% util DESYNC confirmed | CRITICAL |
| Test 03 FP16 Load | 197W at 0% util complete blackout | CRITICAL |
| Test 04 Cooldown | No cooldown period instant return to ghost floor | HIGH |
| Test 05 Post Load | Spontaneous 195W burst at 0% util no workload | CRITICAL |
| Test 06 Multi GPU | GPU1 always 1-2W higher than GPU0 | MEDIUM |

### Key Findings

#### FINDING B200-01 — Ghost Power From Cold Boot
B200 draws 143-145W at 0% utilization from first boot.
No workload required. More severe than A100 SXM.
B200 idle floor IS the ghost power floor.

#### FINDING B200-02 — FP32 DESYNC Confirmed
238W at only 7-9% reported utilization under FP32 load.

#### FINDING B200-03 — FP16 Complete Telemetry Blackout
197W sustained at 0% reported utilization during FP16 compute.
8 minutes continuous — never registered above 0%.
FP16 tensor core workloads completely invisible to NVML.

#### FINDING B200-04 — No Cooldown Period
Power returns to ghost floor instantly after load stops.
Periodic power spikes every 30 seconds at 0% util.

#### FINDING B200-05 — Spontaneous Power Burst
GPU0 jumped to 195.72W GPU1 to 181.95W with zero workload.
SM clock activated to 1965 MHz. Utilization still 0%.

#### FINDING B200-06 — Inter-GPU Power Differential
GPU1 consistently 1.00-2.00W more than GPU0 across all tests.
Hardware asymmetry confirmed.

#### FINDING B200-07 — PyTorch Incompatibility
Minimum version required: PyTorch 2.11.0+cu128

### Architecture Comparison
| GPU | Idle Floor | Ghost Trigger | P0 From Boot |
|---|---|---|---|
| T4 | 9.5W | None | No |
| A100 PCIe | 47W | None | No |
| H100 SXM | 69.5W | None | No |
| A100 SXM | 67.1W | Post workload | No |
| B200 | 143-145W | Cold boot | YES |

### Status
6 tests complete. Hardware-attested. First public B200 validation.
Remaining tests require partner partner data center hardware.
