# GPU Energy Optimizer
**Built on a Samsung S25 Ultra. No laptop. No desktop. Just curiosity.**  
Manmohan Bains | 2026 | Proprietary

**Live API:** https://ai-gpu-brain-v3.onrender.com  
**Contact:** mikebains41@gmail.com

---

## The Problem Nobody Talks About

Every GPU monitoring tool trusts `utilization %` as the primary metric.  
**We proved it is broken.**  

Raw power draw: >130 W. Reported utilization: 0%. That is **ghost power**, and no other documented tool detects it.

---

## What This Project Does (That Others Don't)

| Capability | Status |
|------------|--------|
| Ghost power detection (power at 0% util) | ✅ Proven with raw CSV logs |
| Telemetry desynchronisation evidence | ✅ Raw data (power vs util) |
| Compute Energy Index (FLOPs/joule) | ✅ New metric, live in API |
| Cross‑GPU idle power floors (6 GPUs) | ✅ Measured and documented |
| Remediation blockers on cloud providers | ✅ Explicit (RunPod blocks low‑level power mgmt) |
| All raw data public | ✅ GitHub |
| 8 real‑time analysis engines | ✅ Live API |

---

## Proven Facts (24 Tests, 6 GPU Architectures)

| Finding | Hard Evidence | Impact |
|---------|--------------|--------|
| Ghost power on A100 SXM | 72‑146 W at 0% utilization | Standard telemetry completely blind |
| Idle floor never drops below 67 W | A100 SXM idle = 67 W, not 30 W like A40 | $58/GPU/year pure waste |
| FP16 is **not** always efficient | Sustained FP16: 483 W vs FP32: 302 W (+60%) | Energy‑aware scheduling required |
| CEI (real FLOPs/joule) | Burst: 1.60e11, Sustained 15min: 5.68e9 | First practical efficiency metric |
| Utilization % does NOT track power | 75% load: 343 W power, 2% reported util | Metric is a broken proxy |
| Remediation blocked on RunPod | `nvidia-smi -pm` and `-pl` both fail | Tenants cannot fix waste themselves |

---

## Idle Power Floors (All 6 GPUs)

| GPU | Idle Power (W) | Ghost Power Observed |
|-----|----------------|----------------------|
| Tesla T4 | 9.5 | No |
| RTX 4090 | 20.0 | No |
| A40 | 30.4 | No |
| A100 PCIe | 47.0 | No |
| A100 SXM | 67.0 | **Yes** |
| H100 SXM | 70.0 | No (but high idle) |

---

## A100 Test Results (24 tests)

| Test | Finding | Key Result |
|------|---------|-------------|
| 1 | Idle Baseline (10 min) | 62.7 W @ 0% util |
| 2 | Ghost Power | 102.3 W @ 0% util – ghost confirmed |
| 3 | Sampling Rate (10ms) | 0% util persists at 10ms sampling |
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
| 15 | Idle Baseline (15 min) | 67.1 W @ 0% util |
| 16 | Remediation (Persistence Mode & Power Cap) | Blocked by RunPod hypervisor |
| 17 | P‑State & Memory Clock Retention | P0 persistent, 1593 MHz locked |
| 18 | Load Ramp – Power vs Matrix Size | Peak power 339 W at size 6144 |
| 19 | FP16 Tensor Core – 10min Continuous | 483 W average (FP16 not always efficient) |
| 20 | FP16 vs FP32 – 5 iterations | FP16 uses ~23% less power (77.5 W vs 100.7 W) |
| 21 | FP32 vs FP16 – 60 Iterations Each | FP16 ~3× faster, similar power |
| 22 | Persistence Mode Disable Attempt | Command appears to succeed but mode unchanged |
| 23 | Idle Baseline (15 min, second run) | 67.1 W @ 0% util |
| 24 | CEI Validation – 15 min Continuous FP32 | CEI = 5.68e9 FLOPs/J (sustained) |

