# A100 SXM Test 03 — FP16 Load Memory Clock
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains

## Key Findings
- FP16 load power: 386-408W at 100% utilization
- SM clock under FP16: 1185-1215MHz
- SM clock under FP32: 1410MHz — FP16 runs at lower SM clock
- Memory clock: 1593MHz — NEVER MOVED
- Post load power: 86-89W at 0% util
- Memory clock post load: 1593MHz — still locked

## Critical Finding
Memory clock 1593MHz unchanged across ALL states including FP16 load.
FP16 SM clock lower than FP32 but memory clock identical.
Ghost power is memory-driven not precision-dependent.
