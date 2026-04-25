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
| **Backend API** | [https://ai-gpu-brain-v2.onrender.com](https://ai-gpu-brain-v2.onrender.com) |
| **API Docs** | [https://ai-gpu-brain-v2.onrender.com/docs](https://ai-gpu-brain-v2.onrender.com/docs) |
| **Frontend Dashboard** | [https://ai-gpu-energy-optimizer.vercel.app](https://ai-gpu-energy-optimizer.vercel.app) |

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
