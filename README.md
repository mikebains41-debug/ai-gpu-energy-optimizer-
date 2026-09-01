## 🔒 Security Findings

**VRAM Residual Data Leakage — reported to MITRE 2026-05-31, no CVE assigned yet (self-assessed CVSS 8.4, not independently reviewed). Patent application in preparation. Published by GPU Optimizer Inc. (incorporated in British Columbia, Canada)** — VRAM residual data leakage observed across A100, H200, and B200 SXM. H100 SXM shows residual as well but is clean on cold-boot ghost power (see Validated Findings). Filed with MITRE 2026-05-31.

👉 [View Interactive Security Findings Charts](https://ai-gpu-energy-optimizer.vercel.app/security-findings)

📄 [Read Full Whitepaper](https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-/blob/main/WHITEPAPER.md)

---

# AI GPU Energy Optimizer



![License](https://img.shields.io/badge/License-Source--Available-blue)




![Commercial Use](https://img.shields.io/badge/Commercial%20Use-License%20Required-red)




![Tests](https://img.shields.io/badge/Tests-42%2F42%20Passing-brightgreen)




![Providers](https://img.shields.io/badge/Cloud%20Providers-17-purple)



**GPU energy observability platform with multi-provider anomaly detection** — per-user API keys, time-series metrics, anomaly detection across 17 cloud GPU providers, live APIs, and Grafana dashboards.

> «Built from an Android phone using Termux. © 2026 Manmohan (Mike) Bains — Source available for research and evaluation.»

---

## 💼 Commercial Use and Licensing

This is NOT open-source software. This is source-available software with restricted commercial use.

### You may
- Use for personal research and testing
- Deploy for internal evaluation up to 50 GPUs
- Contribute bug fixes and improvements
- Share anonymized telemetry for CEI benchmark

### You may NOT
- Use for commercial purposes without a license
- Resell, relicense, or host as a managed service
- Deploy in production without a commercial license
- Replicate the DESYNC/GHOST anomaly detection methodology in competing products

### Commercial Licensing

GPU Optimizer is available for commercial deployment under a per-deployment license.
Pricing is based on GPU count and deployment scale.

Contact mikebains41@gmail.com with:
- Number of GPUs in deployment
- Deployment environment (cloud, bare metal, hybrid)
- Use case (energy optimization, compliance reporting, security)

### Intellectual Property

The DESYNC/GHOST anomaly detection method, CEI benchmark standard,
ratio-based CEI gating, and VRAM residual detection method are proprietary
intellectual property of GPU Optimizer Inc. Patent pending.

Copyright 2026 Manmohan (Mike) Bains. All rights reserved.

---

## 🌐 Live URLs

| Service | URL |
|---------|-----|
| Live API Docs | https://ai-gpu-brain-v3.onrender.com/docs |
| Frontend Dashboard | https://ai-gpu-energy-optimizer.vercel.app |
| A100 Metrics | https://ai-gpu-brain-v3.onrender.com/metrics/a100 |
| H100 Metrics | https://ai-gpu-brain-v3.onrender.com/metrics/h100 |
| A100 Results (24 tests) | https://ai-gpu-brain-v3.onrender.com/results/a100 |
| H100 Results (11 tests) | https://ai-gpu-brain-v3.onrender.com/results/h100 |
| CEI Standard | https://ai-gpu-brain-v3.onrender.com/standards/cei |
| GPU Compare API | https://ai-gpu-brain-v3.onrender.com/compare/gpu |
| CEI Telemetry | https://gpu-core-private.onrender.com/telemetry/stats |

---

## ⚡ 60-Second Install

```bash
curl -fsSL https://get.docker.com | sh
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
cd ai-gpu-energy-optimizer-
docker-compose up
```

Open: http://localhost:3000

---

## 🔌 Example API Usage

```bash
curl -H "X-API-Key: YOUR_API_KEY" https://ai-gpu-brain-v3.onrender.com/metrics/a100
curl https://ai-gpu-brain-v3.onrender.com/compare/gpu
curl https://ai-gpu-brain-v3.onrender.com/standards/cei
```

---

## 📡 API Coverage

30+ endpoints covering:

- Real-time ghost power detection
- Compute Energy Intensity (CEI) benchmarking
- A100 vs H100 comparative analysis
- FP32 vs FP16 vs FP8 efficiency comparison
- Matrix scaling analysis (2048 → 8192)
- Prometheus metrics export
- Grafana dashboard integration
- SSE replay of recorded test runs
- Job tracking and duration measurement

---

## 🏗️ Architecture

GPU Agent → FastAPI Backend → SQLite/PostgreSQL → Grafana Dashboard

**Supported Providers**

AWS • GCP • Azure • RunPod • CoreWeave • Vast.ai • Lambda • Paperspace • Colab • Kaggle • HuggingFace • Salad • Voltage Park • Crusoe • Genesis • FluidStack • Massed Compute

---

## 🚀 What You Get

- Real-time GPU energy dashboard
- DESYNC and GHOST anomaly detection
- 17 cloud provider support
- Per-user API keys
- Time-series metrics scaling to 500 GPUs
- Grafana dashboard integration
- Prometheus-compatible metrics
- 18/18 smoke tests passing

---

## ⚡ Scale & Performance

- Up to 500 GPUs monitored simultaneously
- Real-time metrics ingestion per agent
- Indexed time-series queries
- Multi-tenant API isolation
- SQLite default deployment
- PostgreSQL migration path planned for v2

---

## 🔍 Anomaly Detection

**GHOST** — GPU drawing power while NVML reports 0% utilization. Sustained ghost power confirmed on A100, H200, and B200 SXM; short post-exit transient spikes (up to ~574W on B200) decay within about a second to the sustained level. Invisible to DCGM, Prometheus, Datadog, and all NVML-based tools.

**DESYNC** — Power rail and NVML utilization counter are out of phase. GPU draws sustained high power while reported utilization lags or reads zero.

**Validated Across:** AWS, GCP, Azure, RunPod, CoreWeave, Vast.ai, Lambda, Paperspace, Colab, Kaggle, HuggingFace, Salad, Voltage Park, Crusoe, Genesis, FluidStack, and Massed Compute.

## 📊 Validated Findings

**VRAM Residual Data Leakage — self-assessed CVSS 8.4, reported to MITRE 2026-05-31, no CVE assigned yet**
- A100 SXM: 457-465MB residual after graceful PyTorch exit — SIGKILL clears to 0MB
- H100 SXM: ~529MB residual after graceful PyTorch exit (H100 is clean on cold-boot ghost power; VRAM residual is a separate, present effect)
- H200 SXM: 529-629MB residual single workload, 1630MB full profile
- B200 SXM: 628-728MB fixed residual regardless of compute precision
- Cross-GPU isolation failure on H200 — GPU1 retained 528MB from GPU0 despite GPU1 idle
- NVML reports 0% throughout — invisible to DCGM, Prometheus, Datadog
- False clear signal — process exits code 0 while 1630MB remains exposed

**Ghost Power**
- A100 SXM: 146.66W at 0% utilization — architectural, confirmed
- B200 SXM: 144W cold boot; short post-exit transient up to 549-574W at 0% NVML, decaying within ~1s to sustained ghost power
- H200 SXM: 147.96W post-load ghost power confirmed — Serial Alice cert sa-b2f092 2026-06-27
- H100 SXM: Clean on cold boot — Hopper HBM2e shows no cold-boot ghost power (ghost power requires a prior workload to trigger)
- HBM memory clock locked 24/7 — A100 1593MHz, B200 3996MHz — root cause confirmed

**Performance Findings**
- H100 SXM idle baseline 69-76W
- H100 sustained load peaks near 412W, burst kernel up to 591W
- A100 SXM cooldown stabilization near 66-78W
- RTX 4090 cooldown returned near 20W idle after sustained load
- Tesla T4 idle baseline near 9.6W
- FP16 tensor workloads showed higher sustained power draw than FP32
- CEI benchmarking validated across A100 SXM and H100 SXM GPUs

---

## 🏅 Independent Validation

**Third-Party Attested — June 27, 2026 (prior to any commercial agreement)**

Independently validated on NVIDIA H200 inside Intel TDX confidential compute enclave in collaboration with a European energy attestation partner. This validation was performed on June 27, 2026, before any commercial agreement between the parties. Ed25519 + ML-DSA-65 post-quantum signatures. Merkle batch. Polygon mainnet anchors. All certificates publicly verifiable on-chain with no account required.

- 24h+ cumulative testing. 11,052 samples. 0 crashes.
- FP32 CEI 3.178e11 FLOPs/J confirmed ±1.6% across 5 independent passes
- Ghost power 147.96W at 0% utilization confirmed — cert sa-b2f092
- Idle floor 80.36W confirmed — cert sa-29820c
- Tenant isolation held in 3 independent scenarios with working positive control
- Cross-GPU isolation failure 528MB confirmed on 2x H200
- 15 blockchain-anchored certificates — all overall_valid across 7 verification layers

This validation would not have been possible without the collaboration of our European partner. Full certificate details and Polygon anchors are in the whitepaper.

---

## 🧠 The CEI Standard

Compute Energy Intensity (CEI) is a benchmark defined by this project. It measures floating-point operations delivered per joule during sustained GPU workloads. The goal is to normalize GPU efficiency measurements across providers, accelerators, and workload types.

---

## 🚀 Version 2 Roadmap

| Feature | Description |
|---------|-------------|
| 🔔 Slack Alerts | Real-time webhook on DESYNC or GHOST anomalies |
| 💰 Cost Estimation | Convert power anomalies into estimated $ waste |
| ⌨️ CLI Tool | gpuopt status / gpuopt submit |
| 📊 Prometheus Exporter | Shipped |
| 📈 Energy Score Timeline | Historical efficiency scoring |
| 🔄 Self-Update Script | Pull latest anomaly rules |

---

## 🛡️ Intellectual Property

The following are protected intellectual property of Manmohan (Mike) Bains:

- **DESYNC Detection Algorithm**: Method for identifying GPU power/utilization desynchronization
- **GHOST Detection Algorithm**: Method for identifying physically impossible telemetry states
- **CEI (Compute Energy Intensity)**: Benchmark standard and calculation methodology
- **Multi-Provider Telemetry Validation Framework**: Cross-cloud anomaly detection system

**Trademarks:** DESYNC™, GHOST™, and CEI™ are trademarks of Manmohan (Mike) Bains.

**Citation:**
```
Bains, M. (2026). GPU Energy Optimizer: Telemetry Validation and Anomaly Detection. GitHub Repository. https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
```

---

## 🧪 Test Coverage

### Hardware Test Results
- 24 A100 SXM tests — publicly queryable
- 11 H100 SXM tests — publicly queryable

### Platform Validation — 40/40 Tests Passing

- All public API endpoints
- DESYNC and GHOST anomaly detection validated against A100 and H100 power envelopes
- 17 cloud provider telemetry validation
- Database operations
- API key authentication and authorization
- Kubernetes and Run:ai integration hooks
- CEI benchmark calculation and persistence

**Full test suite: 42/42 Morpheus passing. Plus 15 Serial Alice blockchain-anchored certificates on H200 inside Intel TDX.**

## Contact
Mike Bains — mike@gpu-optimizer.com
