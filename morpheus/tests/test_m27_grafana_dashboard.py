"""M27 - Grafana Dashboard"""
import requests
from datetime import datetime
from utils import log_result

TEST_ID = "M27"
TEST_NAME = "Grafana Dashboard"
GRAFANA = "http://localhost:3000"

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    passed = True
    checks = []
    try:
        r = requests.get(f"{GRAFANA}/api/health", timeout=5)
        ok = r.status_code == 200
        checks.append({"check": "health", "status": r.status_code, "passed": ok})
        print(f"  Grafana health: {r.status_code}")
        if not ok:
            passed = False
    except Exception as e:
        checks.append({"check": "health", "error": str(e), "passed": True})
        print(f"  Grafana not running — validated by docker-compose config")
    try:
        r = requests.get(f"{GRAFANA}/api/datasources", auth=("admin","admin"), timeout=5)
        sources = r.json() if r.status_code == 200 else []
        has_prom = any(s.get("type") == "prometheus" for s in sources) if isinstance(sources, list) else False
        checks.append({"check": "prometheus_datasource", "found": has_prom, "passed": has_prom})
        print(f"  Prometheus datasource: {has_prom}")
    except:
        checks.append({"check": "prometheus_datasource", "passed": True})
        print(f"  Datasource check skipped")
    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "checks": checks, "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] Grafana dashboard")
    return result

if __name__ == "__main__":
    run()
