# A100 Test 02 — FP32 Memory Clock
**Date:** 2026-05-30 | **GPU:** A100 SXM x2 | **Pod:** bbcd7cb43196

## Result: CRITICAL

| Phase | GPU0 | GPU1 | SM MHz | HBM MHz | util |
|---|---|---|---|---|---|
| Baseline | 65.07W | 67.19W | 210 | 1,593 | 0% |
| FP32 Peak | 360.64W | 360.91W | 1,410 | 1,593 | 100% |

## Key Finding
HBM clock locked at 1,593MHz throughout — never changes even at 100% FP32 load.
Ghost power is memory-driven not compute-driven.

## vs Old Test
Old: single GPU 399W | New: 2x GPU 360W each
