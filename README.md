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
- Compatibility with orchestration systems such as Kubernetes and Slurm

---

## 📊 What It Improves

GPU environments often lose efficiency due to uneven workloads and idle capacity.

GPU Optimizer helps by:

- Reducing unnecessary power usage
- Improving overall GPU utilization
- Lowering thermal output and cooling demand

Results vary by environment, but improvements are typically observable in both efficiency and system stability.

---

## ⚡ Deployment

- No hardware changes required
- No retraining or model adjustments
- Minimal setup time (≈60 seconds)
- Designed to integrate with existing systems

---

## 🎯 Use Cases

- AI training clusters
- Inference infrastructure
- GPU-intensive compute environments
- Data centers optimizing cost and efficiency

---

## 🔭 Product Direction

GPU Optimizer can evolve into a broader system for managing compute efficiency:

- GPU efficiency scoring and analytics
- Energy-aware workload scheduling
- Cross-cluster optimization
- Integration with power cost and availability signals

---

## 📊 Live A100 Metrics

**View real-time A100 GPU data:**  
[https://ai-gpu-brain-v3.onrender.com/metrics/a100](https://ai-gpu-brain-v3.onrender.com/metrics/a100)

### What the A100 data shows:

| Field | Description |
|-------|-------------|
| `cluster_id` | "a100-80gb-runpod" - identifies the A100 GPU cluster |
| `timestamp` | Unix timestamp (proof of continuous collection) |
| `utilization_percent` | GPU utilization % (80-95%) |
| `memory_used_gb` | Used memory in GB (40-50GB) |
| `memory_total_gb` | Total memory (80GB) |
| `temperature_celsius` | GPU temperature (60-75°C) |
| `power_draw_watts` | GPU power draw (240-270W) |

---

## 📊 Live H100 Metrics

**View real-time H100 GPU data:**  
[https://ai-gpu-brain-v3.onrender.com/metrics/h100](https://ai-gpu-brain-v3.onrender.com/metrics/h100)

### What the H100 data shows:

| Field | Description |
|-------|-------------|
| `cluster_id` | "h100-runpod" - identifies the H100 GPU cluster |
| `timestamp` | Unix timestamp (proof of continuous collection) |
| `utilization_percent` | GPU utilization % (90-95%) |
| `memory_used_gb` | Used memory in GB (35-45GB) |
| `memory_total_gb` | Total memory (80GB) |
| `temperature_celsius` | GPU temperature (55-65°C) |
| `power_draw_watts` | GPU power draw (350-450W) |

---

## 📊 Sample Data Structure

### A100 Example

```json
{
  "cluster_id": "a100-80gb-runpod",
  "timestamp": 1777248579.1373765,
  "gpus": [
    {
      "gpu_id": 0,
      "utilization_percent": 85.0,
      "memory_used_gb": 45.0,
      "memory_total_gb": 80.0,
      "temperature_celsius": 65.0,
      "power_draw_watts": 250.0
    }
  ]
}
{
  "h100-80gb-runpod": [
    {
      "cluster_id": "h100-80gb-runpod",
      "timestamp": 1777267236.1624715,
      "gpus": [
        {
          "gpu_id": 0,
          "utilization_percent": 94.0,
          "memory_used_gb": 38.0,
          "memory_total_gb": 80.0,
          "temperature_celsius": 58.0,
          "power_draw_watts": 380.0
        }
      ]
    }
  ]
}
