# A100 Test 01 — Memory Clock Idle
**Researcher:** Manmohan (Mike) Bains | mikebains41@gmail.com
**Provider:** RunPod | **Pod:** bbcd7cb43196

## Key Numbers
- Ghost power GPU0 = 65.14W | GPU1 = 67.52W
- GPU1 consistently 2-3W higher than GPU0
- HBM clock locked = 1,593MHz both GPUs throughout
- SM clock = 210MHz baseline
- VRAM = 0 MB
- util.gpu = 0% throughout
- P-state = P0 locked
- Duration = 23 minutes
- Samples = ~276 both GPUs

## Spontaneous Burst
- Timestamp = 2026-05-30 22:30:05
- GPU1 power = 107.84W
- GPU1 SM clock = 1,350MHz
- HBM = 1,593MHz unchanged
- GPU0 unaffected
- util.gpu = 0% (NVML blind)

## Security Finding
Autonomous GPU activity at 0pct utilization — NVML completely blind — potential undisclosed GPU microcode execution.

## Cross-Architecture Correlation
A100 HBM 1593MHz = 65W ghost power
B200 HBM 3996MHz = 144W ghost power
Ratio 2.51x memory clock = 2.21x power — confirmed.
