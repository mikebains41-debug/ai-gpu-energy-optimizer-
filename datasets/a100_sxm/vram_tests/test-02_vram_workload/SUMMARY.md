# Test 26 — VRAM Workload
**Date:** 2026-05-29 | **GPU:** A100 SXM x2 | **Pod:** ff9ab4afab02

## Result: PASS

## Key Finding — VRAM Memory Utilization Desync
NVML reports 0% memory utilization while 807MB VRAM is loaded.
Same NVML lie as compute utilization vs power.

## VRAM States
| Phase | memory.used | util.memory | Power |
|---|---|---|---|
| Idle | 0 MB | 0% | 65.84W |
| Workload | 807 MB | 0% | 85.99W |
| Post exit | 0 MB | 0% | 65.84W |

## Findings
1. VRAM desync confirmed — 807MB used, 0% reported
2. VRAM clears immediately after process exits
3. Ghost power unchanged by VRAM state
4. No VRAM residual — clean memory handoff

## Conclusion
NVML lies about memory utilization. VRAM clears cleanly.
