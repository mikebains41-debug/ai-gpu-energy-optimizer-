# A100 SXM Test 06 — Multi GPU Memory Clock Divergence
## Date: 2026-05-29
## Pod: c6432c0108d6 | Provider: RunPod
## Researcher: Manmohan (Mike) Bains

## Key Findings
- GPU0 consistently higher than GPU1 by 1.71W
- Both GPUs memory clock locked at 1593MHz
- Simultaneous spontaneous burst on BOTH GPUs
- Burst: GPU0 86.13W, GPU1 84.36W at 0% util
- SM clock jumped to 1140MHz on both during burst

## Architecture Comparison
| GPU | Higher GPU | Differential | Pattern |
|---|---|---|---|
| A100 SXM | GPU0 | 1.71W | GPU0 always higher |
| B200 | GPU1 | 1.65W | GPU1 always higher |

Hardware asymmetry confirmed on both architectures.
Direction differs but magnitude similar.
