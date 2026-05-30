# B200 Test 06 — Multi GPU Divergence
**Date:** 2026-05-30 | **GPU:** B200 SXM x2 | **Pod:** f8982abf565d

## Result: CRITICAL

| Phase | GPU0 | GPU1 |
|---|---|---|
| Baseline | 144.51W | 149.64W |
| GPU0 Only Peak | 457.17W | 148.85W |
| GPU1 Only Peak | 196.76W | 455.33W |
| Both GPU Peak | 462.45W | 436.74W |
| Post Load | 196.79W | 202.53W |

## Key Finding
GPU0 draws 26W more than GPU1 under dual load.
GPU1 draws 5W more than GPU0 at baseline.
