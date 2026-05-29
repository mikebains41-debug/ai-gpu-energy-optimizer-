# A100 SXM Test 03 — FP16 Load Memory Clock
## Test ID: A100_TEST_03_FP16_MEMORY_CLOCK
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains | mikebains41@gmail.com

## Finding
Memory clock locked at 1593MHz during FP16 tensor core workload.
FP16 SM clock lower than FP32 but memory clock identical.

## Power Phases
| Phase | Power | Util | SM Clock | MEM Clock |
|---|---|---|---|---|
| Idle | 55W | 0% | 210MHz | 1593MHz |
| FP16 load | 405W | 100% | 1200MHz | 1593MHz |
| Post load | 86W | 0% | 1155MHz | 1593MHz |

## FP16 vs FP32 Comparison
| Precision | SM Clock | Power | MEM Clock |
|---|---|---|---|
| FP32 | 1410MHz | 399W | 1593MHz |
| FP16 | 1200MHz | 405W | 1593MHz |

## Files
- README.md — this file
- SUMMARY.md — test summary
- metrics.json — structured metrics
- evidence.json — evidence data
- raw_data.csv — raw telemetry

## Conclusion
Ghost power is memory-driven not precision-dependent.
HBM2e locked at 1593MHz regardless of compute precision.
