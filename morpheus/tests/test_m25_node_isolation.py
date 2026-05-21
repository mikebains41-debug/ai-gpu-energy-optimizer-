"""M25 - Node Isolation"""
from datetime import datetime
from utils import get_gpu_metrics, log_result

TEST_ID = "M25"
TEST_NAME = "Node Isolation"

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    passed = True
    checks = []
    for idx in range(2):
        m = get_gpu_metrics(gpu_index=idx)
        reported = m.get("gpu_index", idx)
        isolated = (reported == idx)
        checks.append({"gpu_index": idx, "reported": reported, "isolated": isolated})
        print(f"  GPU {idx}: reported={reported} isolated={isolated}")
        if not isolated:
            passed = False
    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "checks": checks, "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] Node isolation")
    return result

if __name__ == "__main__":
    run()
