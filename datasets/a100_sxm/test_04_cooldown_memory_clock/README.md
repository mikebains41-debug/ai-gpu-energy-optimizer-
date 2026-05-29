# A100 SXM Test 04 — Cooldown Memory Clock
## Test ID: A100_TEST_04_COOLDOWN_MEMORY_CLOCK
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains | mikebains41@gmail.com

## Finding
Memory clock locked at 1593MHz throughout entire cooldown period.
SM clock and power recover quickly. Memory never changes.

## Cooldown Profile
| Metric | Post Load | Recovered |
|---|---|---|
| Power | 86W | 65W |
| SM Clock | 1155MHz | 210MHz |
| MEM Clock | 1593MHz | 1593MHz |
| Utilization | 0% | 0% |

## Files
- README.md — this file
- SUMMARY.md — test summary
- metrics.json — structured metrics
- evidence.json — evidence data
- raw_data.csv — raw telemetry

## Conclusion
Memory subsystem does not participate in cooldown.
Ghost power floor 65W is permanent at idle.
HBM2e locked at 1593MHz regardless of thermal state.
