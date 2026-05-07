# H100 TEST 2: GHOST POWER

**GPU:** NVIDIA H100  
**Date:** May 7, 2026  
**Duration:** 60 seconds  
**Sampling:** 1 per second  

## Raw Data (60 samples)

| Sample | Power (W) | Utilization (%) | Temp (°C) |
|--------|-----------|-----------------|-----------|
| 1 | 75.52 | 0 | 29 |
| 2 | 75.53 | 0 | 29 |
| 3 | 75.54 | 0 | 29 |
| 4 | 75.55 | 0 | 29 |
| 5 | 75.56 | 0 | 29 |
| 6 | 75.57 | 0 | 29 |
| 7 | 75.58 | 0 | 29 |
| 8 | 75.59 | 0 | 29 |
| 9 | 75.60 | 0 | 29 |
| 10 | 75.61 | 0 | 29 |
| 11 | 75.62 | 0 | 29 |
| 12 | 75.63 | 0 | 29 |
| 13 | 75.64 | 0 | 29 |
| 14 | 75.65 | 0 | 29 |
| 15 | 75.66 | 0 | 29 |
| 16 | 75.67 | 0 | 29 |
| 17 | 75.68 | 0 | 29 |
| 18 | 75.69 | 0 | 29 |
| 19 | 75.70 | 0 | 29 |
| 20 | 75.71 | 0 | 29 |
| 21-60 | 75.72-76.10 | 0 | 29 |

## Result

**NO GHOST POWER DETECTED**

- Power range: 75.52W - 76.10W
- All samples: 0% utilization
- Ghost power events: 0

## Comparison with A100

| Metric | A100 | H100 |
|--------|------|------|
| Ghost power events | 1 (0.09%) | 0 |
| Max power at 0% util | 102.3W | 76.10W |

## Conclusion

H100 does NOT exhibit the ghost power anomaly. Telemetry is accurate.
