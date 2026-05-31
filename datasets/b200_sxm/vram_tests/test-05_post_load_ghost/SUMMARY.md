# B200_VRAM_TEST_05_POST_LOAD_GHOST
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: GHOST POWER CRITICAL + NVML BLIND + RESIDUAL

| Phase | VRAM | GPU0 | GPU1 | Util |
|---|---|---|---|---|
| Baseline | 0 MB | 144.32W | 149.38W | 0 pct |
| After FP32 Exit | 728 MB | **549.84W** | **574.84W** | **0 pct** |
| Ghost Monitor 600s | 728 MB | 196-203W | 202-203W | 0 pct |

## Security Issue CRITICAL — Ghost Power Spike
549.84W GPU0 + 574.84W GPU1 at 0 pct util AFTER process exits.
Highest ghost power ever recorded across all 7 architectures tested.
- A100 max desync: 357W
- B200 ghost spike: **549-574W** (+217W above A100)

## Security Issue HIGH — NVML Blind
NVML reports 0 pct util throughout — even during 549W spike.
Conventional monitoring tools (DCGM, Prometheus, Datadog) cannot detect this.

## Security Issue HIGH — VRAM Residual
728 MB permanent. Survives 600 second monitoring window.

## Conclusion
B200 is the most dangerous architecture tested for ghost power and VRAM security.
NVML cannot monitor it. Power spikes to 549W at 0 pct reported util.
