# The Ghost Power Anomaly and VRAM Residual Vulnerability: Hardware-Measured Evidence of GPU Telemetry Failure Across Seven NVIDIA Architectures

**Author:** Manmohan (Mike) Bains
**Original research period:** May 19 – June 12, 2026
**Document revision:** v2 — restructured June 2026
**Contact:** mikebains41@gmail.com
**Repository:** https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
**Live API:** https://ai-gpu-brain-v3.onrender.com/docs
**Related:** CVE Request 2048350 (filed with MITRE, 2026-05-31)

> **Revision note:** This document consolidates and supersedes the original multi-part research log (Parts I–IX, XI), which was published incrementally between May 19 and June 12, 2026. The underlying findings are unchanged; this revision removes redundant executive summaries, tightens claims that the original log stated more strongly than the evidence supports, and adds an explicit limitations section. Anyone citing specific figures should treat this version as authoritative over the original dated parts.

---

## Executive Summary

Standard GPU telemetry — `nvidia-smi`, the NVML library underlying nearly every monitoring tool (DCGM, Prometheus exporters, Datadog, cloud billing dashboards), and the cloud dashboards built on top of it — assumes that reported utilization is a reliable proxy for GPU activity and that VRAM is fully reclaimed when a process exits. Across 72+ hardware tests on seven NVIDIA GPU architectures, both assumptions were found to be false in measurable, reproducible ways.

Two distinct findings emerged, one concerning energy observability and one concerning security:

**Ghost power:** GPUs in the SXM form factor draw substantial, sustained power while NVML reports 0% utilization. This ranges from 65–146W on A100 SXM (Ampere) to as high as 549–574W on B200 (Blackwell) immediately after a workload exits. The magnitude of this effect correlates with HBM memory clock frequency, which does not scale down at idle on affected architectures. Critically, H100 SXM (Hopper, HBM2e) shows no ghost power at all, while H200 SXM (also Hopper, but HBM3e) does — indicating the effect is tied to specific HBM generations rather than being a universal property of the SXM form factor.

**VRAM residual (the security-relevant finding):** After a process exits using the standard PyTorch cleanup sequence (`del`, `gc.collect()`, `torch.cuda.empty_cache()`), 382–728MB of VRAM remains allocated and unreadable as "in use" by NVML, which reports 0% memory utilization throughout. This residual is confirmed across A100, H100, H200, and B200 SXM architectures, and is absent on every PCIe architecture tested (A100 PCIe, T4, RTX 4090). A hard `SIGKILL` forces the OS to zero the memory; a graceful exit does not. On H200, a related cross-GPU effect was also observed: compute activity on one GPU left 528MB of residual data on a second GPU in the same pod that ran no compute workload at all.

In a multi-tenant cloud environment, where physical GPU hardware is reassigned between customers sequentially, this residual is — in principle — readable by the next tenant assigned to the same hardware, using standard memory inspection. **This document does not yet include a proof-of-concept demonstrating actual data recovery from another tenant's residual memory; that is identified as the highest-priority next step in the Limitations section below.** Absent that, this finding should be read as a confirmed, hardware-measured observability and memory-management defect with a plausible but not yet directly demonstrated data-exposure pathway.

Both findings are invisible to every monitoring tool built on NVML, including DCGM, Prometheus, Datadog, and cloud provider billing/security dashboards.

A subset of the ghost power finding (H200, idle and full-load power draw) was independently reproduced inside a verified Intel TDX confidential-computing enclave in collaboration with Serial Alice (Sirius GreenTech), with measurement hashes cryptographically bound to the hardware attestation quote and anchored on the Polygon blockchain. This is described in full, with an explicit statement of what is and is not attested, in Section 6.

---

## 1. Methodology

All tests were conducted independently, at personal expense, with no sponsorship, primarily on RunPod containerized GPU infrastructure (NVIDIA A100, H100, H200, and B200 SXM; A100 PCIe, T4, and RTX 4090 for PCIe comparison). One result set (Section 6) was additionally validated inside a Phala Network TDX confidential VM in collaboration with Serial Alice/Sirius GreenTech.

