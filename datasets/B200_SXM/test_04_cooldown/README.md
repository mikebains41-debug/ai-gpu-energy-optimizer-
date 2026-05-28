# B200 2x GPU Test 04 — Cooldown Profile
## Status: COMPLETE — NO COOLDOWN PERIOD — PERIODIC SPIKES CONFIRMED

---

## Hardware Configuration
| Field | Value |
|---|---|
| GPU Model | NVIDIA B200 |
| GPU Count | 2x |
| Total VRAM | 360GB |
| VRAM Per GPU | 180GB |
| Driver Version | 580.126.20 |
| CUDA Version | 13.0 |
| PyTorch Version | 2.11.0+cu128 |
| Power Limit Per GPU | 1000W |
| Combined Power Limit | 2000W |
| Pod ID | aee29124a02b |
| Provider | RunPod |
| Test Date | 2026-05-28 |

---

## Test Configuration
| Field | Value |
|---|---|
| Test Type | Post-load cooldown monitoring |
| Previous Test | Test 03 FP16 Tensor Core Load |
| Previous Test End Power | 195-202W |
| Start Time | 2026/05/28 20:05:27 UTC |
| End Time | 2026/05/28 20:14:19 UTC |
| Duration | 8 minutes 52 seconds |
| Samples Per GPU | 54 |
| Sampling Interval | 10 seconds |

---

## GPU 0 Cooldown Results
| Metric | Value |
|---|---|
| Baseline Power | 143.83 - 144.18W |
| Spike Power | 146.05 - 146.63W |
| Utilization | 0% |
| SM Clock | 120 MHz |
| Temperature | 30-31C |
| P-State | P0 |

---

## GPU 1 Cooldown Results
| Metric | Value |
|---|---|
| Baseline Power | 145.53 - 146.05W |
| Spike Power | 147.79 - 148.54W |
| Utilization | 0% |
| SM Clock | 120 MHz |
| Temperature | 31-32C |
| P-State | P0 |

---

## Periodic Spike Pattern
| Timestamp | GPU 0 W | GPU 1 W | Spike |
|---|---|---|---|
| 20:10:18 | 146.63 | 148.36 | YES |
| 20:10:48 | 146.58 | 148.42 | YES |
| 20:11:18 | 146.38 | 147.91 | YES |
| 20:11:48 | 146.05 | 147.79 | YES |
| 20:12:18 | 146.17 | 148.04 | YES |
| 20:12:48 | 146.31 | 148.09 | YES |
| 20:13:18 | 146.63 | 148.54 | YES |
| 20:13:49 | 146.50 | 148.15 | YES |
| 20:14:19 | 146.57 | 148.31 | YES |

---

## Key Findings

### FINDING 1 — No Cooldown Period
Power returned to baseline immediately after FP16 load.
First reading at 20:05:27 already at 144W baseline.
No gradual decay observed.
Instant transition from 195-202W load to 143-145W idle.

### FINDING 2 — Periodic Power Spikes
Spikes occur every approximately 30 seconds.
GPU 0 spikes: 146-147W from 144W baseline.
GPU 1 spikes: 147-149W from 145W baseline.
Both GPUs spike simultaneously.
Cause unknown — possibly GPU management background activity.

### FINDING 3 — Ghost Power Floor Maintained
143-145W ghost power floor persists in cooldown.
Identical to cold boot baseline from Test 01.
Ghost power is permanent baseline state on B200.

### FINDING 4 — SM Clock Recovery
SM clock returned to 120 MHz immediately from 1965 MHz.
Unlike P0 state which remained locked.
Clock recovers but power state does not.

---

## Evidence Files
| File | Description |
|---|---|
| b200_test04_cooldown_raw_data.csv | Raw nvidia-smi readings |
| metrics.json | Structured key metrics |
| evidence.json | Full evidence chain |
| SUMMARY.md | Executive summary |
| README.md | This document |
| Screenshots | Raw terminal output images |

---

## Conclusion
B200 exhibits no cooldown period after compute load.
Power returns instantly to 143-145W ghost power floor.
Periodic power spikes of 2-3W occur every 30 seconds
at 0% utilization — cause undetermined.
Ghost power floor is permanent and load-independent on B200.

---

## Next Test
Test 05 — Post Load Ghost Power Comparison

---

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
Duncan BC Canada
2026-05-28

## Project
GPU Energy Optimizer v2.0
https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
