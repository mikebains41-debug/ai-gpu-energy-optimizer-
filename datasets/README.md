# GPU Energy Optimizer — Validated Hardware Datasets

Author: Manmohan (Mike) Bains
Contact: mikebains41@gmail.com
Project: GPU Energy Optimizer v2.0
https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-

## Overview
Hardware-attested GPU telemetry datasets across 7 architectures.
All tests conducted on real hardware at personal expense.
No simulations. No estimates. Physical measurements only.
Provider: RunPod

---

## Dataset Structure
Each test folder contains 5 files:
- SUMMARY.md — executive summary
- metrics.json — structured key metrics
- evidence.json — full evidence chain
- raw_data.csv — raw nvidia-smi readings
- README.md — full technical report

---

## B200 SXM — NVIDIA Blackwell 2x GPU (2026-05-28)
Hardware: 2x NVIDIA B200 | 360GB VRAM | Driver 580.126.20
Provider: RunPod | Pod: aee29124a02b

| Test | Finding | Status |
|---|---|---|
| test_01_idle_baseline | 288W combined at 0% util from cold boot | COMPLETE |
| test_02_fp32_load | 238W at 7-9% util — DESYNC confirmed | COMPLETE |
| test_03_fp16_load | 197W at 0% util — complete telemetry blackout | COMPLETE |
| test_04_cooldown | No cooldown — instant return to ghost floor | COMPLETE |
| test_05_post_load_ghost | Spontaneous 195W burst at 0% util no workload | COMPLETE |
| test_06_multi_gpu_divergence | GPU1 always 1-2W higher than GPU0 | COMPLETE |

---

## A100 SXM — NVIDIA Ampere
Hardware: A100 SXM 40GB | Provider: RunPod
Tests: 24 validated hardware tests

| Finding | Value |
|---|---|
| Ghost power | 146.66W at 0% utilization |
| Idle floor | 67.1W |
| CEI | 5.68B FLOPs/joule |
| True CEI corrected | 4.12B FLOPs/joule — 27.5% worse than reported |
| FP16 average | 482.7W |
| FP32 average | 302W |
| Severe desync event | 357W documented |
| P0 state lock | Confirmed post-load |
| Hypervisor | Blocks persistence mode and power cap |

---

## H100 SXM — NVIDIA Hopper
Hardware: H100 SXM | Provider: RunPod
Tests: 11 validated hardware tests

| Finding | Value |
|---|---|
| Ghost power | NONE — clean architecture |
| Idle floor | 69.5W |
| CEI | 76.5 GFLOPS/W — 2x A100 |
| FP32 | 47 TFLOPS — 3.1x faster than A100 |
| FP16 | 592.8 TFLOPS — 3.87x faster than A100 |
| Samples | 22,378 — normal distribution confirmed |

---

## Other Validated GPUs

| GPU | Idle Floor | Ghost Power | Tests |
|---|---|---|---|
| A100 PCIe | 47W | None | 2 |
| T4 | 9.5W | None | 1 |
| A40 | 30.4W | None | 1 |
| RTX 4090 | 20W | None | 1 |

---

## Architecture Comparison

| GPU | Idle Floor | Ghost Power | Ghost Trigger | P0 From Boot |
|---|---|---|---|---|
| T4 | 9.5W | None | None | No |
| RTX 4090 | 20W | None | None | No |
| A40 | 30.4W | None | None | No |
| A100 PCIe | 47W | None | None | No |
| H100 SXM | 69.5W | None | None | No |
| A100 SXM | 67.1W | 146.66W | Post-load | No |
| B200 2x GPU | 143-145W | From boot | Cold boot | YES |

---

## Total Validated Tests
- A100 SXM: 24 tests
- H100 SXM: 11 tests
- B200 2x GPU: 6 tests
- Other GPUs: 5 tests
- Total: 46 validated hardware tests

---

## Live API
https://ai-gpu-brain-v3.onrender.com/docs
35 public hardware tests queryable via API

---

## Pending — Partner Data Center Access
- 48hr sustained A100 tests
- 48hr sustained H100 tests
- 48hr sustained B200 tests
- Multi-GPU 4x configurations
- MIG profiling on H100

---

## License
Data: Creative Commons Attribution 4.0
Code: Source Available — see LICENSE
2026 Manmohan Bains
