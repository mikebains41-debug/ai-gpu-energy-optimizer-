# AI GPU Energy Optimizer

**GPU energy observability platform with multi-provider anomaly detection** — per-user API keys, time-series metrics, anomaly detection across 17 cloud GPU providers, and live Grafana dashboards.

> Built from an Android phone using Termux. © 2026 Mike Bains — Source available for research and evaluation.

---

## ⚡ 60-Second Install

    curl -fsSL https://get.docker.com | sh
    git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
    cd ai-gpu-energy-optimizer-
    docker-compose up

Open http://localhost:3000 — done.

---

## 🏗️ Architecture

GPU Agent → FastAPI Backend → SQLite/PostgreSQL → Grafana Dashboard

Supported Providers:
AWS • GCP • Azure • RunPod • CoreWeave • Vast.ai
Lambda • Paperspace • Colab • Kaggle • HuggingFace
Salad • Voltage Park • Crusoe • Genesis • FluidStack • Massed Compute

---

## What You Get

- Real-time GPU energy dashboard
- DESYNC and GHOST power anomaly detection
- 17 cloud provider support
- Per-user API keys
- Time-series metrics scaling to 50 GPUs
- 18/18 smoke tests passing

---

## ⚡ Scale & Performance

- **Up to 50 GPUs** across multiple providers simultaneously
- Real-time metrics ingestion per agent
- Indexed time-series queries
- Multi-tenant isolation per API key

Need 100+ GPUs? PostgreSQL + TimescaleDB upgrade is planned for v2.

---

## 🔍 Anomaly Detection

**DESYNC** — GPU drawing 420W while reporting 8% utilization. You are paying full price for a GPU doing almost no useful work.

**GHOST** — GPU reporting 98% utilization at 40W draw. Physically improbable telemetry indicating scheduler or observability corruption.

Validated across: AWS, GCP, Azure, RunPod, CoreWeave, Vast.ai, Lambda, Paperspace, Colab, Kaggle, HuggingFace, Salad, Voltage Park, Crusoe, Genesis, FluidStack, and Massed Compute.

---

## 📊 Validated Findings

- H100 SXM idle baseline observed around 69-76W
- H100 sustained load peaks observed near 591W
- A100 SXM cooldown stabilization observed near 66-78W
- RTX 4090 cooldown returned near 20W idle after sustained load
- Tesla T4 idle baseline observed near 9.6W
- No persistent ghost power detected on validated hardware
- FP16 tensor workloads showed higher sustained power draw than expected

---

## 🔌 Example API Usage

    curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8000/metrics

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

## 📜 License

Source available for research and evaluation purposes.
Commercial redistribution, resale, or hosting of this software is prohibited without permission from the author.
