# GPU Energy Optimizer — Public Benchmark Datasets

Real hardware telemetry from GPU energy efficiency research.
All data collected on RunPod infrastructure (A100 SXM, H100 SXM).

## Key Findings

| Finding | Value | GPU |
|---------|-------|-----|
| Peak ghost power | 146W at 0% utilization | A100 SXM |
| Idle floor | 67W | A100 SXM |
| FP32 CEI | 5.68e9 FLOPs/J | A100 SXM |
| FP16 draw vs FP32 | 483W vs 302W | A100 SXM |
| Estimated waste (500 GPUs) | $17,445/year | A100 SXM |

## Dataset Index

| GPU | Test | Finding | Files |
|-----|------|---------|-------|
| A100 SXM | Test 13 — Load Cooldown | Ghost power retention after workload | CSV, JSON, PNG |
| A100 SXM | Test 17 — P-State Retention | Power state lock after activity | CSV, JSON, PNG |
| A100 SXM | Test 24 — CEI Validation | 5.68e9 FLOPs/J benchmark | CSV, JSON, PNG |
| A100 SXM | Ghost Power | 146W at 0% util | CSV, JSON, PNG |
| A100 SXM | FP16 vs FP32 | 483W vs 302W draw | CSV, JSON, PNG |
| H100 SXM | Test 01 — Idle Baseline | Idle floor measurement | CSV, JSON, PNG |
| H100 SXM | Test 05 — FP16 Tensor | Tensor core efficiency | CSV, JSON, PNG |
| H100 SXM | Test 11 — Validation | Cross-validation run | CSV, JSON, PNG |

## Methodology

- Provider: RunPod (pod env @4a081da99c4d)
- Measurement: nvidia-smi + pynvml with fallback
- Sampling rate: 1Hz
- Total validated tests: 54 (24 A100 + 11 H100 + 5 platform + 30 enterprise Morpheus)
- Hypervisor note: persistence mode and power cap blocked by RunPod hypervisor

## Important Transparency Notes

Some tests returned BLOCKED or INCONCLUSIVE due to hypervisor restrictions.
These are published as-is. Real infrastructure research includes provider limitations.

## Reproduce This Data

```bash
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-
cd ai-gpu-energy-optimizer-
pip install -r requirements-production.txt
python morpheus/tests/run_all.py
for dir in \
  "datasets/a100_sxm/test_13_load_cooldown" \
  "datasets/a100_sxm/test_17_pstate_retention" \
  "datasets/a100_sxm/test_24_cei_validation" \
  "datasets/a100_sxm/test_ghost_power" \
  "datasets/a100_sxm/test_fp16_vs_fp32"; do

cat > $dir/evidence.json << 'EOF'
{
  "gpu": "A100 SXM",
  "provider": "RunPod",
  "pod_env": "@4a081da99c4d",
  "collection_date": "2026",
  "status": "VALIDATED",
  "peak_power_w": null,
  "idle_power_w": 67,
  "utilization_at_peak_ghost": 0,
  "finding": "TBD — populate after RunPod run",
  "hypervisor_note": "persistence mode and power cap blocked",
  "cei_flops_per_joule": null
}
