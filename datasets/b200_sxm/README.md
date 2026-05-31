# B200 SXM — VRAM Test Reports
**Date:** 2026-05-30 | **Pod:** f8982abf565d
**GPU:** B200 SXM x2 | **VRAM per GPU:** 183,359 MB

## Test Results
| Test | Result | Residual | Security |
|---|---|---|---|
| test-01 baseline | RESIDUAL | **628 MB** | HIGH x2 |
| test-02 FP32 load | RESIDUAL + ANOMALOUS | **728 MB** | HIGH x2 |
| test-03 FP16 load | RESIDUAL | **726 MB** | HIGH |
| test-04 cooldown | POWER STUCK | **728 MB** | HIGH x2 |
| test-05 ghost | CRITICAL GHOST + NVML BLIND | **728 MB** | CRITICAL + HIGH x2 |
| test-06 full profile | RESIDUAL + STUCK + BLIND | **728 MB** | HIGH x3 |

## Cross-Architecture Residual
| GPU | HBM | Residual |
|---|---|---|
| A100 SXM | HBM2e | 457-465 MB |
| H200 SXM | HBM3e | 529-629 MB |
| B200 SXM | HBM3e | **628-728 MB** |

## B200 Unique Security Findings
1. CRITICAL: Ghost spike 549.84W GPU0 + 574.84W GPU1 at 0 pct util after process exits
2. HIGH: NVML completely blind — DCGM Datadog Prometheus all cannot monitor B200
3. HIGH: Power never returns to baseline — permanently +52W elevated after any workload
4. HIGH: 728 MB fixed residual — does not vary with compute precision type
5. HIGH: Anomalous cooldown spike 684-700W at 45-48 pct util during cooldown phase
6. HIGH: B200 has no recovery state — unlike A100 which has State 1 and State 2

## Ghost Power Comparison
| GPU | Max Ghost Power |
|---|---|
| A100 SXM | 357W |
| H200 SXM | 136W post-load |
| B200 SXM | **549-574W** |

## NVML Blind Issue
NVML utility.gpu = 0 pct throughout B200 tests.
Makes conventional GPU monitoring completely ineffective on B200 architecture.

## Live Endpoints
- https://ai-gpu-brain-v3.onrender.com
- https://ai-gpu-energy-optimizer.vercel.app
