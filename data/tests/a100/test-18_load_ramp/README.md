# Test 18 – Load Ramp (Power vs Matrix Size)

## Protocol
- 2 minutes of continuous matrix multiplication per size (512, 1024, 2048, 4096, 6144, 8192).
- Power, utilisation, and temperature logged every second.
- Averages computed over the 2‑minute window.

## Results
| Matrix Size | Average Power (W) | Utilisation (%) |
|-------------|------------------|------------------|
| 512         | 188.95           | 64-66            |
| 1024        | 288.21           | 93               |
| 2048        | 300.19           | 100              |
| 4096        | 333.05           | 100              |
| 6144        | 339.10 (peak)    | 100              |
| 8192        | 305.33           | 100              |

## Interpretation
- Power scales with workload size, saturating near 6144.
- At 8192, memory bandwidth becomes the bottleneck, causing power to drop despite 100% utilisation.
- This curve is critical for understanding power efficiency and scheduling workloads.

## Conclusion
The load ramp test successfully characterises power draw as a function of matrix size, identifying the peak power point and the region where memory limits dominate.
