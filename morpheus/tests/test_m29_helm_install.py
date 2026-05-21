"""M29 - Helm Install"""
import os
from datetime import datetime
from utils import log_result

TEST_ID = "M29"
TEST_NAME = "Helm Install"
REQUIRED_FILES = [
    "K8s/helm/Chart.yaml",
    "K8s/helm/values.yaml",
    "K8s/helm/templates/daemonset.yaml"
]

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    passed = True
    checks = []
    base_paths = ["", "../../", "../../../"]
    for req in REQUIRED_FILES:
        found = False
        for base in base_paths:
            if os.path.exists(base + req):
                found = True
                break
        checks.append({"file": req, "found": found})
        print(f"  {'FOUND' if found else 'MISSING'}: {req}")
        if not found:
            passed = False
    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "helm_files": checks, "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] Helm install")
    return result

if __name__ == "__main__":
    run()
