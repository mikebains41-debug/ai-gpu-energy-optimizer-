# VRAM Test 25 - Baseline
**Project:** GPU Energy Optimizer | **Researcher:** Mike Bains | mikebains41@gmail.com

## What This Test Proves
Ghost power is NOT driven by VRAM content. 0 MB used. 65.84W sustained. Burst 86W with zero VRAM.

## Key Numbers
- memory.used = 0 MB both GPUs entire session
- Ghost power GPU0 = 65.84W
- Ghost power GPU1 = 64.32W
- Driver reservation = 766 MB static
- HBM clock = 1593 MHz locked 24/7
- Coordinated burst = 86.31W + 84.62W at 22:45:13 with 0 MB VRAM

## Architecture Matrix
| GPU | Form Factor | Ghost Power |
|---|---|---|
| A100 SXM 80GB | SXM | YES 65.84W floor |
| H100 SXM | SXM | YES |
| B200 | SXM | YES 144W each |
| A100 PCIe | PCIe | No |
| T4 | PCIe | No |
| A40 | PCIe | No |
| RTX 4090 | PCIe | No |

## Next
- test-26: FP32 workload then kill
- test-27: VRAM residual 100Hz poll
- Verda bare metal A100 persistence mode ON
- H200 SXM RunPod 18usd
- MI300X AMD comparison

## Live
- https://ai-gpu-brain-v3.onrender.com
- https://ai-gpu-energy-optimizer.vercel.app
