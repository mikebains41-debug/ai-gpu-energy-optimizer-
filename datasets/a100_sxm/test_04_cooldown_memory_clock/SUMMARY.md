# A100 SXM Test 04 — Cooldown Memory Clock
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains

## Key Findings
- SM clock recovered to 210MHz immediately after workload
- Power recovered to 64-65W baseline
- Memory clock: 1593MHz — never moved throughout cooldown
- Cooldown is fast — SM clock drops within first sample

## Critical Finding
Memory clock remains locked at 1593MHz even during cooldown.
No cooldown period affects memory subsystem.
Ghost power floor 64-65W maintained indefinitely.
