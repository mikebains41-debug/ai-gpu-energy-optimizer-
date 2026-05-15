# GPU Energy Optimizer

**Author:** Manmohan Bains  
**Contact:** mikebains41@gmail.com  
**Live API:** [https://ai-gpu-brain-v3.onrender.com/docs](https://ai-gpu-brain-v3.onrender.com/docs)  
**Status:** Active — open to partnership

---

## What This Is

A production GPU energy observability platform that detects, measures, and compares real power behavior across NVIDIA AI accelerators. Built from live telemetry collected on RunPod infrastructure across A100 SXM and H100 SXM GPUs.

---

## Key Findings

- **Ghost power confirmed:** A100 SXM draws up to 146.7 W at 0% reported utilization
- **Idle floor:** 67.1 W on A100, 69.5 W on H100
- **CEI (FP32):** 5.68 billion FLOPs per joule on A100 SXM
- **FP16 power:** 60% higher than FP32 at equivalent matrix size
- **Telemetry desync:** Confirmed across multiple test runs
- **Hypervisor restrictions:** Persistence mode and power capping blocked on RunPod

---

## API Endpoints (Live)

| Endpoint | URL |
|----------|-----|
| A100 Live Metrics (if agent active) | [https://ai-gpu-brain-v3.onrender.com/metrics/a100](https://ai-gpu-brain-v3.onrender.com/metrics/a100) |
| H100 Live Metrics (if agent active) | [https://ai-gpu-brain-v3.onrender.com/metrics/h100](https://ai-gpu-brain-v3.onrender.com/metrics/h100) |
| A100 Recorded Test Results (24 tests) | [https://ai-gpu-brain-v3.onrender.com/results/a100](https://ai-gpu-brain-v3.onrender.com/results/a100) |
| H100 Recorded Test Results (11 tests) | [https://ai-gpu-brain-v3.onrender.com/results/h100](https://ai-gpu-brain-v3.onrender.com/results/h100) |
| Full API Documentation | [https://ai-gpu-brain-v3.onrender.com/docs](https://ai-gpu-brain-v3.onrender.com/docs) |
| Frontend Dashboard | [https://ai-gpu-energy-optimizer.vercel.app](https://ai-gpu-energy-optimizer.vercel.app) |

---

## What the API Does

**51 endpoints** covering:

- Real‑time ghost power detection
- Compute Energy Intensity (CEI) benchmarking
- A100 vs H100 comparative analysis
- FP32 vs FP16 vs FP8 efficiency comparison
- Matrix size scaling analysis (2048 to 8192)
- Prometheus metrics export
- Grafana dashboard integration
- SSE replay of recorded test runs
- Job tracking and duration measurement

---

## The CEI Standard

Compute Energy Intensity (CEI) is a metric defined by this project: it measures floating‑point operations delivered per joule during a sustained workload. Reference values and full methodology are available at:  
[https://ai-gpu-brain-v3.onrender.com/standards/cei](https://ai-gpu-brain-v3.onrender.com/standards/cei)

---

## Validated On

| Provider | GPU | Tests |
|----------|-----|-------|
| RunPod | A100 SXM | 24 |
| RunPod | H100 SXM | 11 |

**Pending:** AWS, CoreWeave, Lambda Labs, Vast.ai

---

## Partnership

This project is open to:

- Cloud GPU compute credits
- Data center access (AWS, CoreWeave, Lambda, Vast)
- Research collaboration
- Seed funding

Source code is available upon request for verified partners and sponsors.

**Contact:** [mikebains41@gmail.com](mailto:mikebains41@gmail.com)  
**API Docs:** [https://ai-gpu-brain-v3.onrender.com/docs](https://ai-gpu-brain-v3.onrender.com/docs)  
**Sponsor endpoint:** [https://ai-gpu-brain-v3.onrender.com/sponsor](https://ai-gpu-brain-v3.onrender.com/sponsor)

---

## Roadmap

- Migrate test data from flat files to TimescaleDB for scalable time‑series storage and real‑time query performance
- Redis Streams for live multi‑GPU telemetry ingestion at scale
- Celery background workers for continuous ghost power detection
- Per‑provider API key management with RBAC
- Redis pub/sub for multi‑instance WebSocket broadcasting
- Validation across AWS, CoreWeave, Lambda Labs, and Vast.ai

---

## About

AI + GPU + Energy Optimization Platform | Real‑time dashboard for data center GPU workloads, power efficiency, heat reuse, and AI‑driven energy scheduling.

© 2026 Manmohan Bains. All rights reserved.  
Proprietary software – no unauthorized copying, modification, or distribution.
