# Test 20 – FP16 vs FP32 – 5 Iterations Each (2048×2048 matmul)

## Protocol
- GPU: NVIDIA A100 SXM (RunPod)
- Date: 2026/05/13
- Matrix size: 2048×2048
- FP32 iterations: 60
- FP16 iterations: 60
- Sampling: nvidia-smi 1Hz
- Workload: torch.matmul

## Results

### FP32
| Metric | Value |
|--------|-------|
| Avg time per iteration | 2.45ms |
| Avg power | 98.73W |
| Power range | 76.06W to 137.28W |
| Avg utilization | 0% |
| Temperature | 44C |
| Ghost power detected | Yes |

### FP16
| Metric | Value |
|--------|-------|
| Avg time per iteration | 0.52ms |
| Avg power | 77.61W |
| Power range | 76.69W to 78.72W |
| Avg utilization | 0-4% |
| Temperature | 45C |
| Ghost power detected | No |

## Key Findings
- FP16 is 4.7x faster than FP32 at this matrix size
- FP32 draws 21% more power on average
- FP32 shows DESYNC ghost power — power ramping from 76W to 137W at 0% utilization
- FP16 telemetry is stable — no ghost power behavior

## Conclusion
For 2048x2048 matrix workloads, FP16 is the clear choice — faster, lower power, and stable telemetry. FP32 exhibits ghost power behavior that inflates cost and obscures true GPU utilization.
