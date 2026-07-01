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

Trail of Bits' January 2024 disclosure (CVE-2023-4969, "LeftoverLocals") demonstrated that GPU *local* memory — the on-chip registers and shared memory used by GPU kernels — was not always cleared between uses, letting one process's kernel read data left behind by another process's kernel on a shared GPU. The researchers published a working proof-of-concept that recovered real data across this boundary, including reconstructing another user's LLM session output (up to ~181MB per query on one AMD GPU). The affected vendors were Apple, AMD, Qualcomm, and Imagination; NVIDIA confirmed during the coordinated disclosure that its GPUs were not affected.

The VRAM residual finding in this document is a distinct and complementary issue, not a larger version of the same one. It differs along three axes:

1. **Memory tier.** LeftoverLocals concerned on-chip local/shared memory, typically kilobytes to low megabytes per leak. This finding concerns global VRAM (HBM) allocations, measured at 382MB–1,630MB of residual after a process exits.
2. **Persistence boundary.** LeftoverLocals leaked between kernel invocations on a shared GPU. The residual here persists *across a full process exit* — the allocating process has terminated entirely, and the memory is not zeroed until overwritten or until a hard SIGKILL forces reclamation. Whether a subsequently scheduled tenant can read that residual across a real allocation boundary is the proof-of-concept identified as the top priority in Section 7, and is not yet demonstrated here.
3. **Vendor and form factor.** LeftoverLocals did not affect NVIDIA. This finding is specific to NVIDIA SXM parts with HBM memory and is absent on every PCIe/GDDR part tested — placing it on hardware the prior work did not cover.

A note on maturity, stated plainly: LeftoverLocals is the more developed result — it shipped with a working cross-process exploit recovering real data. This finding is at an earlier stage: a confirmed, hardware-measured memory-management and observability defect, with the cross-tenant exploitation pathway still to be demonstrated (Section 7). The contribution is not "bigger than LeftoverLocals" but "a different memory region, a longer persistence boundary, and a vendor LeftoverLocals left untouched."

---

## 4. Carbon and Regulatory Implications

Ghost power has a second-order consequence beyond direct electricity cost: it inflates Scope 2 (operational energy) emissions in a way that is not visible to standard carbon accounting, which typically derives energy estimates from reported utilization.

A single A100 SXM's estimated annual carbon footprint, combining Scope 2 (operational, ~730 kg CO2) and Scope 3 (embodied/manufacturing, ~1,600 kg CO2), is approximately 2,330 kg CO2/year on a global-average grid, with Scope 3 representing roughly two-thirds of the total. On cleaner grids (e.g., BC Canada hydro, Portuguese solar), Scope 3 becomes a much larger share of total emissions — over 90% in both cases by our estimate — meaning ghost power elimination becomes proportionally *more* impactful on cleaner grids, not less, since it is one of the few remaining operational levers once the grid itself is decarbonized.

**On the fleet-scale cost projections:** the original research log estimated annual electricity cost from ghost power at various fleet sizes (e.g., ~$2.1M/year for a 100,000-GPU A100 fleet), calculated by applying the measured excess wattage continuously, 24/7, across every GPU in the fleet. This is a useful upper-bound / theoretical-maximum figure, but it assumes every GPU in the fleet has run a workload that triggers the post-load ghost state and is never rebooted — an assumption we have not validated against real fleet telemetry. We do not have sampling data on what fraction of GPUs in a representative production fleet are actually in the ghost-power state at any given time, and we are not presenting one here. Until that duty-cycle data exists, fleet-level dollar figures should be read as a ceiling, not an expected value, and any party relying on this for a business case should treat it as directional rather than load it into a precise ROI calculation.

---

## 5. Regulatory Landscape

The following frameworks across 14 jurisdictions create reporting obligations for GPU energy consumption and emissions where hardware-measured (rather than utilization-estimated) telemetry would materially improve compliance accuracy: EU AI Act Annex XI (PUE/WUE KPIs), US EO14110 and SB253 (Scope 1-2-3 mandatory disclosure), Canada's Bill C-27 (AIDA, net-zero 2050 alignment), Japan's Energy Conservation Act (PUE 1.4 target by 2030), South Korea's AI Basic Act (enforcement from January 2026), Singapore's Model AI Governance Framework (PUE 1.3 target), Australia's mandatory PUE 1.4 requirement (effective July 2025), and equivalent frameworks in Mexico, Brazil, China, India, the UAE, and Saudi Arabia. This list is included to establish relevance, not as a claim of legal analysis; we are not lawyers, and any organization evaluating compliance exposure should consult its own counsel.

