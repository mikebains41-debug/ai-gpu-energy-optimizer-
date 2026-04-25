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
| **MIG Support** | Per-partition monitoring, Profile detection |

## 🔧 Installation

### 60-Second Quick Start

```bash
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer
cd ai-gpu-energy-optimizer
