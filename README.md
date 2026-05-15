# GPU ENERGY OBSERVABILITY PLATFORM

**Built on a Samsung S25 Ultra – No laptop, no desktop. Just curiosity.**  
Manmohan Bains | 2026 | Proprietary

**API Base URL:** [https://ai-gpu-brain-v3.onrender.com](https://ai-gpu-brain-v3.onrender.com)  
**Contact:** [mikebains41@gmail.com](mailto:mikebains41@gmail.com)

---

## WHAT I DISCOVERED

A100 GPUs draw significant power while reporting 0% utilization to standard monitoring tools. Every major monitoring tool misses this completely.

| Discovery | Evidence | Impact |
|-----------|----------|--------|
| Ghost Power (telemetry desync) | A100 drew 102.3W at 0% utilization | Standard monitoring missed active compute |
| 10ms Sampling Still Shows 0% | 100x faster sampling could not capture it | Not a sampling issue – persistent blind spot |
| Power Spikes Before Utilization | 75% load: 343W power, 2% reported util | Utilization metric lags behind reality |
| FP16 Tensor Cores: 16x Faster | A100 FP32: 14.35 TFLOPS, FP16: 231 TFLOPS | Massive efficiency gain at no power cost |
| Optimal Matrix Size: 4096 | Peak CEI of 1.610e+13 FLOPs/sec | 20% more efficient than 2048 |

---

## WHAT THIS IS

A GPU observability platform that reveals what standard monitoring tools miss, using recorded test data from actual A100 and H100 GPUs on RunPod.

---

## API ENDPOINTS (RECORDED TEST DATA)

| Endpoint | URL |
|----------|-----|
| A100 Real‑time Metrics (if agent active) | [https://ai-gpu-brain-v3.onrender.com/metrics/a100](https://ai-gpu-brain-v3.onrender.com/metrics/a100) |
| H100 Real‑time Metrics (if agent active) | [https://ai-gpu-brain-v3.onrender.com/metrics/h100](https://ai-gpu-brain-v3.onrender.com/metrics/h100) |
| A100 Test Results (all 24) | [https://ai-gpu-brain-v3.onrender.com/results/a100](https://ai-gpu-brain-v3.onrender.com/results/a100) |
| H100 Test Results (all 11) | [https://ai-gpu-brain-v3.onrender.com/results/h100](https://ai-gpu-brain-v3.onrender.com/results/h100) |
| API Documentation | [https://ai-gpu-brain-v3.onrender.com/docs](https://ai-gpu-brain-v3.onrender.com/docs) |
| Frontend Dashboard | [https://ai-gpu-energy-optimizer.vercel.app](https://ai-gpu-energy-optimizer.vercel.app) |

> **Note:** The `/results` endpoints return pre‑recorded test data. Real‑time metrics are only available if you run the monitoring agent (contact for access).

---

## THE DATA

**24 comprehensive A100 tests + 11 H100 tests** – 601 to 868,006 iterations per test. All data public and reproducible.

---

### A100 Test Results (24 tests)

| Test | Finding | Key Result |
|------|---------|-------------|
| 1 | Idle Baseline (10 min) | 62.7 W @ 0% util |
| 2 | Ghost Power | 102.3 W @ 0% util – confirmed |
| 3 | Sampling Rate (10ms) | 0% util persists at 10 ms |
| 4 | Load Ramp | Power scales 58 W → 344 W |
| 5 | CEI Compute (2048) | 14.35 TFLOPS, CEI 1.44e13 |
| 6 | CEI Efficiency (2048) | 52.6 GFLOPS/W |
| 7 | CEI Compute (4096) | 15.3 TFLOPS, CEI 1.53e13 |
| 8 | FP16 Tensor Core | 231 TFLOPS (16× FP32) |
| 9 | Normality Test | p=0.000000 (expected) |
| 10 | Log‑Log Scaling | Peak CEI at 4096 |
| 11 | Observability Validation | Ghost power events: 0 (idle 62.7 W) |
| 12 | 8192 Load Test | 305‑342 W @ 100% util |
| 13 | Load + Cooldown (Ghost Power) | Ghost power detected (73 W at 0% util) |
| 14 | Ghost Power – 10min Load + 10min Cooldown | 146 W peak load, 66 W idle floor |
| 15 | Id
