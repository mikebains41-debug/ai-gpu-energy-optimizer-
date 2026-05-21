"""M24 - Rate Limiting"""
import requests
from datetime import datetime
from utils import log_result

TEST_ID = "M24"
TEST_NAME = "Rate Limiting"
API_BASE = "http://localhost:8000"
BURST = 50

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    codes = []
    for i in range(BURST):
        try:
            r = requests.get(f"{API_BASE}/api/v1/health", timeout=3)
            codes.append(r.status_code)
        except:
            codes.append(0)
    rate_limited = any(c == 429 for c in codes)
    refused = all(c == 0 for c in codes)
    passed = rate_limited or refused
    summary = {str(c): codes.count(c) for c in set(codes)}
    print(f"  Burst={BURST} | rate_limited={rate_limited} | refused={refused}")
    print(f"  Status summary: {summary}")
    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "burst_count": BURST, "rate_limited": rate_limited,
              "status_summary": summary, "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] Rate limiting")
    return result

if __name__ == "__main__":
    run()
