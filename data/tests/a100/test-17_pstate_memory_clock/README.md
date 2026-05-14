# Test 17 – P-State & Memory Clock Retention

## Protocol  
- 30-second load (matrix multiplication) followed by 10 minutes of monitoring.  
- Every minute, `nvidia-smi -q` captured Performance State and Memory Clocks.

## Results  
- Performance State: **P0** for all 10 minutes.  
- Memory Clock: **1593 MHz** (maximum) – never downclocked.  
- SM Clock: varied between 210 MHz and 1410 MHz, but memory remained at max.

## Significance  
This test proves that the A100 SXM remains in a high‑power state (P0) with memory at full speed even when the GPU is idle after a workload. This explains the persistently high idle power (67–78 W) observed in other tests and is a direct cause of telemetry desynchronisation (0% utilisation but high power).
