# A100 SXM Test 05 — Post Load Ghost Power
## Test ID: A100_TEST_05_POST_LOAD_GHOST
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains | mikebains41@gmail.com

## Finding
Two distinct ghost power states identified.
Memory clock locked at 1593MHz in both states.

## Ghost Power States
| State | Power | SM Clock | MEM Clock | Trigger |
|---|---|---|---|---|
| Cold boot idle | 65W | 210MHz | 1593MHz | Power on |
| Post load ghost | 85W | 1155MHz | 1593MHz | After workload |

## Files
- README.md — this file
- SUMMARY.md — test summary
- metrics.json — structured metrics
- evidence.json — evidence data
- raw_data.csv — raw telemetry

## Conclusion
Post load ghost power 30% higher than cold boot baseline.
SM clock elevation persists after workload.
Memory clock permanently locked regardless of state.