---


## 6. Independent Validation: Serial Alice — June 27, 2026

In June 2026, Serial Alice (Sirius GreenTech) conducted an independent validation of GPU Energy Optimizer across a battery of 15 tests on a NVIDIA H200 SXM inside an Intel TDX confidential-computing enclave hosted on Phala Cloud. All results are cryptographically signed with Ed25519 (classical) and ML-DSA-65 (FIPS 204 post-quantum) signatures, included in a Merkle batch, and anchored on the Polygon mainnet. Every certificate is independently verifiable at api.serialalice.pt with no account required.

This section reports what Serial Alice attests. What it does not attest is stated explicitly: Serial Alice attests the measurement and its tamper-evidence, not the researcher's interpretation, GPU Energy Optimizer's methodology, or regulatory conformance.

### 6.1 Scope and Method

Hardware: NVIDIA H200 SXM · Intel TDX confidential-compute enclave · Phala Cloud (dstack CVM)
Date: 2026-06-27
Cumulative test duration: 24 hours and above
Total samples: 11,052
Crashes: 0

Two attestation tiers were used. self_reported: Serial Alice signs and anchors GPU Energy Optimizer's own measured values verbatim, providing tamper-evidence for the measurement without independently re-deriving it. hardware_attested: Serial Alice's own agent measures inside the H200 TEE and binds the record to the Intel TDX quote. Two certificates (AGT-M4, AGT-M7) reached this tier — the highest available.

Every certificate was verified across seven independent layers: schema conformance (CEA-2.0), SHA-256 hash, Ed25519 signature, ML-DSA-65 signature, Merkle batch proof, Polygon anchor confirmation, and issuance policy. A certificate is overall_valid only when all seven layers pass. All 15 certificates are overall_valid.

### 6.2 Ghost Power and Idle Floor — Confirmed

The ghost power finding from Section 2 was independently reproduced on H200.

- Idle floor: 80.36W — cert sa-29820cec7f404fcfb9b56ed15e1757ca
- Ghost power cooldown tail at ~0% utilization: 147.96W — cert sa-b2f092b30e3c4196a8afbceffda266ee
- Ghost power excess above idle: ~67.6W (derived)

The cooldown tail of 147.96W at approximately 0% reported utilization — approximately 67.6W above the measured idle floor — is the attested figure for genuine post-workload idle-leak on H200. This is consistent with the A100 SXM finding in Section 2 (146.66W peak ghost power) and confirms the cross-architecture pattern.

A Serial Alice caveat applies to the M2 and M3 sample counts: at 487W workload power, essentially every active sample clears the idle+8W threshold, so the ghost sample count reflects compute power above idle, not isolated idle-leak. The genuine isolated idle-leak figure is the M6 cooldown tail above.

The ghost-threshold inconsistency flagged by Serial Alice — M2 used dynamic idle+8W while the production exporter used a flat 90W constant across six files — was identified and corrected. The dynamic idle+8W threshold is now applied across all test files and the production exporter.

### 6.3 Compute Energy Intensity — Cross-Laboratory Reproduced

- FP32 CEI: 3.178e11 FLOPs/J (tier EXCELLENT) — cert sa-8858266ebbda45ceb240db0fa122a554
- FP32 CEI reproducibility: 3.135–3.187e11 across 5 passes (±1.6%)
- FP32 CEI cross-laboratory: ~4% vs. researcher's separate bare-metal H200 run at 3.288e11
- FP16 CEI inside TDX enclave: 2.846e12 FLOPs/J (tier EXCELLENT) — cert sa-b6d99f8d118543fdb136bf36872a9ad3
- FP16 CEI researcher bare-metal: 5.13e12 FLOPs/J
- Same-GPU FP16/FP32 ratio inside enclave: approximately 9x
- Same-GPU FP16/FP32 ratio bare-metal: 15.6x

