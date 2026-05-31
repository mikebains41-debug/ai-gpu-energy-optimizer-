# A100 SXM 80GB — Complete Test Reports
**Date:** 2026-05-29 to 2026-05-31 | **Pod:** bbcd7cb43196 / ff9ab4afab02
**Researcher:** Manmohan (Mike) Bains | mikebains41@gmail.com

---

## VRAM Tests

| Test | ID | Result | VRAM Residual | Security |
|---|---|---|---|---|
| VRAM Baseline | test-01 | PASS | 0 MB | None |
| VRAM Workload | test-02 | RESIDUAL | **457 MB** | HIGH |
| VRAM Residual SIGKILL | test-03 | PASS | **0 MB** | None |
| VRAM Detailed FP32 | test-04 | RESIDUAL | **457 MB** | HIGH |
| VRAM Detailed FP16 | test-05 | RESIDUAL | **463 MB** | HIGH |
| VRAM Full Profile | test-06 | RESIDUAL + ASYMMETRIC | **465 MB** | HIGH |

## Memory Clock Tests

| Test | ID | Key Finding | Security |
|---|---|---|---|
| Idle Baseline | test-01 | MEM=1593MHz locked at 0MB VRAM | None |
| FP32 Load | test-02 | SM 210→1410MHz, MEM=1593 always | HIGH |
| FP16 Load | test-03 | SM 210→1155MHz, MEM=1593 always | HIGH |
| Cooldown | test-04 | SM stuck at 1155MHz post-load | HIGH |
| Post Load Ghost | test-05 | 416W peak, ghost state 2 confirmed 300s | HIGH |

---

## VRAM Residual Summary

| Test | Compute | Cleanup | Residual |
|---|---|---|---|
| TEST_03 | Any | SIGKILL | **0 MB** ✅ |
| TEST_02 | Workload | del+empty_cache | 457 MB ⚠️ |
| TEST_04 | FP32 | del+empty_cache | 457 MB ⚠️ |
| TEST_05 | FP16 | del+empty_cache | 463 MB ⚠️ |
| TEST_06 | FP32+FP16 | del+empty_cache | 465 MB ⚠️ |

**Pattern: More compute = more residual. SIGKILL = only safe method.**

---

## Security Findings

### 1. VRAM Data Persistence — HIGH
Every graceful PyTorch exit leaves 457-465 MB in VRAM uncleared.
On shared cloud GPU infrastructure, next tenant can read previous tenant data.
Affected data: model weights, intermediate tensors, FP32/FP16 computation results.

### 2. SIGKILL is Safer than Graceful Exit
OS kernel forces immediate VRAM reclaim and zeroing on hard kill.
PyTorch `del` + `empty_cache()` does NOT fully clear VRAM.

### 3. Ghost Power State 2 — SM Clock Stuck
After any workload, SM clock does not return to 210 MHz idle.
Stuck at 1155 MHz. Power elevated from 65W to 86W indefinitely.

### 4. HBM Memory Clock Locked 24/7
MEM clock = 1593 MHz across all phases — idle, load, compute, cooldown.
Never changes. Root cause of ghost power.

### 5. Asymmetric GPU Load (TEST_06)
FP32 compute ran entirely on GPU0 (356W, 100%).
GPU1 at 7.48W — not participating in compute.

---

## Ghost Power States

| State | Trigger | SM Clock | MEM Clock | Power |
|---|---|---|---|---|
| State 1 | Cold boot | 210 MHz | 1593 MHz | 65W |
| State 2 | Post-load | 1155 MHz | 1593 MHz | 86W |

---

## Live Endpoints
- https://ai-gpu-brain-v3.onrender.com
- https://ai-gpu-energy-optimizer.vercel.app
