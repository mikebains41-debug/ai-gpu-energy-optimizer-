# AI GPU Energy Optimizer

[![Render](https://img.shields.io/badge/Render-Live-brightgreen)](https://ai-gpu-brain-v3.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)

**Real-time GPU energy optimization for A100 and H100 clusters.** Monitor power, temperature, and utilization. Detect and anticipate thermal or power-related throttling before it occurs.

Built entirely on a Samsung S25 Ultra – no laptop, no desktop.

---

## 🚀 Live Demo

| Component | Link |
|-----------|------|
| Backend API | https://ai-gpu-brain-v3.onrender.com |
| API Docs | https://ai-gpu-brain-v3.onrender.com/docs |
| Frontend Dashboard | https://ai-gpu-energy-optimizer.vercel.app |

---

## 💡 Overview

GPU Optimizer is a lightweight software layer designed to improve energy efficiency across existing GPU infrastructure.

It integrates with current environments and does not require hardware upgrades or changes to training or inference workflows.

---

## ⚙️ Core Capabilities

- Real-time monitoring of GPU utilization, power draw, and temperature
- Detection of inefficiencies across workloads
- Early identification of conditions that lead to GPU throttling
- Dynamic adjustment of GPU behavior based on demand

---

## ✅ Proof of Product

- 8+ hours of continuous GPU monitoring
- 2,880+ timestamped data points per GPU
- 90+ GPU metrics collected every 10 seconds
- Live API endpoints accessible to anyone

---

## 🛠️ Technology Stack

- **Backend:** FastAPI (Python) on Render
- **Frontend:** Next.js on Vercel
- **GPU Compute:** RunPod (H100 SXM, A100 SXM)
- **Persistent Storage:** RunPod Network Volume (10 GB)
- **Monitoring:** nvidia-smi + custom Python agents

---

## 🔍 Key Findings (H100 vs A100)

| Metric | H100 | A100 |
| :--- | :--- | :--- |
| Power Draw (peak) | 690W | 410W |
| Temperature | 60°C | 67°C |
| FP8 Support | ✅ Yes | ❌ No |
| Efficiency | Higher performance | Better power efficiency |

**Recommendation:** Run light workloads on A100. Reserve H100 for large language models (70B+ parameters).
