# A100 SXM Test 05 — Post Load Ghost Power
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains

## Key Findings
- Post load power: 84-86W at 0% utilization
- SM clock: 1155MHz — elevated, did not return to 210MHz
- Memory clock: 1593MHz — locked as always
- No spontaneous burst detected this run
- Ghost power floor elevated vs cold boot baseline 65W

## Two Ghost Power States Identified
State 1 — Cold boot idle: 65W, SM 210MHz, MEM 1593MHz
State 2 — Post load ghost: 85W, SM 1155MHz, MEM 1593MHz

Both states: memory clock 1593MHz locked.
State 2 power is 30% higher than State 1.
SM clock remains elevated in State 2.
