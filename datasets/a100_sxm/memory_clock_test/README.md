# A100 SXM Memory Clock Test — New Finding
## Test ID: A100_MEMORY_CLOCK_TEST
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains | mikebains41@gmail.com

## Finding
HBM2e memory subsystem locked at 1593MHz while compute idle at 210MHz.
Memory clock 7.6x higher than compute clock at 0% utilization.
Ghost power is memory-driven not compute-driven.

## Spontaneous Burst
- 17:45:08 — power 65W → 73W, SM 210MHz → 720MHz
- Memory clock unchanged at 1593MHz
- Utilization 0% throughout
- No workload running

## Architecture Comparison
| GPU | MEM Clock | SM Clock | Ratio | Ghost Power |
|---|---|---|---|---|
| A100 SXM | 1593 MHz | 210 MHz | 7.6x | 65W |
| B200 | 3996 MHz | 120 MHz | 33.3x | 143W |

Memory clock 2.5x higher on B200 = ghost power 2.2x higher.
Direct correlation confirmed.

## Files
- README.md — this file
- SUMMARY.md — test summary
- metrics.json — structured metrics
- evidence.json — evidence data
- a100_memory_clock_idle.csv — raw telemetry 138 samples

## Conclusion
Ghost power is architectural. HBM memory subsystem does not
clock down at idle. Cannot be remediated without hardware redesign.
