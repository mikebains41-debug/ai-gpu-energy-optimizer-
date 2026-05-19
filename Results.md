# GPU Energy Optimizer – Final Validation Report

**Author:** Manmohan Bains  
**Date:** May 13, 2026  
**Repository:** [github.com/mikebains41-debug/ai-gpu-energy-optimizer-](https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-)

## Executive Summary
Over 40 controlled test runs on six GPU architectures (A100 SXM, A100 PCIe, H100 SXM, A40, RTX 4090, T4), we have demonstrated that standard GPU telemetry (nvidia‑smi, DCGM) systematically under‑reports real compute activity and energy waste. Key findings:

- **Ghost power (telemetry desynchronisation):** A100 SXM draws up to 146 W while reported utilisation is 0% – both during sustained matrix multiplication and forced idle. Idle floor ~67 W.
- **Compute Efficiency Index (CEI):** 15‑minute sustained FP32 CEI = 5.68 × 10⁹ FLOPs/J (Test‑24).
- **FP16 vs FP32:** Sustained FP16 draws 483 W – 60% higher than FP32 (302 W).
- **Remediation blocked by RunPod:** Persistence mode and power cap changes are impossible on standard RunPod instances.
- **Cross‑architecture idle floors:** T4 9.5 W, RTX 4090 20 W, A40 30.4 W, A100 PCIe 47 W, A100 SXM 67 W, H100 SXM 70 W.

## Raw Data & Reproducibility
All CSV logs, JSON summaries, screenshots, and analysis scripts are in this repository:
- A100 tests: `data/tests/a100/test-01/` to `test-24_cei_15min/`
- H100 tests: `data/tests/h100/test-01/` to `test-11/`
- Other GPUs: A40, RTX 4090, T4, A100 PCIe under respective folders.

Each test folder contains `data.csv`, `summary.json`, `metrics.json`, `evidence.json`, `README.md`, and `screenshots/`. The repository is private; access can be granted upon request.

## Final Verdict
The GPU Energy Optimiser is validated as an observability framework that exposes hidden energy waste and telemetry desynchronisation. The data is real, the product works, and the insights are actionable.

*End of Report – Manmohan Bains, May 13, 2026*
