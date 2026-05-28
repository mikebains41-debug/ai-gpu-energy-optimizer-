# B200 Test 01 — Executive Summary

## One Line Finding
B200 draws 143-145W at 0% utilization from cold boot with zero processes.

## What Was Tested
Fresh B200 pod on RunPod. No workloads. No processes. Just boot and measure.

## What Was Found
- GPU 0: 143.23W at 0% util
- GPU 1: 145.08W at 0% util
- Both GPUs: P0 state locked
- Memory clock: 3996 MHz at idle
- Duration confirmed: 3 minutes 10 seconds sustained
- No variation. No recovery. Flat line at 143-145W.

## Why This Matters
A100 SXM ghost power appeared AFTER a workload ran.
B200 ghost power is present FROM BOOT with zero workload ever run.
B200 idles at more than double the A100 SXM idle floor.

## Comparison
| GPU | Idle Floor |
|---|---|
| A100 SXM | 67.1W |
| H100 SXM | 69.5W |
| B200 | 143-145W |

## Financial Impact
Single B200: $125/year wasted on ghost power
1000 B200s: $125,300/year wasted
100,000 B200s: $12,530,000/year wasted

## Status
CONFIRMED. Not a transient. Not a boot artifact.
This is the B200 idle floor.

## Date
2026-05-28 17:18 UTC