The FP32 CEI result (3.178e11 FLOPs/J) is the most reproducible signal in the battery — ±1.6% across five passes and within ~4% of an independent bare-metal reproduction. Cross-laboratory reproduction at this level of agreement is the strongest available evidence that GPU Energy Optimizer measures consistently.

The FP16 gap between the TDX enclave result and the bare-metal result is explained by encrypted-memory overhead in confidential compute: FP16 is memory-bandwidth-bound, and TDX encrypted-memory overhead applies a measurable tax. This is the measurable cost of attestation, not a discrepancy. The correct figure to cite for same-GPU FP16 speedup is the CEI ratio from the same run, not a cross-environment comparison of absolute values.

The hardware-attested certificates AGT-M4 and AGT-M7 confirm measurements taken by Serial Alice's own agent inside the verified TDX enclave, bound to the Intel hardware attestation quote.

### 6.4 Methodological Finding: Measure Ratios, Not Absolutes

Serial Alice's 30-run reproducibility study on H200 is the central methodological finding of this validation:

| Quantity (30 runs) | Mean | Coefficient of Variation |
|---|---|---|
| FP32 absolute CEI | 7.03e10 FLOPs/J | 20.6% — not reproducible single-run |
| FP16 absolute CEI | 5.93e11 FLOPs/J | 19.5% — not reproducible single-run |
| BF16 absolute CEI | 6.08e11 FLOPs/J | 21.4% — not reproducible single-run |
| FP8 absolute CEI | 8.62e11 FLOPs/J | 22.9% — not reproducible single-run |
| FP8/BF16 ratio | 1.410 (+41%) | 2.81% — reproducible |

Under back-to-back load the GPU heats and throttles, swinging absolute CEI by roughly 2x. The ratio between precision levels is rock-stable because the thermal state affects every precision proportionally, canceling the dominant noise term.

The practical consequence: any pass/fail gate built on a single-run absolute CEI against a fixed reference sits on this noise floor and will flip on thermal state alone, independent of actual GPU performance. GPU Energy Optimizer's M20 test exhibited exactly this fragility — it reads FAIL on H200 because the H200 is approximately 54x above the A100 reference constant, documented and expected behavior, not a defect. The correctly-calibrated gate (M20_H200) passes at +1.9% against Serial Alice's attested H200 baseline. The ratio-based gate (M20_v2) runs both precision modes in the same thermal session and checks the ratio, which is stable. This is the correct design for production CEI gates.

### 6.5 Tenant Isolation — SEC-AB, SEC-VRAM, SEC-KILL

Three isolation scenarios were tested. All three passed.

- SEC-AB (A/B writer/reader with positive control): 0 cross-tenant recoveries; positive control 3,125,000 hits — cert sa-f47d9425a06b443ab3bb93d033276da0
- SEC-VRAM (graceful teardown): 0 recoveries; isolation_held = true — cert sa-2346aeedc75a464b974f5fc052ad2b56
- SEC-KILL (SIGKILL termination): 0 recoveries; isolation_held = true — cert sa-83c49247b7b94b5dbe77d2075031d37d

The positive control in SEC-AB is critical to interpreting the result correctly: the scanner confirmed 3,125,000 hits when the marker was intentionally present, proving the harness can detect a leak when one exists. Finding zero in the actual test is therefore meaningful, not a silent null.

These results apply to same-GPU isolation within the single-GPU CVM tested. Cross-GPU isolation requires two or more physical GPUs and is listed as a gap in Section 7.

### 6.6 Cross-GPU Isolation Failure — Confirmed Outside Serial Alice Scope

The cross-GPU residual finding from Section 3.3 was confirmed in independent testing on a 2x H200 pod outside the Serial Alice CVM environment. GPU1, which ran no compute workload, retained 528MB of residual VRAM from GPU0 activity while NVML reported 0% utilization on both GPUs throughout. This is a distinct and broader exposure pathway than same-GPU sequential residual. It has not yet been replicated in a Serial Alice attested run, as cross-GPU testing was outside the scope of the single-GPU CVM used for the June 27 battery. It is listed as the top priority next step in Section 7.

### 6.7 FP8 Precision Ladder — Serial Alice Finding, Attribution Required

Beyond the GPU Energy Optimizer test battery, Serial Alice ran an independent four-precision FLOPs-per-joule ladder on the H200 inside the TDX enclave. This is a Serial Alice finding. The source script was not provided to and is not present in this codebase. The specific numbers below have not been independently reproduced by GPU Energy Optimizer's own measurement code and should be cited with this attribution.

