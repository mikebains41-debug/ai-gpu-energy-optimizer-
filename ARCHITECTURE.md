# System Architecture
## GPU Optimizer Inc.
## Author: Manmohan (Mike) Bains
## Date: 2026-07-09

---

## Overview

GPU Optimizer is a software-only detection layer that identifies hardware-level
power anomalies ("ghost power") and VRAM security vulnerabilities on NVIDIA
data center GPUs. It does not build or require any proprietary hardware,
custom silicon, or embedded systems. See CEI_SPECIFICATION.md for the
measurement methodology and WHITEPAPER.md for full validated findings.

---

## System Flow

GPU Agent -> FastAPI Backend -> SQLite/PostgreSQL -> Dashboard & Alerts

- **GPU Agent**: polls NVIDIA GPU telemetry via nvidia-smi/NVML subprocess
  calls (power draw, utilization, memory state, clock speeds). Runs on the
  same host as the monitored GPU.
- **FastAPI Backend**: receives agent telemetry, cross-validates power/memory
  state against reported NVML utilization, classifies anomalies (ghost power,
  VRAM residual, telemetry desync).
- **Storage**: SQLite for local/single-node deployments, PostgreSQL/TimescaleDB
  for fleet-scale time-series telemetry.
- **Dashboard & Alerts**: Grafana/Prometheus-compatible metrics export;
  live API docs at ai-gpu-brain-v3.onrender.com/docs.

---

## Data Boundaries

- Telemetry data collected: GPU power draw, utilization percentage, memory
  usage, clock speeds, temperature. No workload contents, no customer data,
  no PII is collected by the agent.
- Data in transit: agent-to-backend communication over HTTPS.
- Data at rest: telemetry stored in SQLite/PostgreSQL; no secrets or
  credentials stored in telemetry tables.

---

## Security Controls

- API key generation uses cryptographically secure randomness
  (Node.js crypto.randomBytes), not Math.random().
- Automated dependency vulnerability scanning (GitHub Dependabot) and
  static code analysis (CodeQL) run continuously on the public codebase.
- Secret scanning and push protection enabled on the public repository.
- See SECURITY.md for current compliance status (SOC2 Type II and
  ISO 27001 certification in progress, not yet complete).

---

## Validated Test Architectures

Detection methodology validated across 7 NVIDIA GPU architectures:
A100 SXM, H100 SXM, H200 SXM, B200 SXM, B300 SXM6, plus PCIe/GDDR
controls (A100 PCIe, T4, RTX 4090) confirming the ghost power/VRAM
residual pattern is specific to SXM/HBM hardware.

Independent third-party validation conducted by Serial Alice/Sirius
GreenTech via Intel TDX confidential-computing hardware; results
cryptographically signed and blockchain-anchored on Polygon.
Full certificate list: WHITEPAPER.md.

---

## References

- CEI methodology: CEI_SPECIFICATION.md
- Full validated findings: WHITEPAPER.md
- Security status: SECURITY.md
- Live API: https://ai-gpu-brain-v3.onrender.com/docs
- Public repository: https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
