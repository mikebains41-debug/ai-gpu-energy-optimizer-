# Test 24 – CEI Validation (15 min Continuous FP32 Matmul)

## Protocol
- 15 minutes (900 seconds) of continuous 2048×2048 FP32 matrix multiplication.
- 100 matmuls per second (90,000 total iterations).
- Power logged every second via `nvidia-smi`.
- Total energy = average power × total time.
- CEI = total FLOPs / total energy.

## Results
- **Average power:** 302.37 W
- **Total FLOPs:** 1.55 × 10¹⁵
- **Total energy:** 272,130 J
- **CEI (FLOPs/J):** 5.68 × 10⁹

## Interpretation
This CEI value represents the real‑world energy efficiency of sustained FP32 matrix multiplication on an A100 SXM. It is significantly lower than per‑kernel approximations (e.g., 1.6×10¹¹ from short burst tests) because it includes idle‑time overhead and power integration. This is a more realistic metric for long‑running workloads.

## Significance
- Provides a baseline for comparing other workloads (e.g., FP16, different matrix sizes).
- Demonstrates the GPU Energy Optimiser’s ability to compute integrated energy efficiency over extended runs.
- Useful for capacity planning and workload scheduling in data centres.

## Raw Data
- Screenshots show the test execution with progress every 60 seconds.
- Full CSV was saved to `/tmp/cei_15min.csv` (not uploaded to GitHub, but the summary numbers are sufficient).

## Conclusion
Test 24 successfully validates the CEI metric over a 15‑minute sustained workload, producing a stable, defensible efficiency number (5.68 GFLOPs/J). This complements the shorter‑duration CEI tests and strengthens the overall methodology.
