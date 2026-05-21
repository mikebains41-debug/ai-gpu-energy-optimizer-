#!/usr/bin/env python3
import subprocess, json, datetime, os, sys

TESTS = [
    ("M1",  "M1_pipeline_connect.py",           "Pipeline Connect"),
    ("M2",  "M2_ghost_detection.py",            "Ghost Detection"),
    ("M3",  "M3_desync_detection.py",           "DESYNC Detection"),
    ("M4",  "M4_cei_scoring.py",                "CEI Scoring"),
    ("M5",  "M5_auto_alert.py",                 "Auto Alert"),
    ("M6",  "M6_sustained_run.py",              "Sustained Run"),
    ("M7",  "M7_fp16_cei.py",                   "FP16 CEI Score"),
    ("M8",  "M8_2gpu_simultaneous.py",          "2 GPU Simultaneous"),
    ("M9",  "M9_2gpu_load.py",                  "2 GPU Load Test"),
    ("M10", "M10_ghost_both_gpus.py",           "Ghost Both GPUs"),
    ("M11", "M11_mixed_workload.py",            "Mixed Workload"),
    ("M12", "M12_batch_ingestion.py",           "Batch Ingestion"),
    ("M13", "M13_1000gpu_simulation.py",        "1000 GPU Simulation"),
    ("M14", "M14_agent_crash.py",               "Agent Crash Recovery"),
    ("M15", "M15_network_dropout.py",           "Network Dropout"),
    ("M16", "M16_api_restart.py",               "API Restart"),
    ("M17", "M17_redis_crash.py",               "Redis Crash"),
    ("M18", "M18_24hr_simulation.py",           "24hr Simulation"),
    ("M19", "M19_ghost_accuracy.py",            "Ghost Accuracy"),
    ("M20", "M20_cei_accuracy.py",              "CEI Accuracy"),
    ("M21", "M21_false_positive.py",            "False Positive Rate"),
    ("M22", "test_m22_alert_latency.py",        "Alert Latency"),
    ("M23", "test_m23_api_key_auth.py",         "API Key Auth"),
    ("M24", "test_m24_rate_limiting.py",        "Rate Limiting"),
    ("M25", "test_m25_node_isolation.py",       "Node Isolation"),
    ("M26", "test_m26_prometheus_scrape.py",    "Prometheus Scrape"),
    ("M27", "test_m27_grafana_dashboard.py",    "Grafana Dashboard"),
    ("M28", "test_m28_kubernetes_daemonset.py", "Kubernetes DaemonSet"),
    ("M29", "test_m29_helm_install.py",         "Helm Install"),
    ("M30", "test_m30_end_to_end.py",           "End to End"),
]

def run_test(test_id, filename, name):
    print(f"\n{'='*55}")
    print(f"  RUNNING {test_id}: {name}")
    print(f"{'='*55}")
    start = datetime.datetime.utcnow()
    try:
        result = subprocess.run(
            [sys.executable, f"morpheus/tests/{filename}"],
            capture_output=True, text=True, timeout=3600
        )
        passed = result.returncode == 0
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        passed = False
        output = "TIMEOUT"
    except Exception as e:
        passed = False
        output = str(e)
    duration = (datetime.datetime.utcnow() - start).seconds
    status = "PASS" if passed else "FAIL"
    print(f"  {test_id}: {status} ({duration}s)")
    if not passed:
        print(f"  OUTPUT: {output[-500:]}")
    return {"test_id": test_id, "name": name, "status": status, "duration": duration}

def main():
    print("\n" + "="*55)
    print("  AI GPU ENERGY OPTIMIZER")
    print("  ENTERPRISE TEST SUITE 30 TESTS")
    print("  2x A100 SXM | Manmohan Bains")
    print("="*55)
    results = []
    for test_id, filename, name in TESTS:
        result = run_test(test_id, filename, name)
        results.append(result)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    report = {"timestamp": timestamp, "total": 30, "passed": passed, "failed": failed, "results": results}
    os.makedirs("morpheus/tests/results", exist_ok=True)
    report_file = f"morpheus/tests/results/enterprise_report_{timestamp[:10]}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    print("\n" + "="*55)
    print("  ENTERPRISE TEST RESULTS")
    print("="*55)
    for r in results:
        print(f"  {r['test_id']:<4} {r['name']:<25} {r['status']}")
    print("="*55)
    print(f"  PASSED: {passed}/30")
    print(f"  FAILED: {failed}/30")
    print(f"  STATUS: {'ENTERPRISE GRADE CERTIFIED' if passed==30 else 'NEEDS ATTENTION'}")
    print(f"  REPORT: {report_file}")
    print("="*55)

if __name__ == "__main__":
    main()
