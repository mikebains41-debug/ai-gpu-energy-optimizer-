# Test 21 – FP32 vs FP16 Performance (60 Iterations Each)

## Purpose
To compare the execution time, power draw, and reported GPU utilisation of FP32 and FP16 matrix multiplication on an A100 SXM, and to verify whether the known speedup of tensor cores is accompanied by a change in power or telemetry behaviour.

## Environment
- **GPU:** NVIDIA A100 SXM (RunPod)
- **CUDA:** 12.4, PyTorch 2.4.1
- **Workload:** 2048×2048 FP32 and FP16 matrix multiplication (`torch.matmul`)
- **Iterations:** 60 per precision (after warm‑up)
- **Metrics per iteration:** kernel time (ms), timestamp, power (W), utilisation (%), temperature (°C)
- **Sampling:** nvidia-smi at 1 Hz (power reading may span several kernels)

## Protocol
1. Allocate two pairs of tensors (FP32 and FP16) on the GPU.
2. Execute 3 warm‑up iterations (not recorded) to stabilise clocks.
3. Run 60 iterations of FP32 matmul, recording each kernel time via `time.time()` and querying nvidia-smi for power/util/temp.
4. Repeat the same for FP16.
5. Exclude the first iteration of each precision (CUDA warm‑up spike) from statistical summaries.

## Results

### FP32 (60 recorded iterations)
| Metric | Value |
|--------|-------|
| Mean kernel time | **1.44 ms** |
| Std dev kernel time | 0.12 ms |
| Power range | 76 – 137 W |
| Mean power | ≈94 W |
| Utilisation | 0% (occasional 4% spikes) |
| Temperature | 44–45°C |

### FP16 (60 recorded iterations)
| Metric | Value |
|--------|-------|
| Mean kernel time | **0.48 ms** |
| Std dev kernel time | 0.15 ms |
| Power range | 76 – 79 W |
| Mean power | ≈77 W |
| Utilisation | 0–4% |
| Temperature | 45°C |

### Speedup
- **FP16 is 3× faster** than FP32 (0.48 ms vs 1.44 ms).
- Theoretical peak speedup for tensor cores is higher, but this matrix size (2048) may not be optimal.

## Key Observations
- **Power remains similar** between FP32 and FP16 (≈77–94 W). The higher power in some FP32 iterations (up to 137 W) is likely due to background temperature or power cap behaviour, not precision.
- **Reported GPU utilisation stays at 0% for the vast majority of samples** – both precisions suffer from the same telemetry blind spot observed in earlier tests.
- **The first iteration of each precision is an outlier** (63 ms for FP32, 135 ms for FP16) – due to CUDA kernel compilation and initialisation. Excluding it gives stable, reproducible results.

## Interpretation
FP16 on A100 SXM delivers a **3× speedup** without increasing board power, but the standard utilisation metric fails to capture the active compute. This reinforces the finding that `nvidia-smi` utilisation is an unreliable proxy for real GPU activity, especially for memory‑bound tensor core workloads.

## Significance for GPU Energy Optimiser
- The CEI (Compute Efficiency Index) for FP16 in this test would be higher than FP32 because kernel time is shorter while power is similar. This is a different conclusion from the 10‑minute sustained FP16 test (Test 19), where power was much higher. This highlights the importance of **sustained workload profiling** – short bursts may not reflect long‑run power behaviour.
- The optimiser successfully captures per‑iteration timing and power, enabling fine‑grained efficiency analysis.

## Raw Data
- Full CSV with 120 rows: `data.csv`
- Screenshots: `screenshots/` folder (5 images)

## Conclusion
Test 21 demonstrates that FP16 tensor cores are significantly faster than FP32 on an A100 SXM, with similar power draw and the same telemetry blind spot. The data is reproducible and adds to the body of evidence that standard GPU utilisation metrics are insufficient for energy‑aware scheduling.
