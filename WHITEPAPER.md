# White Paper: The Ghost Power Anomaly – Exposing Hidden GPU Energy Waste and the Case for a New Observability Standard

**Author:** Mike Bains  
**Date:** May 19, 2026  
**Project:** AI GPU Energy Optimizer  
**Contact:** mikebains41@gmail.com  
**Repository:** https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-  
**Live API:** https://ai-gpu-brain-v3.onrender.com/docs  

---

## Executive Summary

Standard GPU telemetry – `nvidia-smi`, Prometheus NVML exporter, and cloud dashboards – assumes that low reported utilization equals low power draw and no useful work. This assumption is **false**. In controlled hardware tests on NVIDIA A100 SXM GPUs, we measured a GPU drawing **146.66 watts** while reporting **0% utilization** for extended periods (11+ minutes). We call this a **GHOST anomaly** – physically impossible telemetry that leads to over‑provisioned clusters, wasted energy, and incorrect scaling decisions.

Furthermore, NVIDIA’s own documentation confirms that **profiling shared GPU resources (MIG partitions) is not supported**, creating a blind spot in multi‑tenant cloud environments where telemetry desynchronisation (DESYNC) can hide silently.

To address this, we have developed an open‑source GPU Energy Optimizer that detects GHOST and DESYNC anomalies in real time, and we propose the **Compute Energy Intensity (CEI)** benchmark – a standardised measure of FLOPs per joule – to enable transparent, cross‑provider energy efficiency comparisons.

This white paper presents the complete methodology, statistical validation, and business case for deploying the GPU Energy Optimizer at scale, and calls for partnerships to validate across 500–1,000 GPUs.

---

## 1. The Problem: GPU Telemetry Lies

Production monitoring tools report **utilization percentage** as a proxy for activity. However, we discovered that an NVIDIA A100 SXM can draw **146.66W** while reporting **0% utilization** across all sampling rates (1s, 100ms, 10ms). This “GHOST anomaly” means:

- **Hidden energy waste** – you pay for compute you cannot see or schedule.
- **Incorrect autoscaling** – the orchestrator believes the GPU is idle and adds more pods, wasting capacity.
- **Faulty benchmarking** – any energy efficiency calculation (e.g., FLOPs per watt) that relies on reported utilization is wrong.

The root cause is a combination of:
- GPU locked in **P0 performance state** after a workload.
- **Memory clock fixed at 1593 MHz** (full speed) even during idle.
- Hypervisor restrictions that block `nvidia-smi -pm` (persistence mode disable) and `nvidia-smi -pl` (power capping).
- **NVML reports 0% utilization** while hardware remains active, causing telemetry desynchronisation.

---

## 2. Methodology: 35 Validated Hardware Tests

All tests were conducted on **RunPod** (NVIDIA A100 SXM 40GB and H100 SXM) at personal expense, with no sponsorship. The test harness used `pynvml`, NVML, and custom Python agents. We executed **24 A100 tests** and **11 H100 tests**, covering:

- Idle baselines (10–15 minutes)
- Ghost power detection (102W, then 146.66W peak)
- Sampling rate sensitivity (1s, 100ms, 10ms – blind spot persists)
- Load ramps (0–100% matrix multiplication)
- CEI compute and efficiency (FP32/FP16, 2048–8192 matrix sizes)
- Normality tests (Shapiro‑Wilk, p=0.000000)
- Log‑log scaling (peak at 4096×4096)
- Extended ghost power cooldown (10+10 minutes, never returned to true idle)
- Remediation attempts (blocked by hypervisor)
- P‑state and memory clock retention (P0 + 1593 MHz locked post‑load)

All raw logs, JSON summaries, and screenshots are available in the private repository (access on request). Public test results are queryable via the live API.

---

## 3. Key Findings

### 3.1 GHOST Power: 146.66W at 0% Utilization

| Test | Duration | Peak Power | Reported Util | Status |
|------|----------|------------|---------------|--------|
| Test 02 | 66 samples | 102.14W | 0% | GHOST confirmed |
| Test 13 | 660 seconds | 146.66W | 0% | GHOST confirmed |
| Test 14 | 1200 seconds | 146.66W | 0% | Never dropped to true idle |

**Idle floor (true)** = 66–68W. Ghost power above idle = **+79.66W unexplained**.

**Cost impact:** At a fleet of 500 GPUs, this hidden waste amounts to approximately **$150/day** in electricity and cooling alone (assuming $0.10/kWh and 24/7 operation). Scheduling inefficiencies add significantly more.

### 3.2 MIG Observability Gap – Confirmed by NVIDIA

NVIDIA’s official MIG user guide states:

> *“Profiling of shared GPU resources is not supported. This is an existing limitation.”*

In multi‑tenant cloud environments (Google Cloud, RunPod, etc.) where MIG partitions are common, telemetry from individual partitions can be desynchronised or incomplete. Our DESYNC detection (high power, near‑zero utilization) and GHOST detection directly address this blind spot.