| Precision | TFLOPS | Power | CEI (FLOPs/J) | vs FP32 |
|---|---|---|---|---|
| FP32 | 46.9 | 620.9W | 7.55e10 | 1.00x |
| FP16 | 340.1 | 525.2W | 6.48e11 | 8.57x |
| BF16 | 349.6 | 517.3W | 6.76e11 | 8.95x |
| FP8 (e4m3) | 384.4 | 400.9W | 9.59e11 | 12.69x |

Certificate: sa-e6628d5cff38402da74d5343a0b17c03 — Polygon: 0x6ae0ce

The FP8 efficiency gain is power-driven, not throughput-driven. FP8 throughput (384 TFLOPS) is only approximately 10% above BF16 (350 TFLOPS), far below the device's FP8 tensor-core peak. The gain comes from lower power draw at 400.9W versus 517-621W for other precisions. The FP8/BF16 ratio of +41% is reproducible at CV 2.81% over 30 runs where the absolute values are not, consistent with the methodological finding in Section 6.4.

An in-house FP8 ladder test (M_fp8_ladder.py) has been written and is ready to run on next H200 rental to independently verify or refute these figures using this codebase's own measurement code.

### 6.8 All 15 Certificates

All certificates verify as overall_valid with all seven layers green and confirmed Polygon anchors.

Shared anchor (11 bridge certificates): polygonscan.com/tx/0x28327b
Verify any certificate: api.serialalice.pt/v2/certificates/<id>/verify

1. M2 ghost detection — self_reported — sa-29820cec7f404fcfb9b56ed15e1757ca — 0x28327b
2. M3 DESYNC detection — self_reported — sa-1270c86eacd64db6bf5f26a34fe1381f — 0x28327b
3. M4 CEI FP32 — self_reported — sa-8858266ebbda45ceb240db0fa122a554 — 0x28327b
4. M6 sustained run — self_reported — sa-b2f092b30e3c4196a8afbceffda266ee — 0x28327b
5. M7 CEI FP16 — self_reported — sa-b6d99f8d118543fdb136bf36872a9ad3 — 0x28327b
6. M19 ghost accuracy — self_reported — sa-6d9f9abf7bb64b9d9894b19338cf57d7 — 0x28327b
7. M20 CEI accuracy — self_reported — sa-9c90bff0f6ce4e4898ff5cc32407bfd2 — 0x28327b
8. M20 H200 calibrated — self_reported — sa-51e01f583e4b4505834f98df32448ae6 — 0x28327b
9. SEC-AB isolation — self_reported — sa-f47d9425a06b443ab3bb93d033276da0 — 0x28327b
10. SEC-VRAM isolation — self_reported — sa-2346aeedc75a464b974f5fc052ad2b56 — 0x28327b
11. SEC-KILL isolation — self_reported — sa-83c49247b7b94b5dbe77d2075031d37d — 0x28327b
12. AGT-M4 TEE hardware_attested — sa-482d90ff89cd415e9b32ac68ef5759e5 — 0xcfc3e7
13. AGT-M7 TEE hardware_attested — sa-208f23496b324f22b8f1327028b612bf — 0xf2a08c
14. FP8 ladder — self_reported — sa-e6628d5cff38402da74d5343a0b17c03 — 0x6ae0ce
15. SA self-proof — self_reported — sa-cb4f69809b524f1faaac37d5b51a20f4 — 0xa4f52b

Attestation statement: Serial Alice attests that the measurements recorded in the fifteen certificates were captured on a NVIDIA H200 GPU operating inside an Intel TDX confidential-compute enclave, at the timestamps bound into each record, and have not been altered since issuance, as independently provable by the classical Ed25519 signature, the post-quantum ML-DSA-65 signature, the Merkle batch proof, and the immutable Polygon on-chain anchor. As of this report, 15 of 15 certificates verify as overall_valid with on-chain anchors confirmed. This is a statement of measurement integrity, not a statement of regulatory conformance.

Acknowledgments: Independent validation provided by Serial Alice / Sirius GreenTech. Validation lead: Nelson Vicente, CEO, Sirius GreenTech, Portugal.


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
