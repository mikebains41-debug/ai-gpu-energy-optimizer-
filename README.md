# AI GPU Energy Optimizer

[![Render](https://img.shields.io/badge/Render-Live-brightgreen)](https://ai-gpu-brain-v3.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)

**Real-time GPU energy optimization for A100, H100, and AI factories.** Monitor power, temperature, and throttling. Predict OC levels before hardware throttling occurs. Deploy in 60 seconds.

Built entirely on a Samsung S25 Ultra – no laptop, no desktop.just out of curiosity.

---

## 🚀 Live Demo

| Link | URL |
|------|-----|
| **Backend API** | https://ai-gpu-brain-v3.onrender.com |
| **API Docs** | https://ai-gpu-brain-v3.onrender.com/docs |
| **Frontend Dashboard** | https://ai-gpu-energy-optimizer.vercel.app |

---

## 💡 GPU Optimizer — Energy Efficiency Layer for AI Infrastructure

### Overview

GPU Optimizer is a lightweight software layer designed to improve energy efficiency across existing GPU clusters.

It works with current infrastructure (including A100 and H100 GPUs) and can be deployed quickly without requiring hardware changes or workload modifications.

### What It Does

GPU Optimizer helps reduce unnecessary power usage by improving how GPUs are utilized in real time.

Key capabilities include:

- Adjusting GPU power states based on workload demand
- Reducing idle or underutilized GPU consumption
- Improving workload distribution across available resources
- Supporting existing schedulers such as Kubernetes or Slurm

### Expected Impact

Results will vary depending on workload and infrastructure, but typical outcomes may include:

- Lower overall energy consumption
- Improved GPU utilization
- Reduced cooling and thermal load

In some environments, this can translate into meaningful cost savings over time.

### Deployment

- No hardware upgrades required
- No changes to existing models or training pipelines
- Minimal setup time (typically under a minute)
- Designed to integrate with existing systems

### Who It's For

- Teams operating GPU clusters for AI training or inference
- Data center operators looking to improve efficiency
- Organizations managing large-scale compute workloads

### Longer-Term Direction

Over time, GPU Optimizer could expand into a broader system for managing energy efficiency across compute environments, including:

- Monitoring and reporting GPU efficiency
- Energy-aware workload scheduling
- Optimization across multiple clusters or regions

### Summary

GPU Optimizer is intended to be a simple, low-friction way to improve efficiency in GPU-based systems—without requiring changes to existing infrastructure.

The goal is to provide measurable improvements while fitting naturally into current workflows.

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

### Example response (A100):

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
