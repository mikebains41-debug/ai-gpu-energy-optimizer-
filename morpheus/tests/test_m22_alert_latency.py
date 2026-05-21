"""M22 - Alert Latency"""
import time
from datetime import datetime
from utils import get_gpu_metrics, log_result

TEST_ID = "M22"
TEST_NAME = "Alert Latency"
THRESHOLD = 5.0

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    latencies = []
    passed = True
    for trial in range(5):
        t0 = time.time()
        metrics = get_gpu_metrics(gpu_index=0)
        latency = time.time() - t0
        latencies.append(latency)
        print(f"  Trial {trial+1}: {latency:.3f}s | power={metrics.get('power_draw_w','N/A')}W")
        if latency > THRESHOLD:
            passed = False
    avg = sum(latencies) / len(latencies)
    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "avg_latency_sec": round(avg, 4), "max_latency_sec": round(max(latencies), 4),
              "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] Avg latency: {avg:.3f}s")
    return result

if __name__ == "__main__":
    run()
