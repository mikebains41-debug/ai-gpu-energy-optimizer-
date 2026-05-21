#!/usr/bin/env python3
"""
Auto-populates dataset CSVs from run_all.py results.
Run this after RunPod completes.
"""
import json, os, glob, csv
from datetime import datetime

RESULTS_DIR = "morpheus/tests/results"
DATASETS_DIR = "datasets"

TEST_TO_DATASET = {
    "M1":  None,
    "M2":  "a100_sxm/test_ghost_power",
    "M3":  None,
    "M4":  "a100_sxm/test_24_cei_validation",
    "M5":  None,
    "M6":  "a100_sxm/test_13_load_cooldown",
    "M7":  "a100_sxm/test_fp16_vs_fp32",
    "M13": None,
    "M19": "a100_sxm/test_ghost_power",
    "M20": "a100_sxm/test_24_cei_validation",
}

def load_latest_report():
    reports = glob.glob(f"{RESULTS_DIR}/enterprise_report_*.json")
    if not reports:
        print("No report found. Run morpheus/tests/run_all.py first.")
        return None
    latest = sorted(reports)[-1]
    print(f"Loading: {latest}")
    with open(latest) as f:
        return json.load(f)

def load_individual_results():
    results = {}
    for f in glob.glob(f"{RESULTS_DIR}/*.json"):
        if "enterprise_report" in f:
            continue
        try:
            with open(f) as fh:
                data = json.load(fh)
                tid = data.get("test_id") or data.get("name", "")
                results[tid] = data
        except:
            pass
    return results

def update_evidence(dataset_path, test_data):
    evidence_file = os.path.join(DATASETS_DIR, dataset_path, "evidence.json")
    if not os.path.exists(evidence_file):
        return
    with open(evidence_file) as f:
        evidence = json.load(f)
    evidence["status"] = "VALIDATED"
    evidence["run_date"] = datetime.utcnow().isoformat()
    evidence["test_status"] = test_data.get("status")
    evidence["duration_sec"] = test_data.get("duration")
    data = test_data.get("data", {})
    if data:
        evidence.update({k: v for k, v in data.items() if v is not None})
    with open(evidence_file, "w") as f:
        json.dump(evidence, f, indent=2)
    print(f"  Updated: {evidence_file}")

def write_summary(dataset_path, test_data):
    summary_file = os.path.join(DATASETS_DIR, dataset_path, "summary.md")
    status = test_data.get("status", "UNKNOWN")
    duration = test_data.get("duration", 0)
    name = test_data.get("name", "")
    content = f"""# Test Summary — {name}

## Status: {status}

## Duration
{duration} seconds

## Run Date
{datetime.utcnow().strftime("%Y-%m-%d")}

## Hardware
- GPU: NVIDIA A100 SXM
- Provider: RunPod
- Pod: 2x A100

## Key Findings
See evidence.json for full data.

## Caveats
- Hypervisor blocked persistence mode
- Power cap commands rejected by RunPod
"""
    with open(summary_file, "w") as f:
        f.write(content)
    print(f"  Updated: {summary_file}")

def write_csv(dataset_path, test_data):
    csv_file = os.path.join(DATASETS_DIR, dataset_path, "raw_metrics.csv")
    data = test_data.get("data", {})
    readings = data.get("readings", [])
    if not readings:
        return
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "power_w", "util_gpu", "temperature_c", "clock_mhz", "pstate"])
        for i, r in enumerate(readings):
            if isinstance(r, dict):
                writer.writerow([i, r.get("power_draw_w",""), r.get("utilization_pct",""),
                                 r.get("temp_c",""), r.get("clock_mhz",""), r.get("pstate","")])
            else:
                writer.writerow([i, r, "", "", "", ""])
    print(f"  CSV written: {csv_file}")

def main():
    print("GPU Energy Optimizer — Dataset Populator")
    print("="*50)

    report = load_latest_report()
    individual = load_individual_results()

    if report:
        print(f"\nReport: {report['passed']}/30 passed\n")

    for test_id, dataset_path in TEST_TO_DATASET.items():
        if not dataset_path:
            continue
        test_data = individual.get(test_id) or {}
        if not test_data and report:
            for r in report.get("results", []):
                if r["test_id"] == test_id:
                    test_data = r
                    break
        if not test_data:
            print(f"  No data for {test_id} — skipping")
            continue
        print(f"\nPopulating {test_id} → {dataset_path}")
        full_path = os.path.join(DATASETS_DIR, dataset_path)
        os.makedirs(full_path, exist_ok=True)
        update_evidence(dataset_path, test_data)
        write_summary(dataset_path, test_data)
        write_csv(dataset_path, test_data)

    print("\n" + "="*50)
    print("Done. Run datasets/scripts/generate_charts.py next.")

if __name__ == "__main__":
    main()
