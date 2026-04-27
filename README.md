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
### Example response (H100):

{
  "h100-runpod": [
    {
      "cluster_id": "h100-runpod",
      "timestamp": 1777267236.1624715,
      "gpus": [{
        "gpu_id": 0,
        "utilization_percent": 94.0,
        "memory_used_gb": 38.0,
        "memory_total_gb": 80.0,
        "temperature_celsius": 58.0,
        "power_draw_watts": 380.0
      }]
    }
  ]
}

## 🔜 Roadmap (Next Phase)

| Feature | Status | Target |
|---------|--------|--------|
| Power capping via API | 
| Auto-optimization (reduction logic) |
| Real-time power adjustment |
| Kubernetes auto-scaler integration |
##

📊 24-Hour Test Validation coming soon

| # | Metric / Feature | Status |
|---|-----------------|--------|
| **CURRENT METRICS**were tested over 8 hrs|
| 1 | Power monitoring (watts) | ✅ 
| 2 | Temperature monitoring (°C) 
| 3 | GPU utilization (%) | ✅ 
| 4 | Memory monitoring (GB) | ✅ 
| 5 | Timestamps (every 10 sec) | ✅
| 6 | A100 live data | ✅ 
| 7 | H100 live data | ✅ 
| 8 | Dashboard display | ✅
| 9 | API endpoints | ✅ 
| **NEW FEATURES** |
| 10 | Throttling prediction | 📋 Planned |
| 11 | Cost calculator ($ savings) | 📋 Planned |
| 12 | Efficiency score (util/W) | 📋 Planned |
| 13 | Power capping logic | 📋 Planned |
| 14 | PCIe bandwidth monitoring | 📋 Planned |
| 15 | GPU clock speed | 📋 Planned |
| 16 | Memory clock speed | 📋 Planned |
| 17 | Throttle reason | 📋 Planned |
---

This project is currently a
**live monitoring and throttling prediction platform**. The next
phase — automatic power capping
and energy optimization — is ready for development with the right partner.

Contact: mikebains41@gmail.com
