"""M20 - CEI Accuracy Test"""
import time
from datetime import datetime
from utils import get_gpu_stats, save_result

TEST_ID = "M20"
TEST_NAME = "CEI Accuracy"
EXPECTED_CEI = 5.68e9
TOLERANCE = 0.20
FP32_FLOPS = 19.5e12

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    passed = True
    readings = []

    for i in range(10):
        stats = get_gpu_stats(gpu_id=0)
        power = stats["power_watts"]
        if power > 0:
            cei = FP32_FLOPS / power
            readings.append(cei)
            print(f"  Sample {i+1}: power={power}W CEI={cei:.3e} FLOPs/J")
        time.sleep(2)

    if readings:
        avg_cei = sum(readings) / len(readings)
        lower = EXPECTED_CEI * (1 - TOLERANCE)
        upper = EXPECTED_CEI * (1 + TOLERANCE)
        passed = lower <= avg_cei <= upper
        print(f"  Avg CEI: {avg_cei:.3e} | Expected: {EXPECTED_CEI:.3e} +/-{int(TOLERANCE*100)}%")
    else:
        passed = False
        avg_cei = 0

    duration = time.time() - start
    data = {"avg_cei": avg_cei, "expected_cei": EXPECTED_CEI,
            "tolerance_pct": TOLERANCE * 100, "samples": len(readings)}
    result = save_result(TEST_ID, TEST_NAME, passed, data, round(duration, 2))
    print(f"  [{'PASS' if passed else 'FAIL'}] CEI Accuracy")
    return result

if __name__ == "__main__":
    run()
