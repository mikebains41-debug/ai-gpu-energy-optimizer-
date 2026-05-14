# RTX 4090 Ghost Power Test – RunPod Cloud

## Test Overview

- **GPU:** NVIDIA RTX 4090 (Ada Lovelace)
- **Platform:** RunPod Cloud (`a9df9bc407a4`)
- **Date:** May 12, 2026
- **Duration:** 30 minutes (5 min warmup, 20 min load, 5 min cooldown)
- **Workload:** Continuous 4096×4096 FP32 matrix multiplication (`torch.mm`)

## Result

**PASS – No sustained ghost power detected**

- Peak transient reading: 351 W (immediately post‑load, one sample)
- Three transient events, all within 3 seconds of load end
- Recovery to ~20 W idle in <4 seconds
- One secondary blip: 58.97 W (driver/memory clock transition, resolved in 2 sec)
- Stable idle power: 20 W for the remaining 5‑minute cooldown (150+ samples)

## Files in this folder

- `data.csv` – raw nvidia-smi log (timestamp, power, util)
- `ghost_events_screenshot.jpg` – visual proof of flagged events
- `summary.json`, `metrics.json`, `evidence.json` – structured test data
- `README.md` – this file

## Interpretation

The RTX 4090 behaves as expected for consumer Ada Lovelace architecture.  
The elevated readings are **normal power ramp‑down artifacts**, not telemetry desynchronization.  
This test serves as a **clean control** – the methodology correctly passes GPUs that do not exhibit ghost power, strengthening the validity of the A100 failure.

## Contact

Part of the GPU Energy Optimizer project – Manmohan Bains
