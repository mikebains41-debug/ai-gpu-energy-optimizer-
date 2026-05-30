# A100 SXM Memory Clock Test — New Finding
## Date: 2026-05-29
## Pod: 827710d5583c | Provider: RunPod
## Researcher: Manmohan (Mike) Bains

## Key Finding: Memory-Driven Ghost Power Confirmed

HBM2e memory subsystem locked at 1593MHz while compute is idle.
SM clock at 210MHz. Memory clock ratio: 7.6x higher than compute.

## Spontaneous Burst Event Captured
- Time: 2026/05/29 17:45:08
- Power jumped: 65W → 73.07W
- SM clock jumped: 210MHz → 720MHz
- Memory clock: 1593MHz — unchanged
- Utilization: 0% throughout

## Architecture Comparison
| GPU | SM Clock | MEM Clock | Ratio | Ghost Power |
|---|---|---|---|---|
| A100 SXM | 210 MHz | 1593 MHz | 7.6x | YES |
| B200 | 120 MHz | 3996 MHz | 33.3x | YES |

B200 memory clock is 2.5x higher than A100.
B200 ghost power is 2.2x higher than A100.
Memory clock magnitude correlates directly with ghost power magnitude.

## Conclusion
Ghost power is memory-driven. HBM subsystem does not
clock down at idle. This is architectural and cannot be
remediated without hardware redesign.
