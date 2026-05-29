# A100 SXM Test 02 — FP32 Load Memory Clock
## Test ID: A100_TEST_02_FP32_MEMORY_CLOCK
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains | mikebains41@gmail.com

## Finding
Memory clock locked at 1593MHz regardless of workload state.
SM clock scales normally. Memory clock does not move.

## Power Phases
| Phase | Power | Util | SM Clock | MEM Clock |
|---|---|---|---|---|
| Idle | 65W | 0% | 210MHz | 1593MHz |
| FP32 load | 399W | 100% | 1410MHz | 1593MHz |
| Post load | 86W | 0% | 1155MHz | 1593MHz |

## Files
- README.md — this file
- SUMMARY.md — test summary
- metrics.json — structured metrics
- evidence.json — evidence data
- raw data captured via screenshots

## Conclusion
HBM2e memory subsystem decoupled from compute workload.
Memory clock architectural lockup confirmed.
Ghost power is memory-driven.
