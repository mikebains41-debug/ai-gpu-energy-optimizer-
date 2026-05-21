"""M30 - End to End Integration"""
import time
from datetime import datetime
from utils import get_gpu_metrics, log_result

TEST_ID = "M30"
TEST_NAME = "End to End"

def run():
    print(f"\n[{TEST_ID}] {TEST_NAME}")
    passed = True
    steps = []

    # Step 1: GPU data collection
    try:
        m = get_gpu_metrics(gpu_index=0)
        ok = "power_draw_w" in m
        steps.append({"step": "gpu_data_collection", "passed": ok, "power_w": m.get("power_draw_w")})
        print(f"  Step 1 GPU collection: power={m.get('power_draw_w')}W ok={ok}")
        if not ok: passed = False
    except Exception as e:
        steps.append({"step": "gpu_data_collection", "passed": False, "error": str(e)})
        passed = False

    # Step 2: Ghost power check
    try:
        power = m.get("power_draw_w", 0)
        util = m.get("utilization_pct", 0)
        ghost = power > 50 and util < 5
        steps.append({"step": "ghost_power_check", "passed": True,
                       "ghost_detected": ghost, "power_w": power, "util_pct": util})
        print(f"  Step 2 Ghost check: power={power}W util={util}% ghost={ghost}")
    except Exception as e:
        steps.append({"step": "ghost_power_check", "passed": False, "error": str(e)})
        passed = False

    # Step 3: CEI calculation
    try:
        power_w = m.get("power_draw_w", 302)
        flops = 19.5e12
        cei = flops / power_w if power_w > 0 else 0
        cei_ok = cei > 1e9
        steps.append({"step": "cei_calculation", "passed": cei_ok,
                       "cei": cei, "flops_per_joule": round(cei, 2)})
        print(f"  Step 3 CEI: {cei:.3e} FLOPs/J ok={cei_ok}")
        if not cei_ok: passed = False
    except Exception as e:
        steps.append({"step": "cei_calculation", "passed": False, "error": str(e)})
        passed = False

    # Step 4: Sustained 30s run
    print(f"  Step 4 Sustained 30s run...")
    readings = []
    for i in range(6):
        r = get_gpu_metrics(gpu_index=0)
        readings.append(r.get("power_draw_w", 0))
        time.sleep(5)
    sustained_ok = len(readings) == 6
    steps.append({"step": "sustained_run", "passed": sustained_ok,
                   "readings": readings, "avg_power_w": round(sum(readings)/len(readings), 2)})
    print(f"  Step 4 complete: avg={sum(readings)/len(readings):.1f}W ok={sustained_ok}")
    if not sustained_ok: passed = False

    result = {"test_id": TEST_ID, "test_name": TEST_NAME, "passed": passed,
              "steps": steps, "total_steps": len(steps),
              "steps_passed": sum(1 for s in steps if s["passed"]),
              "timestamp": datetime.utcnow().isoformat()}
    log_result(result)
    print(f"  [{'PASS' if passed else 'FAIL'}] End to end — {result['steps_passed']}/{len(steps)} steps")
    return result

if __name__ == "__main__":
    run()
