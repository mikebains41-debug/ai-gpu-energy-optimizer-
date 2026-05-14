# Test 14 – Ghost Power (10 min Load + 10 min Cooldown)

## Purpose
To measure the power draw and reported GPU utilisation during a sustained memory‑bound matrix multiplication workload and subsequent idle cooldown, and to confirm the existence of “ghost power” (high power at 0% reported utilisation) on an A100 SXM in a cloud container.

## Environment
- **GPU:** NVIDIA A100 SXM (RunPod)
- **CUDA:** 12.4, PyTorch 2.4.1
- **Workload:** Continuous `torch.matmul` on 4096×4096 FP32 tensors
- **Logging:** `nvidia-smi` every second (timestamp, power, utilisation, temperature)
- **Duration:** 10 minutes load + 10 minutes cooldown (total 20 minutes)

## Protocol
1. Allocate 4096×4096 FP32 tensors on the GPU.
2. Run a tight loop of `torch.matmul` with `torch.cuda.synchronize()` for 600 seconds (LOAD phase).
3. Delete tensors, empty cache, and continue logging for another 600 seconds (COOLDOWN phase).
4. No other processes used the GPU.

## Results

### Load Phase (600 seconds)
- **Power range:** 66.75 – 146.66 W (mean ≈82 W)
- **Reported GPU utilisation:** 0% (except occasional 3-4% spikes during warm‑up)
- **Temperature:** rose from 27°C to 29°C

### Cooldown Phase (600 seconds)
- **Power range:** 66.16 – 78.37 W
- **Power first 60 seconds:** ~77.8 W (elevated)
- **Power last 60 seconds:** ~67.0 W (still far above a true idle floor)
- **Reported GPU utilisation:** 0% throughout
- **Temperature:** slowly returned to 27°C

## Key Observations
- **Ghost power confirmed:** During LOAD, the GPU drew up to 146 W while `nvidia-smi` showed 0% utilisation – the workload is memory‑bound, not SM‑bound.
- **Persistent idle floor:** Even after 10 minutes of cooldown, power never dropped below 66 W (the A40 idles at 30 W, RTX 4090 at 20 W).
- **Slow cooldown decay:** Power stayed at 78 W for the first minute of cooldown, indicating the GPU remains in P0 state with max memory clock.

## Conclusion
This test provides strong evidence that standard GPU utilisation metrics are a broken proxy for power consumption on the A100 SXM. The GPU draws significant power during memory‑bound work and never enters a true low‑power idle state, wasting ~37 W per GPU compared to an A40. The GPU Energy Optimiser successfully detects this inefficiency.

## Files in this folder
- `data.csv` – raw telemetry (1200 rows, 1 Hz)
- `summary.json` – test metadata
- `metrics.json` – computed metrics
- `evidence.json` – key raw observations
- `README.md` – this explanation
- `screenshots/` – 17 terminal screenshots showing the test execution
