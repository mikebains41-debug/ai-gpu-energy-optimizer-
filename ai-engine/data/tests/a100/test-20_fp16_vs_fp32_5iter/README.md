# Test 20 – FP16 vs FP32 Burst Comparison (5 Iterations)

## Protocol
- Workload: torch.matmul(2048×2048)
- Iterations: 5 per precision
- GPU: NVIDIA A100 SXM (RunPod)
- Date: 2026-05-13

## Results

| Precision | Mean Kernel Time | Avg Power | Speedup |
|-----------|-----------------|-----------|---------|
| FP32      | 1.40 ms         | 79 W      | 1×      |
| FP16      | 0.34 ms         | 77 W      | 4×      |

## Key Finding
FP16 is 4× faster than FP32 with similar board power in burst mode.

## Important Caveat
This 5-iteration burst test does **not** represent sustained workload behaviour.
See **Test-21** (60 iterations) and **Test-19** (10-minute sustained FP16) which show
FP16 drawing **483W vs FP32 302W** — a 60% power increase under sustained load.

## Significance
Short burst tests can mislead energy analysis. This test motivated the design
of longer sustained tests (Test-19, Test-21, Test-24) for accurate CEI measurement.
