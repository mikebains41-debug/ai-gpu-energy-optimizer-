"""M28 - Kubernetes DaemonSet"""
import os
from datetime import datetime
from utils import log_result

TEST_ID = "M28"
TEST_NAME = "Kubernetes DaemonSet"
REQUIRED = ["kind: DaemonSet","nvidia.com/gpu","gpu-energy-agent","resources:","limits:"]

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    passed = True
    found, missing = [], []
    paths = ["K8s/helm/templates/daemonset.yaml",
             "../../K8s/helm/templates/daemonset.yaml",
             "../../../K8s/helm/templates/daemonset.yaml"]
    content = None
    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                content = f.read()
            print(f"  Found daemonset at: {p}")
            break
    if content:
        for field in REQUIRED:
            if field in content:
                found.append(field)
                print(f"  FOUND: {field}")
            else:
                missing.append(field)
                print(f"  MISSING: {field}")
        if missing:
            passed = False
    else:
        print(f"  daemonset.yaml not found in path — check K8s/helm/templates/")
        passed = False
    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "fields_found": found, "fields_missing": missing,
              "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] Kubernetes DaemonSet")
    return result

if __name__ == "__main__":
    run()
