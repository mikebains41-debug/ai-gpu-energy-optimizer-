# CLAUDE.md — AI GPU Energy Optimizer

## Project Overview
AI + GPU Energy Optimization Platform. Real-time dashboard for 
data center GPU workloads, power efficiency, heat reuse, and 
AI-driven energy scheduling.

## Engineering Principles

### Plan First
- For any non-trivial change, outline affected files before editing
- Understand the test structure before modifying benchmarks
- Never touch core CEI calculations without a clear plan

### Surgical Edits Only
- Change only what is necessary
- Do not refactor unrelated code
- Keep pull requests small and focused

### Verify Always
- Run existing tests after every change
- 18/18 tests must pass before any commit
- Never weaken a test to make it pass

### Keep It Simple
- Prefer 100 lines over 1000
- No speculative abstractions
- No unnecessary dependencies

## Project Structure
- `/data` — benchmark results (A100, H100, T4, A40, RTX 4090)
- `/K8s` — Helm charts for 1000-GPU DaemonSet
- `/slurm` — HPC cluster configs
- `/components` — dashboard UI
- `WHITEPAPER.md` — full research findings

## What Lives Here
Public benchmark data, dashboard, and architecture only.
Core engine and telemetry pipeline are proprietary.

## Contact
mikebains41@gmail.com
