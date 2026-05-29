# A100 SXM Test 02 — FP32 Load Memory Clock
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains

## Key Findings
- FP32 load power: 371-399W at 100% utilization
- SM clock under load: 1410MHz
- Memory clock under load: 1593MHz — UNCHANGED
- Post load power: 85-90W at 0% util
- Post load SM clock: 1155MHz — elevated
- Post load memory clock: 1593MHz — UNCHANGED

## Critical Finding
Memory clock locked at 1593MHz across ALL states:
- Idle: 1593MHz
- FP32 load: 1593MHz  
- Post load cooldown: 1593MHz

Memory subsystem completely decoupled from workload.
Ghost power is memory-driven and architectural.
