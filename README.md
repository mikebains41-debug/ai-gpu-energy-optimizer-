# AI GPU Energy Optimizer



![License](https://img.shields.io/badge/License-Source--Available-blue)




![Commercial Use](https://img.shields.io/badge/Commercial%20Use-License%20Required-red)




![Tests](https://img.shields.io/badge/Tests-18%2F18%20Passing-brightgreen)




![Providers](https://img.shields.io/badge/Cloud%20Providers-17-purple)



**GPU energy observability platform with multi-provider anomaly detection** — per-user API keys, time-series metrics, anomaly detection across 17 cloud GPU providers, live APIs, and Grafana dashboards.

> «Built from an Android phone using Termux. © 2026 Mike Bains — Source available for research and evaluation.»

---

## 💼 Commercial Use & Licensing

**This is NOT open-source software.** This is source-available software with restricted commercial use.

**Need commercial deployment?** Contact mikebains41@gmail.com for:
- Production deployment licenses
- Enterprise support agreements
- OEM integration rights
- Managed service provider licenses
- Cloud provider partnerships

**Pricing starts at $25K/year** for commercial deployments. Custom pricing available for volume deployments and strategic partnerships.

**Current commercial license holders:** [None yet — be the first!]

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

**DESYNC** — GPU drawing 420W while reporting 8% utilization. You are paying full price for a GPU doing almost no useful work.

**GHOST** — GPU reporting 98% utilization at 40W draw. Physically improbable telemetry indicating scheduler or observability corruption.

**Validated Across:** AWS, GCP, Azure, RunPod, CoreWeave, Vast.ai, Lambda, Paperspace, Colab, Kaggle, HuggingFace, Salad, Voltage Park, Crusoe, Genesis, FluidStack, and Massed Compute.

---

## 📊 Validated Findings

- H100 SXM idle baseline observed around 69–76W
- H100 sustained load peaks observed near 412W (burst kernel up to 591W recorded separately)
- A100 SXM cooldown stabilization observed near 66–78W
- RTX 4090 cooldown returned near 20W idle after sustained load
- Tesla T4 idle baseline observed near 9.6W
- Ghost power observed up to ~146W at 0% utilization on A100 SXM hardware
- FP16 tensor workloads showed higher sustained power draw than expected during full tensor utilization
- CEI benchmarking validated across A100 SXM and H100 SXM GPUs
- Telemetry synchronization confirmed across repeated sustained-load test runs

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
| 📊 Prometheus Exporter | Integration with existing monitoring stacks |
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

**Mike Bains**

- Built entirely from Android + Termux
- Focused on GPU observability, telemetry validation, and energy benchmarking
- Open to infrastructure, observability, and AI systems partnerships

Email: mikebains41@gmail.com

---

## 📊 Benchmark Contribution (Optional)

The GPU Energy Optimizer includes an opt-in telemetry sharing feature to build the CEI benchmark dataset. By enabling contribution, you help map systematic telemetry divergence across cloud providers and improve DESYNC/GHOST detection accuracy. All data is anonymized, aggregated, and used strictly for research and standardization. You retain full ownership of your raw metrics and may disable sharing at any time.

**Enable via Docker Compose:** CEI_TELEMETRY=true

**What we collect:** GPU model, cloud provider, power draw, utilization, workload type, anonymized anomaly flags.

**What we NEVER collect:** Instance IDs, account names, job payloads, IP addresses, or API keys.

**Data Rights:** By contributing telemetry data, you grant Mike Bains a non-exclusive, royalty-free license to use anonymized, aggregated data for CEI benchmark development, anomaly detection improvement, provider reliability reporting, and academic research. You retain full ownership of your raw telemetry. Individual contributor data is never identified without explicit consent.

For data requests or enterprise DPA: mikebains41@gmail.com

---

## 🛡️ Intellectual Property

The following are protected intellectual property of Mike Bains:

- **DESYNC Detection Algorithm**: Method for identifying GPU power/utilization desynchronization
- **GHOST Detection Algorithm**: Method for identifying physically impossible telemetry states
- **CEI (Compute Energy Intensity)**: Benchmark standard and calculation methodology
- **Multi-Provider Telemetry Validation Framework**: Cross-cloud anomaly detection system

**Trademarks:** DESYNC™, GHOST™, and CEI™ are trademarks of Mike Bains.

**Research Use:** Academic and non-commercial research use is permitted with proper citation. Commercial deployment requires explicit licensing.

**Citation:**
\`\`\`
Bains, M. (2026). GPU Energy Optimizer: Telemetry Validation and Anomaly Detection.
GitHub Repository. https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
\`\`\`

---

## 📜 License & Use Terms

**Source Available for Research & Evaluation**

This software is provided for research, evaluation, and non-commercial use only.

✅ **You may:**
- Use for personal research and testing
- Deploy for internal evaluation (up to 50 GPUs)
- Contribute bug fixes and improvements
- Share anonymized telemetry for CEI benchmark

❌ **You may NOT:**
- Use for commercial purposes without explicit written permission
- Resell, relicense, or host as a managed service
- Deploy in production environments without a commercial license
- Clone or replicate the DESYNC/GHOST detection methodology in competing products

**Intellectual Property Notice:** The DESYNC/GHOST anomaly detection method, CEI benchmark standard, and related algorithms are proprietary intellectual property of Mike Bains. Commercial use requires a separate license agreement.

For commercial licensing: mikebains41@gmail.com

© 2026 Mike Bains. All rights reserved.

*This notice is for informational purposes and does not constitute legal advice.*

---

## 🧪 Test Coverage

### Hardware Test Results
- 25 A100 SXM tests — publicly queryable
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

**Full test suite: 40/40 passing.**
