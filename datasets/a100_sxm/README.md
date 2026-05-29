# A100 SXM Dataset — NVIDIA Ampere

## Status
24 validated hardware tests
Provider: RunPod | Pod: env@4a081da99c4d

## Key Findings
| Metric | Value |
|---|---|
| Ghost power | 146.66W at 0% utilization |
| Idle floor | 67.1W |
| CEI reported | 5.68B FLOPs/joule |
| CEI true | 4.12B FLOPs/joule |
| CEI degradation | 27.5% worse than reported |
| FP16 average | 482.7W |
| FP32 average | 302W |
| Severe desync | 357W event documented |
| P0 lock | Confirmed post-load |
| Hypervisor | Blocks remediation |

## Note
A100 SXM tests pending restructure into 5-file format.
B200 SXM tests are the reference format.
See datasets/B200_SXM for complete 5-file structure.

## Researcher
Manmohan (Mike) Bains
mikebains41@gmail.com
2026-05-28
