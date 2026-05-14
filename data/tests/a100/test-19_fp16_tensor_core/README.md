# Test 19 – FP16 Tensor Core Efficiency (10‑minute Continuous Matmul)

## 1. Purpose
To measure the real‑world energy efficiency of FP16 matrix multiplication using tensor cores on an A100 SXM, and to compare it against the FP32 baseline (Test C). The test evaluates whether the advertised speedup of tensor cores translates into better energy efficiency (FLOPs per Joule) or comes at a power cost.

## 2. Test Environment
- **GPU:** NVIDIA A100 SXM (RunPod)
- **CUDA:** 12.4, PyTorch 2.4.1
- **Workload:** Continuous 2048×2048 FP16 matrix multiplication (`torch.matmul`)
- **Duration:** 600 seconds (10 minutes)
- **Sampling rate:** 1 Hz (nvidia-smi)
- **Additional metrics:** Power (W), GPU utilisation (%), temperature (°C)

## 3. Protocol
- A single pair of 2048×2048 FP16 tensors was allocated on the GPU.
- The test ran for 600 seconds, executing 100 matmuls per second (≈ 60,000 iterations total).
- Every second, `nvidia-smi` logged timestamp, power draw, utilisation, and temperature.
- The average power was computed from the entire 600‑second log.
- Total energy = average power × 600 s.
- CEI (Compute Efficiency Index) = total FLOPs / total energy (Joules).

## 4. Key Results

| Metric | Value |
|--------|-------|
| Average power | **482.70 W** |
| Power range | 66.75 – 501.86 W |
| Utilisation | 0% (first 2 seconds), then 100% |
| Temperature range | 27 – 49°C |
| Total iterations | 60,000 |
| Total FLOPs | 1.030 × 10¹⁵ |
| Total energy | 289,620 J |
| CEI (FLOPs/J) | **3.56 × 10⁹** |

## 5. Comparison with FP32 (Test C)

| Metric | FP32 (Test C) | FP16 (Test 19) | Difference |
|--------|---------------|----------------|------------|
| Average power | 302.37 W | 482.70 W | +60% |
| CEI (FLOPs/J) | 5.68 × 10⁹ | 3.56 × 10⁹ | -37% |

**Key observation:** FP16 completes each kernel faster (tensor core speedup), but the GPU draws **significantly more board power** during sustained FP16 execution. On this A100 SXM, FP16 is **less energy‑efficient** than FP32 for this matrix size.

## 6. Interpretation
- The increase in power (from 302 W to 483 W) suggests that tensor core operations trigger a higher‑power state (likely higher memory controller or core clock) that outweighs the benefit of shorter kernel times.
- This result is counter‑intuitive to the common belief that “FP16 = faster and greener”. For energy‑conscious scheduling, the workload size and architecture must be considered.
- The finding is specific to the A100 SXM; H100 may behave differently (its FP16 CEI is higher than FP32, as shown in H100 test‑08).

## 7. Significance for GPU Energy Optimizer
- The tool successfully quantifies the **real‑world energy efficiency** of different precision modes.
- It reveals that **faster is not always more efficient** – a critical insight for workload placement and power cap decisions.
- The CEI metric allows direct comparison of energy efficiency across architectures and precisions.

## 8. Raw Data Access
- Full CSV log: `data.csv` in this folder.
- Screenshots: `screenshots/` folder showing the `awk` average calculation and sample log lines.

## 9. Conclusion
Test 19 demonstrates that on an A100 SXM, FP16 tensor cores draw 60% more power than FP32 for the same matrix size, resulting in a 37% lower CEI (energy efficiency). This challenges the assumption that mixed‑precision always saves energy and highlights the need for workload‑specific efficiency profiling – exactly what the GPU Energy Optimizer provides.

---

*Part of the GPU Energy Optimizer validation suite – May 13, 2026*
