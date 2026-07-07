## 🔒 Security Findings

**CVE-2048350 CVSS 8.4** — VRAM residual data leakage confirmed across A100, H100, H200, and B200 SXM. Filed with MITRE 2026-05-31.

👉 [View Interactive Security Findings Charts](https://ai-gpu-energy-optimizer.vercel.app/security-findings)

📄 [Read Full Whitepaper](https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-/blob/main/WHITEPAPER.md)

---

# AI GPU Energy Optimizer



![License](https://img.shields.io/badge/License-Apache%202.0-brightgreen)




![Commercial Use](https://img.shields.io/badge/Commercial%20Use-Permitted-brightgreen)




![Tests](https://img.shields.io/badge/Tests-42%2F42%20Passing-brightgreen)




![Providers](https://img.shields.io/badge/Cloud%20Providers-17-purple)



**GPU energy observability platform with multi-provider anomaly detection** — per-user API keys, time-series metrics, anomaly detection across 17 cloud GPU providers, live APIs, and Grafana dashboards.

> «Built from an Android phone using Termux. © 2026 Manmohan (Mike) Bains — Licensed under Apache 2.0 — free to use, modify, and distribute.»

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
| A100 Results (24 tests, example: /results/a100/test-01_idle_baseline) | https://ai-gpu-brain-v3.onrender.com/results/a100 |
| H100 Results (11 tests, example: /results/h100/test-01_idle_baseline) | https://ai-gpu-brain-v3.onrender.com/results/h100 |
| CEI Standard | https://ai-gpu-brain-v3.onrender.com/standards/cei |
| GPU Compare API | https://ai-gpu-brain-v3.onrender.com/compare/gpu |
| CEI Telemetry | https://gpu-core-private.onrender.com/telemetry/stats |

---

## ⚡ 60-Second Install

\`\`\`bash
curl -fsSL https://get.docker.com | sh
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
cd ai-gpu-energy-optimizer-
docker-compose up
\`\`\`

Open: http://localhost:3000

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

**GHOST** — GPU drawing 65-574W while NVML reports 0% utilization. Confirmed across A100, H200, B200 SXM. Invisible to DCGM, Prometheus, Datadog, and all NVML-based tools.

**DESYNC** — Power rail and NVML utilization counter are out of phase. GPU draws sustained high power while reported utilization lags or reads zero.

**Validated Across:** AWS, GCP, Azure, RunPod, CoreWeave, Vast.ai, Lambda, Paperspace, Colab, Kaggle, HuggingFace, Salad, Voltage Park, Crusoe, Genesis, FluidStack, and Massed Compute.

---

## 📊 Validated Findings

**CVE-2048350 CVSS 8.4 — VRAM Residual Data Leakage**
- A100 SXM: 457-465MB residual after graceful PyTorch exit — SIGKILL clears to 0MB
- H100 SXM: 457MB residual after graceful PyTorch exit
- H200 SXM: 529-629MB residual single workload, 1630MB full profile
- B200 SXM: 628-728MB fixed residual regardless of compute precision
- Cross-GPU isolation failure on H200 — GPU1 retained 528MB from GPU0 despite GPU1 idle
- NVML reports 0% throughout — invisible to DCGM, Prometheus, Datadog
- False clear signal — process exits code 0 while 1630MB remains exposed

**Ghost Power**
- A100 SXM: 146.66W at 0% utilization — architectural confirmed
- B200 SXM: 144W cold boot, 549-574W ghost spike after process exit at 0% NVML
- H200 SXM: 147.96W post-load ghost power confirmed — Serial Alice cert sa-b2f092 2026-06-27
- H100 SXM: Clean — Hopper HBM2e confirmed no ghost power
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

**Third-Party Attested — June 27, 2026**

Independently validated on NVIDIA H200 inside Intel TDX confidential compute enclave
in collaboration with a European energy attestation partner.
Ed25519 + ML-DSA-65 post-quantum signatures. Merkle batch. Polygon mainnet anchors.
All certificates publicly verifiable on-chain with no account required.

- 24h+ cumulative testing. 11,052 samples. 0 crashes.
- FP32 CEI 3.178e11 FLOPs/J confirmed ±1.6% across 5 independent passes
- Ghost power 147.96W at 0% utilization confirmed — cert sa-b2f092
- Idle floor 80.36W confirmed — cert sa-29820c
- Tenant isolation held in 3 independent scenarios with working positive control
- Cross-GPU isolation failure 528MB confirmed on 2x H200
- 15 blockchain-anchored certificates — all overall_valid across 7 verification layers

This validation would not have been possible without the collaboration of our European partner.
Full certificate details and Polygon anchors are in the whitepaper.

---

## 🔌 Example API Usage

\`\`\`bash
curl -H "X-API-Key: YOUR_API_KEY" https://ai-gpu-brain-v3.onrender.com/metrics/a100
curl https://ai-gpu-brain-v3.onrender.com/compare/gpu
curl https://ai-gpu-brain-v3.onrender.com/standards/cei
\`\`\`

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

## 🧠 The CEI Standard

Compute Energy Intensity (CEI) is a benchmark defined by this project.

It measures: Floating-point operations delivered per joule during sustained GPU workloads.

The goal is to normalize GPU efficiency measurements across providers, accelerators, and workload types.

---

## 🚀 Version 2 Roadmap

| Feature | Description |
|---------|-------------|
| 🔔 Slack Alerts | Real-time webhook on DESYNC or GHOST anomalies |
| 💰 Cost Estimation | Convert power anomalies into estimated $ waste |
| ⌨️ CLI Tool | gpuopt status / gpuopt submit |
| 📊 Prometheus Exporter | Shipped — integration with existing monitoring stacks |
| 📈 Energy Score Timeline | Historical efficiency scoring |
| 🔄 Self-Update Script | Pull latest anomaly rules |

---

## 🗺️ Full Feature Roadmap

### Security & Access
- SSO / OAuth login
- Role-based access control
- API key expiry and rotation

### GPU Hardware
- Tenstorrent support
- AMD ROCm support
- Apple Silicon MPS support
- Intel Arc GPU support

### Scheduling & Automation
- Auto-migrate workloads on anomaly
- Energy-aware job scheduling
- Off-peak scheduling optimization

### Reporting
- Weekly energy reports
- Carbon footprint estimation
- Data center compliance reporting

### Integrations
- Weights & Biases
- HuggingFace monitoring
- Kubernetes operator
- Terraform provider

### Business Features
- Multi-tenant billing dashboard
- SLA monitoring per provider
- Real-time provider cost comparison
- Team chargeback reporting

### Developer Experience
- CLI tooling
- Prometheus exporter
- Self-update utility
- Python and Node.js SDKs

---

## 👤 Author

**Manmohan (Mike) Bains**

- Built entirely from Android + Termux — Samsung S25 Ultra
- Independent GPU security and energy researcher, Duncan BC Canada
- Focused on GPU observability, telemetry validation, energy benchmarking, and security
- Open to infrastructure, observability, AI systems partnerships, and licensing

Email: mikebains41@gmail.com

---

## 📊 Benchmark Contribution (Optional)

The GPU Energy Optimizer includes an opt-in telemetry sharing feature to build the CEI benchmark dataset. By enabling contribution, you help map systematic telemetry divergence across cloud providers and improve DESYNC/GHOST detection accuracy. All data is anonymized, aggregated, and used strictly for research and standardization. You retain full ownership of your raw metrics and may disable sharing at any time.

**Enable via Docker Compose:** CEI_TELEMETRY=true

**What we collect:** GPU model, cloud provider, power draw, utilization, workload type, anonymized anomaly flags.

**What we NEVER collect:** Instance IDs, account names, job payloads, IP addresses, or API keys.

**Data Rights:** By contributing telemetry data, you grant Manmohan (Mike) Bains a non-exclusive, royalty-free license to use anonymized, aggregated data for CEI benchmark development, anomaly detection improvement, provider reliability reporting, and academic research. You retain full ownership of your raw telemetry. Individual contributor data is never identified without explicit consent.

For data requests or enterprise DPA: mikebains41@gmail.com

---

## 🛡️ Intellectual Property

The following are protected intellectual property of Manmohan (Mike) Bains:

- **DESYNC Detection Algorithm**: Method for identifying GPU power/utilization desynchronization
- **GHOST Detection Algorithm**: Method for identifying physically impossible telemetry states
- **CEI (Compute Energy Intensity)**: Benchmark standard and calculation methodology
- **Multi-Provider Telemetry Validation Framework**: Cross-cloud anomaly detection system

**Trademarks:** DESYNC™, GHOST™, and CEI™ are trademarks of Manmohan (Mike) Bains.

**Research Use:** Academic and non-commercial research use is permitted with proper citation. Commercial deployment requires explicit licensing.

**Citation:**
\`\`\`
Bains, M. (2026). GPU Energy Optimizer: Telemetry Validation and Anomaly Detection.
GitHub Repository. https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
\`\`\`

---



---

## 🧪 Test Coverage

### Hardware Test Results
- 24 A100 SXM tests — publicly queryable
- 11 H100 SXM tests — publicly queryable
- Query any result: `curl https://ai-gpu-brain-v3.onrender.com/results/a100/1`

### Platform Validation — 40/40 Tests Passing

- All public API endpoints (health, metrics, engine, standards, compare, results)
- DESYNC and GHOST anomaly detection validated against A100 and H100 power envelopes
- 17 cloud provider telemetry validation
- Database operations (insert, query, aggregation)
- API key authentication and authorization
- Kubernetes and Run:ai integration hooks
- CEI benchmark calculation and persistence

**Full test suite: 42/42 Morpheus passing. Plus 15 Serial Alice blockchain-anchored certificates on H200 inside Intel TDX.**


## 📊 Security Findings Charts

Interactive charts for all key findings:
[View Charts](charts/gpu_security_charts.jsx)

## Contact
Mike Bains — mike@gpu-optimizer.com
