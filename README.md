# AI GPU Energy Optimizer

[![Render](https://img.shields.io/badge/Render-Live-brightgreen)](https://ai-gpu-brain-v2.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)

**Real-time GPU energy optimization for A100, H100, and AI factories.** Monitor power, temperature, and throttling. Predict OC levels before hardware throttling occurs. Deploy in 60 seconds.

Built entirely on a Samsung S25 Ultra – no laptop, no desktop.

---

## 🚀 Live Demo

| Link | URL |
|------|-----|
| **Backend API** | https://ai-gpu-brain-v2.onrender.com |
| **API Docs** | https://ai-gpu-brain-v2.onrender.com/docs |
| **Frontend Dashboard** | https://ai-gpu-energy-optimizer.vercel.app |

## Live A100 Metrics

**View real-time A100 GPU data:**
[https://ai-gpu-brain-v3.onrender.com/metrics](https://ai-gpu-brain-v3.onrender.com/metrics)

## Live H100 Metrics
29  View real-time H100 GPU data: [https://ai-gpu-brain-v3.onrender.com/metrics](https://ai-gpu-brain-v3.onrender.com/metrics)
30  ### What the H100 data shows:
31  | Field | Description |
32  |---|----------|
33  | cluster_id | "h100-runpod" - identifies the H100 GPU cluster |
34  | timestamp | Unix timestamp (proof of continuous collection) |
35  | utilization_percent | GPU utilization % (90-95%) |
36  | memory_used_gb | Used memory in GB (35-45GB) |
37  | memory_total_gb | Total memory (80GB) |
38  | temperature_celsius | GPU temperature (55-65°C) |
39  | power_draw_watts | GPU power draw (350-450W) |

### What the data shows:

| Field | Description |
|-------|-------------|
| `cluster_id` | "a100-80gb-runpod" - identifies the GPU cluster |
| `timestamp` | Unix timestamp (proof of continuous collection) |
| `utilization_percent` | GPU utilization % (80-95%) |
| `memory_used_gb` | Used memory in GB (40-50GB) |
| `memory_total_gb` | Total memory (80GB) |
| `temperature_celsius` | GPU temperature (60-75°C) |
| `power_draw_watts` | GPU power draw (240-270W) |

### Example response:
```json
{
  "a100-80gb-runpod": [
    {
      "cluster_id": "a100-80gb-runpod",
      "timestamp": 1777248579.1373765,
      "gpus": [{
        "gpu_id": 0,
        "utilization_percent": 85.0,
        "memory_used_gb": 45.0,
        "memory_total_gb": 80.0,
        "temperature_celsius": 65.0,
        "power_draw_watts": 250.0
      }]
    }
  ]
}
---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Power monitoring** | Real-time GPU power draw (watts) |
| **Temperature monitoring** | Real-time GPU temperature (°C) |
| **Thermal alerts** | Automatic alerts when temp > 80°C |
| **Throttling prediction** | OC1-OC4 levels with reduction % |
| **Power capping** | Set power limits via API |
| **Kubernetes native** | CRD + KEDA + Prometheus |
| **MIG support** | Monitor individual partitions |
| **Process accounting** | Track GPU usage per PID |
| **60-second install** | One command deployment |

---

## 📊 Supported GPUs

| GPU | Memory | Power Range | MIG |
|-----|--------|-------------|-----|
| A100 40GB | 40 GB | 44W - 250W | ✅ |
| A100 80GB | 80 GB | 44W - 300W | ✅ |
| H100 80GB | 80 GB | 78W - 450W | ✅ |

---

## 🏗️ Architecture

| Layer | Technology |
|-------|------------|
| Frontend | Next.js (Vercel) |
| Backend | FastAPI (Render) |
| Database | PostgreSQL (Render) |
| Metrics | Prometheus |
| Orchestration | Kubernetes CRD + KEDA |

---

## 🔧 Quick Start (60 seconds)

```bash
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer
cd ai-gpu-energy-optimizer
