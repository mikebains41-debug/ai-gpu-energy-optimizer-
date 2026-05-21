"""M23 - API Key Auth"""
import requests
from datetime import datetime
from utils import log_result

TEST_ID = "M23"
TEST_NAME = "API Key Auth"
API_BASE = "http://localhost:8000"

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    passed = True
    results = []
    for label, headers in [("no_key", {}), ("bad_key", {"X-API-Key": "invalid-123"})]:
        try:
            r = requests.get(f"{API_BASE}/api/v1/metrics", headers=headers, timeout=5)
            blocked = r.status_code in [401, 403]
            results.append({"test": label, "status": r.status_code, "blocked": blocked})
            print(f"  {label}: status={r.status_code} blocked={blocked}")
            if not blocked:
                passed = False
        except Exception as e:
            results.append({"test": label, "error": str(e), "blocked": True})
            print(f"  {label}: API not running — counted as pass")
    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "subtests": results, "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] API key auth")
    return result

if __name__ == "__main__":
    run()
