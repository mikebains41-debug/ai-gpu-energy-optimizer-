# AI GPU Energy Optimizer

[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)
FastAPI 0.115  

---

**Real-time GPU energy optimization for A100, H100, and AI factories.** Monitor power, temperature, and throttling. Predict OC levels before hardware throttling occurs. Deploy in 60 seconds.

Built entirely on a Samsung S25 Ultra – no laptop, no desktop, just out of curiosity.

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

- 8+ hours of continuous GPU monitoring on **real RunPod hardware** (H100 SXM, A100 SXM)
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
## Live Demo

| Link    | URL    |
|---|---|
| Backend API   | https://ai-gpu-brain-v3.onrender.com    |
| API Docs    | https://ai-gpu-brain-v3.onrender.com/docs    |
| Frontend Dashboard | https://ai-gpu-energy-optimizer.vercel.app    |

---

## Live A100 Metrics

View real-time A100 GPU data:
https://ai-gpu-brain-v3.onrender.com/metrics/a100

### What the A100 data shows:

| Field    | Description    |
|---|---|
| cluster_id   | "a100-80gb-runpod" - identifies the A100 GPU cluster    |
| timestamp    | Unix timestamp (proof of continuous collection)    |
| utilization_percent | GPU utilization % (80-95%)    |
| memory_used_gb  | Used memory in GB (40-50GB)    |
| memory_total_gb | Total memory (80GB)    |
| temperature_celsius | GPU temperature (60-75°C)    |
| power_draw_watts | GPU power draw (240-270W)    |

---

## Live H100 Metrics

View real-time H100 GPU data:
https://ai-gpu-brain-v3.onrender.com/metrics/h100

### What the H100 data shows:

| Field    | Description    |
|---|---|
| cluster_id   | "h100-runpod" - identifies the H100 GPU cluster    |
| timestamp    | Unix timestamp (proof of continuous collection)    |
| utilization_percent | GPU utilization % (90-95%)    |
| memory_used_gb  | Used memory in GB (35-45GB)    |
| memory_total_gb | Total memory (80GB)    |
| temperature_celsius | GPU temperature (55-65°C)    |
| power_draw_watts | GPU power draw (350-450W)    |

---
## Test Results (A100)

Complete test results available in [RESULTS.md](RESULTS.md)

| Test | Finding | Status |
|------|---------|--------|
| 1 | Baseline idle: 58.1W @ 0% | ✅ |
| 2 | Ghost power: 102.3W @ 0% util | ✅ |
| 3 | Sampling: 0% util at 1s/100ms/10ms | ✅ |
| 4 | Load ramp: Power scales 58W→344W | ✅ |
| 5 | CEI compute (2048): 1.316e+13 FLOPs/sec | ✅ |
| 6 | CEI efficiency: 1.839e+11 FLOPs/Watt | ✅ |
| 7 | CEI compute (4096 15min): 1.510e+13 | ✅ |
| 8 | FP16 vs FP32: 10.25x faster | ✅ |
| 9 | Normality: p=0.000000 (expected) | ✅ |
| 10 | Scaling: Peak at 4096 | ✅ |
| 11 | Final Proof (Nsight) | ⏳ Pending |

**Current Classification:** Advanced Benchmarking System  
**Requires Test 11 for:** Efficiency Discovery System

## 📊 Live Metrics

**All GPU Metrics:** https://ai-gpu-brain-v3.onrender.com/metrics

## Example response (A100):

```json
{
    "a100-80gb-runpod": [
        {
            "cluster_id": "a100-80gb-runpod",
            "timestamp": 1777248579.13,
            "gpus": [
                {
                    "gpu_id": 0,
                    "utilization_percent": 85,
                    "memory_used_gb": 45.0,
                    "memory_total_gb": 80.0,
                    "temperature_celsius": 65,
                    "power_draw_watts": 250.0
                }
            ]
        }
    ]
}
{
    "h100-runpod": [
        {
            "cluster_id": "h100-runpod",
            "timestamp": 1777267236.16,
            "gpus": [
                {
                    "gpu_id": 0,
                    "utilization_percent": 94,
                    "memory_used_gb": 38.0,
                    "memory_total_gb": 80.0,
                    "temperature_celsius": 58,
                    "power_draw_watts": 380.0
                }
            ]
        }
    ]
}
## 🔍 Key Findings (H100 vs A100)

| Metric | H100 | A100 |
| :--- | :--- | :--- |
| Power Draw (peak) | 690W | 410W |
| Temperature | 60°C | 67°C |
| FP8 Support | ✅ Yes | ❌ No |
| Efficiency | Higher performance | Better power efficiency |

**Recommendation:** Run light workloads on A100. Reserve H100 for large language models (70B+ parameters
## 📬 Contact
# GPU Optimizer

Real-time GPU FinOps Intelligence Platform.

## What It Reveals

→ Standard GPU monitoring (nvidia-smi) misses micro-burst workloads
→ A100 can draw 70W+ power while reporting 0% utilization
→ 8 engines measure true compute efficiency

## Live System

- **API:** https://ai-gpu-brain-v3.onrender.com
- **Docs:** https://ai-gpu-brain-v3.onrender.com/docs
- **Frontend:** https://ai-gpu-energy-optimizer.vercel.app

## Quick Start

```bash
# Send test data to API
curl -X POST https://ai-gpu-brain-v3.onrender.com/api/v1/metrics \
  -H "Authorization: Bearer test_key_123" \
  -H "Content-Type: application/json" \
  -d '{"cluster_id":"test","timestamp":'$(date +%s)',"gpus":[{"gpu_id":0,"utilization_percent":50,"kernel_time_ms":10,"memory_used_gb":20,"memory_total_gb":80,"temperature_celsius":65,"power_draw_watts":300}]}'

- **Name:** Manmohan Bains
- **Email:** mikebains41@gmail.com
- **GitHub:** [github.com/mikebains41-debug](https://github.com/mikebains41-debug)
- **Project:** [ai-gpu-energy-optimizer.vercel.app](https://ai-gpu-energy-optimizer.vercel.app)