### 3.3 CEI Benchmark: A Standard for Compute Energy Intensity

We define **Compute Energy Intensity (CEI)** as:


**Reference value (sustained FP32, A100 SXM):** 5.68 B FLOPs/J (Test 24, 900 seconds, 90,000 iterations).

| Tier | CEI (FLOPs/J) |
|------|----------------|
| Excellent | > 10 B |
| Good | 5–10 B |
| Moderate | 1–5 B |
| Poor | < 1 B |

A100 SXM baseline = **Good** tier. H100 efficiency is 45% higher (76.5 vs 52.6 GFLOPS/W).

### 3.4 Statistical Confidence

- Test 05: relative error **0.15%**, 95% CI ±1.153e+11
- Test 09: Shapiro‑Wilk p = **0.000000** (non‑normal distribution, as expected)
- 24 A100 tests: **22 passed, 1 blocked (hypervisor), 1 inconclusive (hypervisor ignored command)**

---

## 4. The GPU Energy Optimizer Solution

The open‑source **AI GPU Energy Optimizer** (v1.0.0) provides:

- **Real‑time GHOST and DESYNC detection** (rules‑based, physics‑validated)
- **CEI benchmarking** across 17+ cloud providers (AWS, GCP, Azure, RunPod, CoreWeave, etc.)
- **Kubernetes / Run:ai integration** for automatic workload eviction on anomaly
- **Grafana + Prometheus** observability stack
- **Lightweight deployment** via `docker-compose up`

All 40 platform validation tests pass. Live API: [ai-gpu-brain-v3.onrender.com/docs](https://ai-gpu-brain-v3.onrender.com/docs)

---

## 5. Business Case & Call to Action

**Immediate opportunity:** Cloud providers (Google Cloud, AWS, etc.) and large GPU fleets are losing money every day to ghost power and telemetry desync. Our open‑source tool already detects these anomalies; what we need is **sponsored compute** (100–500 GPUs) to validate the system at scale and prove the ROI.

**We are seeking:**

- **GPU cloud partnerships** – sponsored compute on A100/H100 (including MIG partitions) to run extended validation.
- **Research collaborations** – with academic or industry labs focusing on GPU telemetry, energy efficiency, or scheduling.
- **Observability experts** – to harden Prometheus exporters and Grafana dashboards for enterprise deployment.

All tests to date were conducted independently at personal expense. We are ready to scale.

**Contact:** mikebains41@gmail.com  
**GitHub:** [mikebains41-debug/ai-gpu-energy-optimizer-](https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-)  
**Live API:** [https://ai-gpu-brain-v3.onrender.com/docs](https://ai-gpu-brain-v3.onrender.com/docs)

---

## Appendix: Complete Test Summary (24 A100 Tests)

| Test | Name | Key Finding |
|------|------|--------------|
| 01 | Idle Baseline | 62.7W @ 0% util |
| 02 | Ghost Power | 102.14W @ 0% util – CONFIRMED |
| 03 | Sampling Rate | Blind spot at 1s, 100ms, 10ms |
| 04 | Load Ramp | 357.7W severe lag at 0% util |
| 05 | CEI Compute 2048 | 14.35 TFLOPS, 0.15% error |
| 06 | CEI Efficiency 2048 | 52.6 GFLOPS/W |
| 07 | CEI Compute 4096 | 15.3 TFLOPS |
| 08 | FP16 Tensor Core | 231.08 TFLOPS – 15 min sustained |
| 09 | Normality Test | p=0.000000, skew=-47.15 |
| 10 | Log-Log Scaling | Peak at 4096 (17.79 TFLOPS) |
| 11 | Observability Validation | 3,044 samples, burst 396-406W |
| 12 | 8192 Load Test | 305-342W @ 100% util |
| 13 | Load + Cooldown 5+6 min | **146.66W peak @ 0% util** |
| 14 | Ghost Power 10+10 min | **146.66W peak, never true idle** |
| 15 | Idle Baseline 15 min | 67.1W floor, 27C |
| 16 | Remediation Attempt | BLOCKED (hypervisor) |
| 17 | P-State Retention | P0 + 1593 MHz locked post‑load |
| 18 | Power vs Matrix Size | Peak 339.1W at 6144x6144 |
| 19 | FP16 10 min Continuous | 482.7W avg, 1.03e+15 FLOPs |
| 20 | FP16 vs FP32 Quick | FP16 4.7x faster, FP32 ghost 137W |
| 21 | FP16 vs FP32 Full | FP16 3.0x faster, mismatch persists |
| 22 | Persistence Disable | INCONCLUSIVE (hypervisor ignored) |
| 23 | Idle Baseline Confirm | 67.1W confirmed |
| 24 | CEI Validation 15 min | **5.68B FLOPs/J – CEI reference** |

**22 complete / 1 blocked / 1 inconclusive = 24 A100 tests**  
**11 H100 tests** also completed (idle ~69.5W, peak ~412W, no ghost power detected).

---

**End of White Paper – May 19, 2026**
