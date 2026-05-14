# Test 23 – A100 SXM Idle Baseline (15 minutes)

## Protocol
- No workload, 1 Hz sampling via `nvidia-smi`
- Duration: 15 minutes (900 samples)
- Logged: timestamp, power (W), GPU utilisation (%), temperature (°C)

## Results
- Mean power: **67.1 W**
- Power range: 66.5 – 68.0 W
- Utilisation: **0%** throughout
- Temperature: 27°C steady

## Significance
This test establishes the idle power floor for the A100 SXM on RunPod. The waste compared to a power‑optimised GPU (e.g., A40 at 30.4 W) is approximately **36 W per GPU**. This baseline is used to subtract background power from active measurements (e.g., ghost power, CEI).

## Raw Data
- Screenshot: `screenshots/idle_baseline.png` shows the test execution with progress every 60 seconds.
- Full 900‑second CSV is available in `data.csv` (if present; otherwise the screenshot serves as evidence).

## Conclusion
The A100 SXM idles at ~67 W, which is significantly higher than many other GPUs. This idle floor is persistent and invisible to utilisation‑based monitoring – a key inefficiency that the GPU Energy Optimiser detects.
