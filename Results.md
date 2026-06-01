# GPU Energy Optimizer – Validation Report
**Author:** Manmohan (Mike) Bains  
**Updated:** 2026-05-31  
**Repository:** github.com/mikebains41-debug/ai-gpu-energy-optimizer-

## Executive Summary

72+ validated hardware tests across 7 GPU architectures confirming two major research tracks — ghost power energy findings and VRAM security vulnerability.

**CVE Request 2048350 filed 2026-05-31.**

## Security Findings — VRAM Residual Data Leakage

Previous tenant computation data remains readable in GPU VRAM after graceful PyTorch process exit.

| GPU | Residual After Graceful Exit | SIGKILL |
|---|---|---|
| A100 SXM 80GB | 457-465 MB | 0 MB |
| H100 SXM | 527 MB | not tested |
| H200 SXM 141GB | 529-629 MB single, 1630 MB full profile | not tested |
| B200 SXM 179GB | 628-728 MB fixed | not tested |

- Cross-GPU isolation failure confirmed on H200 — GPU1 retained 528MB from GPU0 despite GPU1 idle
- NVML reports 0% memory utilization throughout all phases
- Process exits code 0 while 1630MB remains exposed
- Root cause: PyTorch CUDA memory allocator above driver layer
- PCIe GPUs — T4, A100 PCIe, RTX 4090 — confirmed clean 0MB residual

## Energy Findings — Ghost Power

| GPU | Ghost Power | Notes |
|---|---|---|
| A100 SXM | 65-146W at 0% util | Post-load trigger |
| H100 SXM | None | Clean — Hopper HBM2e |
| H200 SXM | 79-136W post-load | HBM3e elevated |
| B200 SXM | 144W cold boot, 549-574W spike | Worst case |

- HBM memory clock locked at full speed 24/7 — A100 1593MHz, B200 3996MHz
- Ghost power is Ampere and Blackwell generation specific
- H100 Hopper HBM2e confirmed clean

## Performance Findings

- FP32 CEI: 5.68e9 FLOPs/J on A100 SXM
- FP16 draws 483W vs FP32 302W — 60% higher
- Idle floors: T4 9.5W, RTX 4090 20W, A40 30.4W, A100 PCIe 47W, A100 SXM 67W, H100 SXM 70W
- B200 NVML completely blind — 0% reported at 400-700W real compute

## Raw Data

All CSV logs, JSON summaries, and evidence files publicly available:

- datasets/a100_sxm/ — 22 tests including memory clock and VRAM series
- datasets/h100_sxm/ — 9 tests including VRAM series
- datasets/h200_sxm/ — 6 VRAM tests
- datasets/b200_sxm/ — 6 VRAM tests
- data/tests/a100/ — test-01 through test-24
- data/tests/h100/ — test-01 through test-11

## Interactive Security Findings

https://ai-gpu-energy-optimizer.vercel.app/security-findings

## Final Verdict

The AI GPU Energy Optimizer is validated as the only tool capable of detecting VRAM residual data leakage, ghost power, and NVML blindness across SXM GPU architectures. All findings are hardware-attested on RunPod cloud infrastructure at 100Hz cross-validation polling.

**End of Report — Manmohan (Mike) Bains, 2026-05-31**
