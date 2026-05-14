# A100 8192 Load Test – RunPod

## Test Overview
- **GPU:** A100 SXM (8192 matrix size)
- **Platform:** RunPod
- **Date:** May 11, 2026
- **Duration:** 20 minutes load
- **Workload:** 8192×8192 FP32 matrix multiplication

## Results
- Power draw stable between 305 W and 342 W
- GPU utilization 100% throughout
- No sustained ghost power (utilization never drops to 0% during load)

## Files
- `data.csv` – raw power and utilization logs