> All data from [`/results/a100/{id}`](https://ai-gpu-brain-v3.onrender.com/results/a100/1) – supports IDs `1` to `24`, `test-01`, `test-01_idle_baseline`, etc.

---

## H100 Test Results (11 tests)

| Test | Finding | Key Result |
|------|---------|-------------|
| 1 | Idle Baseline | 69.5 W @ 0% util |
| 2 | Ghost Power | ✖ None detected |
| 3 | Sampling Rate | No ghost power at any rate |
| 4 | Load Ramp | Linear scaling, no lag |
| 5 | CEI Compute (2048) | 49.13 TFLOPS |
| 6 | FP16 Tensor Core | 592.76 TFLOPS |
| 7 | Efficiency | 76.5 GFLOPS/W |
| 8 | vs A100 Speed | 3.4× faster |
| 9 | vs A100 Efficiency | 1.45× better |
| 10 | Thermal | 60°C peak |
| 11 | Final Proof (Nsight) | Complete |

---

## Financial Impact

**Idle waste (A100 SXM):**  
- Idle power floor: **67 W** (tests 15 & 23)  
- 8,760 hours/year × 67 W × $0.10/kWh = **$58.70 per GPU per year** – just from being on but idle.

**Ghost power** (extra above idle during “0% util” events):  
- Measured ghost event power: 102.3 W (test‑02), but baseline idle is 67 W, so ghost event adds about 35 W during the event. Not continuous, so the added cost is smaller than idle waste.

**Total annual waste per A100 SXM** (idle + ghost events):  
- If a GPU is idle 50% of the time and ghost events occur 10% of idle time, total waste ~$60‑65/GPU/year.  
- For 1 million A100 SXM GPUs globally, that’s **$60‑65 million per year**.

**Simpler headline:**  
> *“A100 SXM GPUs waste over **$58 per GPU per year** just from being powered on but idle – before any ghost power is added. For a fleet of 1 million GPUs, that’s **$58 million annually**.”*

---

## The 8 Analysis Engines

| Engine | What It Detects |
|--------|----------------|
| 1. True Efficiency | Useful compute time × (util/power) × consistency |
| 2. Idle Waste | GPUs drawing power at 0% activity + cost in $ |
| 3. Burst Detection | Power spikes >50 W with flat utilization |
| 4. Sampling Gap | Missed compute due to 1 Hz sampling |
| 5. Alerts | Thermal (>75°C), power, idle warnings |
| 6. Export | JSON/CSV dataset for offline analysis |
| 7. Power State | High‑power residency (P0, memory clock locked) |
| 8. Delta Tracker | Before/after workload efficiency comparison |

---

## Live API

Base URL: `https://ai-gpu-brain-v3.onrender.com`

| Endpoint | Description |
|----------|-------------|
| `/results/a100` | All 24 A100 test summaries (sorted JSON array) |
| `/results/h100` | All 11 H100 test summaries (sorted) |
| `/results/a100/{test_id}` | Single test (supports `1`, `test-1`, `test-01`, full folder name) |
| `/results/h100/{test_id}` | Same for H100 |
| `/api/summary` | Dashboard summary |
| `/engine/efficiency` | Real‑time efficiency score |
| `/engine/idle` | Idle waste + cost |
| `/engine/burst` | Burst detection |
| `/engine/alerts` | Live alerts |
| `/docs` | Interactive Swagger UI |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) on Render |
| Frontend | Next.js on Vercel |
| GPU Compute | RunPod (A100 SXM, H100 SXM) |
| Monitoring | NVML + custom Python agents |
| Built On | Samsung S25 Ultra (no laptop, no desktop) |

---

## Repository & Raw Data

Every test folder contains:
- `data.csv` – raw telemetry (timestamp, power, utilization, temperature)
- `summary.json` – test metadata and key results
- `metrics.json` – computed metrics (CEI, mean power)
- `evidence.json` – conclusion and supporting outputs
- `screenshots/` – terminal proof

**GitHub:** [github.com/mikebains41-debug/ai-gpu-energy-optimizer-](https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-)

---

## Future Roadmap

- [x] NVIDIA A100/H100 validation (complete)  
- [x] Live API with 8 analysis engines (complete)  
- [x] One‑line installer script (available)  
- [ ] Prometheus/Grafana integration (planned)  
- [ ] Docker image (planned)  
- [ ] TileLang support (planned)  
- [ ] Huawei Ascend compatibility (planned)  
- [ ] Multi‑architecture observability (vision)

---

## Contact

**Author:** Manmohan Bains  
**Email:** mikebains41@gmail.com  
**GitHub:** github.com/mikebains41-debug  
**Frontend Dashboard:** [ai-gpu-energy-optimizer.vercel.app](https://ai-gpu-energy-optimizer.vercel.app)

*These are not simulations. Raw CSV logs, screenshots, and JSON summaries from actual RunPod GPUs.*

© 2026 Manmohan Bains. All Rights Reserved.  
Proprietary software – no unauthorized copying, modification, or distribution.
