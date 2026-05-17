AI GPU Energy Optimizer

GPU energy observability platform with multi-provider anomaly detection — per-user API keys, time-series metrics, anomaly detection across 17 cloud GPU providers, live APIs, and Grafana dashboards.

«Built from an Android phone using Termux. © 2026 Mike Bains — Source available for research and evaluation.»

---

🌐 Live URLs

Service| URL
Live API Docs| https://ai-gpu-brain-v2.onrender.com/docs
Frontend Dashboard| https://ai-gpu-energy-optimizer.vercel.app
A100 Metrics| https://ai-gpu-brain-v2.onrender.com/metrics/a100
H100 Metrics| https://ai-gpu-brain-v2.onrender.com/metrics/h100
A100 Results| https://ai-gpu-brain-v2.onrender.com/results/a100
H100 Results| https://ai-gpu-brain-v2.onrender.com/results/h100
CEI Standard| https://ai-gpu-brain-v2.onrender.com/standards/cei
GPU Compare API| https://ai-gpu-brain-v2.onrender.com/compare/gpu

---

⚡ 60-Second Install

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone repository
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-

# Start platform
cd ai-gpu-energy-optimizer-
docker-compose up

Open:

http://localhost:3000

---

🏗️ Architecture

GPU Agent → FastAPI Backend → SQLite/PostgreSQL → Grafana Dashboard

Supported Providers

AWS • GCP • Azure • RunPod • CoreWeave • Vast.ai • Lambda • Paperspace • Colab • Kaggle • HuggingFace • Salad • Voltage Park • Crusoe • Genesis • FluidStack • Massed Compute

---

🚀 What You Get

- Real-time GPU energy dashboard
- DESYNC and GHOST anomaly detection
- 17 cloud provider support
- Per-user API keys
- Time-series metrics scaling to 50 GPUs
- Grafana dashboard integration
- Prometheus-compatible metrics
- 18/18 smoke tests passing

---

⚡ Scale & Performance

- Up to 50 GPUs monitored simultaneously
- Real-time metrics ingestion per agent
- Indexed time-series queries
- Multi-tenant API isolation
- SQLite default deployment
- PostgreSQL migration path planned for v2

Need 100+ GPUs? PostgreSQL + TimescaleDB support is on the v2 roadmap.

---

🔍 Anomaly Detection

DESYNC

GPU drawing 420W while reporting 8% utilization.

You are paying full price for a GPU doing almost no useful work.

GHOST

GPU reporting 98% utilization at 40W draw.

Physically improbable telemetry indicating scheduler or observability corruption.

Validated Across

AWS, GCP, Azure, RunPod, CoreWeave, Vast.ai, Lambda, Paperspace, Colab, Kaggle, HuggingFace, Salad, Voltage Park, Crusoe, Genesis, FluidStack, and Massed Compute.

---

📊 Validated Findings

- H100 SXM idle baseline observed around 69–76W
- H100 sustained load peaks observed near 591W
- A100 SXM cooldown stabilization observed near 66–78W
- RTX 4090 cooldown returned near 20W idle after sustained load
- Tesla T4 idle baseline observed near 9.6W
- No persistent ghost power detected on validated hardware
- FP16 tensor workloads showed higher sustained power draw than expected during full tensor utilization
- CEI benchmarking validated across A100 SXM and H100 SXM GPUs
- Telemetry synchronization confirmed across repeated sustained-load test runs

---

🔌 Example API Usage

Fetch Metrics

curl -H "X-API-Key: YOUR_API_KEY" \
https://ai-gpu-brain-v2.onrender.com/metrics/a100

Compare GPUs

curl https://ai-gpu-brain-v2.onrender.com/compare/gpu

Fetch CEI Standard

curl https://ai-gpu-brain-v2.onrender.com/standards/cei

---

📡 API Coverage

51+ endpoints covering:

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

🧠 The CEI Standard

Compute Energy Intensity (CEI) is a benchmark defined by this project.

It measures:

Floating-point operations delivered per joule during sustained GPU workloads.

The goal is to normalize GPU efficiency measurements across providers, accelerators, and workload types.

---

🚀 Version 2 Roadmap

Feature| Description
🔔 Slack Alerts| Real-time webhook on DESYNC or GHOST anomalies
💰 Cost Estimation| Convert power anomalies into estimated $ waste
⌨️ CLI Tool| gpuopt status / gpuopt submit
📊 Prometheus Exporter| Integration with existing monitoring stacks
📈 Energy Score Timeline| Historical efficiency scoring
🔄 Self-Update Script| Pull latest anomaly rules

---

🗺️ Full Feature Roadmap

Security & Access

- SSO / OAuth login
- Role-based access control
- API key expiry and rotation

GPU Hardware

- Tenstorrent support
- AMD ROCm support
- Apple Silicon MPS support
- Intel Arc GPU support

Scheduling & Automation

- Auto-migrate workloads on anomaly
- Energy-aware job scheduling
- Off-peak scheduling optimization

Reporting

- Weekly energy reports
- Carbon footprint estimation
- Data center compliance reporting

Integrations

- Weights & Biases
- HuggingFace monitoring
- Kubernetes operator
- Terraform provider

Business Features

- Multi-tenant billing dashboard
- SLA monitoring per provider
- Real-time provider cost comparison
- Team chargeback reporting

Developer Experience

- CLI tooling
- Prometheus exporter
- Self-update utility
- Python and Node.js SDKs

---

👤 Author

Mike Bains

- Built entirely from Android + Termux
- Focused on GPU observability, telemetry validation, and energy benchmarking
- Open to infrastructure, observability, and AI systems partnerships

Email:

mikebains41@gmail.com

---

📜 License

Source available for research and evaluation purposes.

Commercial redistribution, resale, or hosting of this software is prohibited without permission from the author.
