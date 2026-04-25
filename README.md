# AI GPU Energy Optimizer

[![Render](https://img.shields.io/badge/Render-Deployed-brightgreen)](https://ai-gpu-brain-v2.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)

Real-time GPU energy optimization for A100, H100, and AI factories. Monitor power, temperature, and throttling. Predict OC levels before hardware throttling occurs. Deploy in 60 seconds.

## 🚀 Live Demo

- **Backend API:** https://ai-gpu-brain-v2.onrender.com
- **API Documentation:** https://ai-gpu-brain-v2.onrender.com/docs
- **Frontend Dashboard:** https://ai-gpu-energy-optimizer.vercel.app

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Real-time GPU monitoring** | Power draw (W), temperature (°C), utilization (%), memory usage (GB) |
| **Thermal alerts** | Automatic alerts when GPU temperature exceeds 80°C |
| **Throttling prediction** | OC1-OC4 levels with reduction percentages |
| **Power capping recommendations** | Suggests optimal power caps (250W inference / 400W training) |
| **Kubernetes-native power capping** | CRD + KEDA + Prometheus metrics |
| **MIG support** | Monitor individual MIG partitions on A100/H100 |
| **Process-level accounting** | Track GPU usage per process (PID) |
| **Mission Control integration** | Factory robot power optimization |
| **60-second install** | One command deployment |

## 📊 Supported GPUs

| GPU | Memory | Power Range | MIG Support |
|-----|--------|-------------|-------------|
| NVIDIA A100 40GB | 40 GB | 44W - 250W | ✅ Yes |
| NVIDIA A100 80GB | 80 GB | 44W - 300W | ✅ Yes |
| NVIDIA H100 80GB | 80 GB | 78W - 450W | ✅ Yes |

## 🏗️ Architecture
| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js (Vercel) – Dashboard, WebSocket, Charts |
| **Backend** | FastAPI (Render) – API, PostgreSQL, Prometheus |
| **Monitoring** | Power, temperature, utilization, memory |
| **Throttling** | OC1-OC4 prediction with reduction % |
| **Kubernetes** | CRD for power capping, KEDA autoscaling |
| **MIG Support** | Per-partition monitoring,

## 🔧 Installation

### 60-Second Quick Start

```bash
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer
cd ai-gpu-energy-optimizer

### Deploy to Render

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Select **Python 3** runtime
4. Set **Root Directory** to `ai-engine`
5. Add `DATABASE_URL` environment variable
6. Click **Create Web Service**

## 📡 API Endpoints
## 🧪 Testing

### Send test metrics from A100

```bash
nvidia-smi --query-gpu=index,power.draw,power.limit,temperature.gpu,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits | while IFS=', ' read idx power power_limit temp mem_used mem_total util; do
    curl -X POST https://ai-gpu-brain-v2.onrender.com/api/v1/metrics \
        -H "Authorization: Bearer test_key_123" \
        -H "Content-Type: application/json" \
        -d "{\"cluster_id\":\"a100-lambda\",\"timestamp\":$(date +%s),\"gpus\":[{\"gpu_id\":$idx,\"utilization_percent\":$util,\"memory_used_gb\":$mem_used,\"memory_total_gb\":$mem_total,\"temperature_celsius\":$temp,\"power_draw_watts\":$power}]}"
done

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/metrics` | View stored GPU metrics |
| POST | `/api/v1/metrics` | Send GPU metrics |
| GET | `/thermal-alerts` | Get overheating alerts |
| GET | `/power-headroom` | Predict throttling (OC1-OC4) |
| GET | `/k8s/power-metrics` | Prometheus metrics for KEDA |