The test harness used NVML (via `nvidia-smi` subprocess calls; `pynvml` was used only inside the TDX environment, per its provider's stack), custom Python workload generators (PyTorch matrix operations at varying precision and size), and continuous power/utilization/memory polling at sampling intervals from 10ms to 1s.

As of June 12, 2026: **72+ validated tests across 7 architectures**, covering idle baselines, load ramps, sampling-rate sensitivity, sustained ghost-power windows, VRAM allocation/residual tests with both graceful and forced (`SIGKILL`) process termination, cross-GPU isolation tests, and one TDX-attested reproduction. All raw logs, JSON summaries, and screenshots are maintained in a private repository (available on request); a public subset is queryable via the live API.

**A note on the testing environment:** all results in Sections 2–5 were collected on containerized cloud infrastructure (RunPod), not bare physical hardware with no hypervisor layer. The findings are hardware-measured (the power and memory figures come directly from NVML/the GPU, not from a simulation), but independent confirmation on true bare-metal hardware — with no virtualization layer between the test process and the silicon — has not yet been completed and is identified as a priority in Section 7.

---

## 2. The Ghost Power Anomaly

### 2.1 Definition and Initial Discovery

The anomaly: a GPU reporting 0% utilization while drawing power substantially above its true idle floor, for sustained periods (confirmed up to 20 minutes continuous in early A100 testing, and indefinitely / without recovery on B200 — see 2.4).

On A100 SXM, the true idle floor (confirmed across multiple independent idle-baseline tests) is 65–69W. After a heavy workload (FP16 or FP32 matrix operations) completes, power was repeatedly measured at 146.66W while NVML continued to report 0% utilization — a persistent +79.66W gap with no corresponding utilization signal, lasting in one test 20 continuous minutes without returning to the true idle floor.

### 2.2 Cross-Architecture Comparison

| GPU | Generation | HBM | Idle Floor | Ghost Power | Trigger | NVML Behavior |
|---|---|---|---|---|---|---|
| T4 | Turing | GDDR6 | 9.5W | None | — | Accurate |
| RTX 4090 | Ada | GDDR6X | 20W | None | — | Accurate |
| A40 | Ampere | GDDR6 | 30.4W | None | — | Accurate |
| A100 PCIe | Ampere | HBM2e | 47W | None | — | Accurate |
| A100 SXM | Ampere | HBM2e | 65–69W | 79.66W excess (→146.66W) | Post-load | Reports 0% util throughout |
| H100 SXM | Hopper | HBM2e | 69.5W | **None** | — | Accurate |
| H200 SXM | Hopper | HBM3e | ~74W | 79–136W excess | Post-load | Reports 0% util throughout |
| B200 SXM | Blackwell | HBM3e | 143–145W | Up to 574W spike on exit | **Cold boot** (no workload needed) | Reports 0% util; FP16 workloads completely invisible |

The clean result on H100 SXM is the most important data point in this table: it rules out "SXM form factor" or "presence of HBM" as the explanation on its own, since H100 SXM has both and shows no ghost power. The pattern that best fits the data is HBM-generation-specific: HBM2e on H100 is clean; HBM2e on A100 (an earlier, lower-clocked implementation) is not; HBM3e on both H200 and B200 is not.

### 2.3 Root Cause: Memory Clock Behavior

Detailed clock telemetry on A100 SXM (138 samples across idle, load, and post-load states) shows that while SM (streaming multiprocessor) clock scales normally with workload — dropping to ~210MHz at idle, rising to 1100–1400MHz under load — memory clock remained fixed at 1593MHz in every single sampled state, including full idle.

| GPU | Memory Clock | SM Clock (idle) | Ghost Power |
|---|---|---|---|
| A100 SXM | 1593 MHz (constant) | 210 MHz | 65–146W |
| B200 | 3996 MHz (constant) | 120 MHz | 143–574W |

B200's memory clock is roughly 2.5x A100's, and its ghost power is roughly 2–4x higher depending on which B200 measurement is used for comparison. This is suggestive of a relationship between memory clock frequency and ghost power magnitude, but it is **based on two architectures and should not be read as a confirmed general law.** A controlled test directly varying memory clock on a single architecture (if exposed by the vendor) or additional architecture data points would be needed to establish this more rigorously. We flag this explicitly because the original research log described this as "a direct causal relationship confirmed across two architectures," which overstates what two data points can establish.

A separate single-data-point observation supports the "memory clock, not data content" framing: ghost power magnitude was unchanged whether 807MB of VRAM was actively loaded or the GPU held 0MB — i.e., the effect does not appear to depend on what is stored in memory, only on the memory subsystem's clock state. This too is one comparison, not an exhaustive test, and should be read as preliminary.

### 2.4 B200: A More Severe and Qualitatively Different Pattern

B200 (Blackwell) departs from every other architecture tested in three ways:

1. **Ghost power from cold boot**, with no prior workload required — 143–145W per GPU (288W combined for 2x B200) measured from first power-on.
2. **No recovery state.** Every other architecture showed at least a partial return toward idle after a workload. B200's floor permanently shifts upward after any workload — from ~144W to 196–202W — and does not recover for the life of the pod. This means each subsequent tenant or workload on a B200 instance inherits an elevated power floor caused by whatever ran before it, with no mechanism to detect or attribute this.
3. **A spike of 549–574W at 0% reported utilization** measured immediately after a process exit — the largest ghost power event recorded across all seven architectures, more than 200W above the largest comparable event on A100 SXM.

A separate, related finding: FP16 tensor-core workloads on B200 report 0% utilization for the *entire* duration of active compute, while SM clock (1965MHz) confirms the GPU is actively computing. Since B200 is marketed primarily for inference, and inference commonly uses FP16, this means a large share of B200's primary intended use case may be invisible to NVML-based monitoring. This was observed on driver version 580.126.20 with CUDA 13.0 and PyTorch 2.11.0+cu128 — an early-release software stack for a newly launched architecture. It is possible some of this behavior is a driver/firmware immaturity issue rather than a permanent hardware characteristic; this is called out explicitly as an open question in Section 7, and we recommend NVIDIA confirm which category it falls into.

---

## 3. VRAM Residual: The Security-Relevant Finding

### 3.1 Discovery and the SIGKILL Mitigation

Initial VRAM testing on A100 SXM found that after a workload allocating 807MB of VRAM exits using the standard PyTorch cleanup sequence (`del`, `gc.collect()`, `torch.cuda.empty_cache()`), 382MB remains allocated — NVML reporting 0% memory utilization throughout, including during active allocation.

Follow-up testing isolated the determining factor precisely: **the residual depends on how the process is terminated, not on the workload itself.**

| Cleanup Method | A100 SXM Residual | VRAM Cleared? |
|---|---|---|
| `del` + `gc.collect()` + `empty_cache()` (graceful) | 457–465 MB | No |
| `SIGKILL` (hard kill) | 0 MB | **Yes** |

This localizes the root cause to PyTorch's CUDA memory allocator: PyTorch maintains an internal memory cache that survives logical tensor deletion, and the driver does not zero physical VRAM pages when that cache is released through the normal API. A hard kill bypasses this entirely — the OS kernel forces immediate GPU memory reclamation on process termination, and the driver zeros the pages. This gives cloud operators an immediate, concrete mitigation available today: enforce SIGKILL (rather than allowing graceful shutdown) on tenant process exit.

### 3.2 Cross-Architecture Residual

| GPU | HBM | Graceful-Exit Residual | SIGKILL Residual |
|---|---|---|---|
| A100 SXM | HBM2e | 457–465 MB | 0 MB |
| H100 SXM | HBM2e | 457 MB | not tested |
| H200 SXM | HBM3e | 527–629 MB (single workload); 1,630 MB (full multi-phase profile) | not tested |
| B200 SXM | HBM3e | 628–728 MB (fixed regardless of precision) | not tested |
| A100 PCIe | GDDR6 | 0 MB | — |
| T4 | GDDR6 | 0 MB | — |
| RTX 4090 | GDDR6X | 0 MB | — |

The pattern is consistent: every tested SXM architecture with HBM shows residual; every tested PCIe architecture with GDDR-family memory shows none. HBM generation also predicts magnitude — HBM2e leaves 457–465MB, HBM3e leaves 529–1,630MB depending on workload complexity — though, as with the ghost power memory-clock hypothesis, this is based on four data points and should be treated as a strong pattern rather than an exhaustively proven law.

The residual does not self-clear over time; it persists until overwritten by a subsequent workload.

### 3.3 Cross-GPU Isolation Failure (H200)

A full multi-phase test profile on a 2x H200 SXM pod produced a result not seen in single-GPU testing: GPU1, which ran no compute workload at all during the test, retained 528MB of residual VRAM that originated from compute activity on GPU0.

| Phase | GPU0 (active) | GPU1 (idle throughout) |
|---|---|---|
| Baseline | 1 MB | 1 MB |
| After GPU0 compute, before cleanup | 19,030 MB | 910 MB |
| After graceful cleanup | 1,102 MB | **528 MB** |

This is a meaningfully different and broader exposure pathway than same-GPU sequential residual: it suggests that in multi-GPU pod allocations, data can cross between GPUs within the same allocation boundary, not only between sequential tenants on one GPU. We have one test profile demonstrating this; it has not yet been characterized across other architectures or repeated to establish how reliably it reproduces, and that replication is listed in Section 7.

### 3.4 NVML Blindness Compounds the Risk

Across every layer tested, NVML's reporting failed to reflect reality:

| Layer | NVML Reports | Measured Reality |
|---|---|---|
| Power vs. compute utilization | 0% util | 65–574W draw |
| Memory utilization during active allocation | 0% util.memory | Up to 19,030 MB loaded |
| VRAM residual after exit | 0% util.memory | 382–1,630 MB resident |
| Cleanup process exit code | 0 (success) | Up to 1,630 MB still resident |

Every cloud provider security or billing dashboard built on NVML — which is to say, nearly every one in production use — will show a clean, idle GPU at the exact moment hundreds of megabytes to over a gigabyte of a previous workload's data remains physically resident.

### 3.5 Comparison to Prior Art: LeftoverLocals (CVE-2023-4969)

Trail of Bits' January 2024 disclosure (CVE-2023-4969, "LeftoverLocals") demonstrated that GPU local memory — registers and shared memory used within a single kernel invocation — could leak between kernel invocations on the same GPU, within a single session.

This research describes a different and substantially larger attack surface, for three concrete reasons:

1. **Scope of memory affected.** LeftoverLocals concerned local registers and shared memory, typically kilobytes to low megabytes in scale. This research concerns full VRAM allocations, measured in hundreds of megabytes to over a gigabyte.
2. **Persistence boundary.** LeftoverLocals leakage occurred within a single user's session, between kernel calls they controlled. The VRAM residual finding persists *across a full process exit*, after the allocating process has terminated entirely and a completely different tenant's process may be scheduled onto the same physical GPU.
3. **Detectability.** LeftoverLocals was at least partially observable through existing GPU profiling approaches. The VRAM residual finding is invisible to every NVML-based monitoring tool, including the ones cloud providers use for their own security dashboards — there is currently no existing tool, to our knowledge, that would alert an operator to this state.

In short: where LeftoverLocals showed that a workload could leak into itself, this finding shows that a workload can leak into a different tenant entirely, at a much larger scale, with no existing detection mechanism.

---

## 4. Carbon and Regulatory Implications

Ghost power has a second-order consequence beyond direct electricity cost: it inflates Scope 2 (operational energy) emissions in a way that is not visible to standard carbon accounting, which typically derives energy estimates from reported utilization.

A single A100 SXM's estimated annual carbon footprint, combining Scope 2 (operational, ~730 kg CO2) and Scope 3 (embodied/manufacturing, ~1,600 kg CO2), is approximately 2,330 kg CO2/year on a global-average grid, with Scope 3 representing roughly two-thirds of the total. On cleaner grids (e.g., BC Canada hydro, Portuguese solar), Scope 3 becomes a much larger share of total emissions — over 90% in both cases by our estimate — meaning ghost power elimination becomes proportionally *more* impactful on cleaner grids, not less, since it is one of the few remaining operational levers once the grid itself is decarbonized.

**On the fleet-scale cost projections:** the original research log estimated annual electricity cost from ghost power at various fleet sizes (e.g., ~$2.1M/year for a 100,000-GPU A100 fleet), calculated by applying the measured excess wattage continuously, 24/7, across every GPU in the fleet. This is a useful upper-bound / theoretical-maximum figure, but it assumes every GPU in the fleet has run a workload that triggers the post-load ghost state and is never rebooted — an assumption we have not validated against real fleet telemetry. We do not have sampling data on what fraction of GPUs in a representative production fleet are actually in the ghost-power state at any given time, and we are not presenting one here. Until that duty-cycle data exists, fleet-level dollar figures should be read as a ceiling, not an expected value, and any party relying on this for a business case should treat it as directional rather than load it into a precise ROI calculation.

---

## 5. Regulatory Landscape

The following frameworks across 14 jurisdictions create reporting obligations for GPU energy consumption and emissions where hardware-measured (rather than utilization-estimated) telemetry would materially improve compliance accuracy: EU AI Act Annex XI (PUE/WUE KPIs), US EO14110 and SB253 (Scope 1-2-3 mandatory disclosure), Canada's Bill C-27 (AIDA, net-zero 2050 alignment), Japan's Energy Conservation Act (PUE 1.4 target by 2030), South Korea's AI Basic Act (enforcement from January 2026), Singapore's Model AI Governance Framework (PUE 1.3 target), Australia's mandatory PUE 1.4 requirement (effective July 2025), and equivalent frameworks in Mexico, Brazil, China, India, the UAE, and Saudi Arabia. This list is included to establish relevance, not as a claim of legal analysis; we are not lawyers, and any organization evaluating compliance exposure should consult its own counsel.

---

## 6. Hardware-Attested Validation: Intel TDX Enclave and On-Chain Anchoring

A subset of the ghost power finding (H200 idle and full-load power measurements) was independently reproduced inside a verified Intel TDX confidential-computing enclave, in collaboration with Serial Alice (Sirius GreenTech). Measurement sample hashes were cryptographically bound into the hardware TDX attestation quote, and the resulting certificates anchored on the Polygon blockchain — providing a tamper-evident, publicly verifiable record, in contrast to the self-reported software telemetry used elsewhere in this document.

**What this attests:**

| Property | Status | Evidence |
|---|---|---|
| Intel TDX enclave genuine | Verified | TD quote verified, MRTD allowed |
| TCB status | Up to date | Intel-PCS collateral |
| Measurement bound to quote | Yes | Sample hash in REPORT_DATA; `tee_quote_bound = true` |
| Certificate integrity | Signed (Ed25519) | — |
| Public verifiability | Anchored on Polygon | Blocks 88401586, 88402187 |

**Attested H200 results:** idle baseline 80.3W; full load 592.84W; ghost fraction (idle/load) 13.6% — measured inside the verified enclave.

**What this does not yet attest, stated plainly:** the trust score reached for this measurement (0.8, the "hardware_attested" tier in Serial Alice's scoring model) reflects verification of the *execution environment* — that the TDX enclave is genuine and the sample hash is bound to it. It does not yet reflect independent attestation of the *energy measurement source itself*: the power readings are NVML values captured from inside the enclave, and a signed energy exporter (which would attest the measurement pipeline, not just the environment) was not present in this submission. The accurate framing is: these measurements were executed inside a genuine, verified, tamper-evident hardware environment — not that the energy values themselves carry independent hardware attestation. Closing the signed-exporter gap is the explicit next milestone for this collaboration.

This attestation work applies to the energy/power finding only. It has no bearing on the VRAM residual finding, and should not be read as extending hardware attestation to that result.

### Additional Finding: Detecting Covert Workloads via Power Fingerprint

A follow-up test using the same TDX-attested H200 setup examined a different question: can an unauthorized background process hide inside an otherwise legitimate, certified workload? A baseline workload was measured at 657.4W ("clean"). The same workload was then re-run with a covert background process injected, consuming approximately 15% of GPU capacity — representative of an unauthorized workload such as cryptocurrency mining running alongside a tenant's legitimate job. Power draw rose to 663.2W ("with covert process"), a difference of 5.8W, captured and certified by two separate attestation certificates anchored at the same Polygon block.

This is a single test on one workload pair and should be read as preliminary, not as a general detection threshold — we do not yet know how this signal scales with covert workload size, varies across GPU architectures, or holds up against a process specifically designed to mask its power signature. It is included here because it is hardware-attested and represents a distinct, additional security application of power telemetry beyond the ghost power and VRAM residual findings described elsewhere in this document: where ghost power and VRAM residual concern data leakage and energy accounting, this finding concerns detecting unauthorized compute activity hidden within an apparently normal, certified workload.

---

## 7. Limitations and Priority Next Steps

This research is hardware-measured and reproducible, but several gaps remain open. They are listed here explicitly rather than implied away, in descending order of priority:

1. **No attack proof-of-concept yet exists.** Section 3 describes what *could* plausibly be present in residual VRAM (model weights, training data, API keys, inference outputs) based on what a typical workload places in GPU memory, but no test to date has demonstrated a second process actually reading recoverable, meaningful data out of another process's residual allocation. This is the single highest-priority next step: a concrete demonstration of "Process B recovers N bytes of Process A's data after Process A exits" would move this finding from a confirmed observability/memory-management defect with a plausible exposure pathway to a directly confirmed data-exposure vulnerability.

2. **All testing to date has been on virtualized/containerized cloud infrastructure**, not on bare physical hardware with no hypervisor present. While the GPU-level measurements (power, memory) are hardware-sourced regardless of the virtualization layer above them, independent confirmation on true bare metal — particularly for the cross-tenant question — has not yet been completed.

3. **The memory-clock-as-root-cause hypothesis (Section 2.3) is based on two architectures.** It is a reasonable and well-supported pattern, not yet a confirmed general law. Direct confirmation from NVIDIA or HBM vendors (SK Hynix, Samsung) on whether HBM3e's idle clock behavior differs intentionally from HBM2e's would resolve this.

4. **B200 findings were collected on early-release driver/CUDA/PyTorch versions** (driver 580.126.20, CUDA 13.0, PyTorch 2.11.0+cu128) for a newly launched architecture. Some findings — particularly the FP16 telemetry blackout — may be partially or fully addressable in firmware/driver updates rather than being permanent hardware characteristics. We recommend these results be re-validated against current driver versions periodically, and would welcome confirmation from NVIDIA on which findings are architectural versus software-addressable.

5. **Fleet-level cost projections (Section 4) assume a 24/7, fleet-wide duty cycle** that has not been validated against real production fleet telemetry. These figures should be treated as a theoretical ceiling, not an expected value, until real-world sampling data exists.

6. **The cross-GPU isolation finding (Section 3.3) is based on a single test profile** on one 2x H200 pod and has not yet been replicated across other multi-GPU configurations or architectures.

7. **The covert-process detection finding (Section 6) is based on a single test** with one covert workload size (~15% GPU) on one architecture (H200). It is not yet known how the detectable power delta scales with smaller covert workloads, varies across GPU architectures, or holds up against processes deliberately designed to minimize their power footprint.

---

## 8. The GPU Energy Optimizer: Detection Tooling

The open-source AI GPU Energy Optimizer (v1.0.0) was built to detect both findings in production in real time, since neither is visible to existing NVML-based tooling:

- Real-time ghost-power and memory-desync detection (cross-validates `memory.used` against `utilization.memory` and `power.draw` against `utilization.gpu`, rather than trusting either utilization figure alone)
- The Compute Energy Intensity (CEI) benchmark — FLOPs per joule — as a standardized cross-provider efficiency metric (reference value: 5.68B FLOPs/J sustained FP32 on A100 SXM; note that this figure excludes ghost-power periods, and a ghost-power-corrected true CEI was measured at 4.12B FLOPs/J, roughly 27.5% lower)
- Kubernetes/Helm deployment for fleet-scale monitoring, with Prometheus/Grafana integration
- Support for 17+ cloud providers

Live API: https://ai-gpu-brain-v3.onrender.com/docs
Repository: https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-

---

## 9. Call to Action

We are seeking three forms of collaboration:

- **GPU cloud partnerships** — sponsored compute access (particularly true bare-metal access, per Limitation 2 above) to validate the cross-tenant exposure pathway directly.
- **Research collaborations** — with security researchers or academic labs who can help design and execute the attack proof-of-concept described in Limitation 1.
- **NVIDIA and HBM vendor engagement** — to confirm or correct the architectural hypotheses in Sections 2.3 and 7, and to assess whether any findings are addressable via firmware/driver update.

All testing to date has been conducted independently and at personal expense.

**Contact:** mikebains41@gmail.com
**GitHub:** https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-

---

## Appendix A: A100 SXM Complete Test Summary (24 Tests)

| Test | Name | Key Finding |
|------|------|--------------|
| 01 | Idle Baseline | 62.7W @ 0% util |
| 02 | Ghost Power | 102.14W @ 0% util — confirmed |
| 03 | Sampling Rate | Blind spot persists at 1s, 100ms, 10ms |
| 04 | Load Ramp | 357.7W with severe lag at 0% util |
| 05 | CEI Compute 2048 | 14.35 TFLOPS, 0.15% error |
| 06 | CEI Efficiency 2048 | 52.6 GFLOPS/W |
| 07 | CEI Compute 4096 | 15.3 TFLOPS |
| 08 | FP16 Tensor Core | 231.08 TFLOPS, 15 min sustained |
| 09 | Normality Test | p=0.000000, skew=-47.15 |
| 10 | Log-Log Scaling | Peak at 4096 (17.79 TFLOPS) |
| 11 | Observability Validation | 3,044 samples, burst 396–406W |
| 12 | 8192 Load Test | 305–342W @ 100% util |
| 13 | Load + Cooldown (5+6 min) | 146.66W peak @ 0% util |
| 14 | Ghost Power (10+10 min) | 146.66W peak, never returned to true idle |
| 15 | Idle Baseline (15 min) | 67.1W floor, 27°C |
| 16 | Remediation Attempt | Blocked by hypervisor |
| 17 | P-State Retention | P0 + 1593MHz locked post-load |
| 18 | Power vs. Matrix Size | Peak 339.1W at 6144×6144 |
| 19 | FP16, 10 min continuous | 482.7W avg, 1.03e+15 FLOPs |
| 20 | FP16 vs FP32 (quick) | FP16 4.7x faster; FP32 ghost at 137W |
| 21 | FP16 vs FP32 (full) | FP16 3.0x faster; mismatch persists |
| 22 | Persistence Disable | Inconclusive — hypervisor ignored command |
| 23 | Idle Baseline Confirm | 67.1W confirmed |
| 24 | CEI Validation (15 min) | 5.68B FLOPs/J reference value |

22 complete / 1 blocked / 1 inconclusive. 11 H100 SXM tests also completed (idle ~69.5W, peak ~412W, no ghost power detected).

## Appendix B: Full Cross-Architecture Security Matrix

| GPU | HBM | VRAM Residual (graceful) | Max Ghost Power | NVML Blind | Power Recovery |
|---|---|---|---|---|---|
| A100 SXM | HBM2e | 457–465 MB | 357W | No | Partial |
| H100 SXM | HBM2e | 457 MB | 86W | No | Partial |
| H200 SXM | HBM3e | 527–1,630 MB | 136W | No | Partial |
| B200 SXM | HBM3e | 628–728 MB | 549–574W | Yes (FP16 complete blackout) | None |
| A100 PCIe | GDDR6 | 0 MB | 0W | No | Full |
| T4 | GDDR6 | 0 MB | 0W | No | Full |
| RTX 4090 | GDDR6X | 0 MB | 0W | No | Full |

---

**Acknowledgments:** TDX attestation and on-chain anchoring (Section 6) provided in collaboration with Serial Alice / Sirius GreenTech (Nelson Vicente).

**Researcher:** Manmohan (Mike) Bains, Duncan, BC, Canada
