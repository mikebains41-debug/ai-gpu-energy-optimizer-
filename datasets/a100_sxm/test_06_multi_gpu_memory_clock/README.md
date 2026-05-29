# A100 SXM Test 06 — Multi GPU Memory Clock Divergence
## Test ID: A100_TEST_06_MULTI_GPU_MEMORY_CLOCK
## Date: 2026-05-29
## Pod: c6432c0108d6 | Provider: RunPod
## Researcher: Manmohan (Mike) Bains | mikebains41@gmail.com

## Finding
GPU0 consistently higher than GPU1 by 1.71W.
Both GPUs memory clock locked at 1593MHz.
Simultaneous spontaneous burst on both GPUs.

## Inter GPU Differential
| GPU | Idle Power | SM Clock | MEM Clock |
|---|---|---|---|
| GPU0 | 65.74W | 210MHz | 1593MHz |
| GPU1 | 63.99W | 210MHz | 1593MHz |
| Differential | 1.75W | 0MHz | 0MHz |

## Spontaneous Burst — Both GPUs Simultaneous
| GPU | Burst Power | SM Clock | MEM Clock | Util |
|---|---|---|---|---|
| GPU0 | 86.13W | 1140MHz | 1593MHz | 0% |
| GPU1 | 84.36W | 1140MHz | 1593MHz | 0% |

## Files
- README.md — this file
- SUMMARY.md — test summary
- metrics.json — structured metrics
- evidence.json — evidence data
- raw_data.csv — raw telemetry

## Conclusion
Hardware asymmetry confirmed. Memory clock locked on both GPUs.
Spontaneous bursts are coordinated across GPUs — not random.
