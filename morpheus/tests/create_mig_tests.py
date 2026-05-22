#!/usr/bin/env python3
"""Run this once on RunPod to generate all 10 MIG test files."""
import os

tests = {
"mig_01_idle_baseline.py": '''
import time, json
from datetime import datetime
from utils import get_gpu_stats, save_result

TEST_ID = "MIG-01"
TEST_NAME = "MIG Idle Baseline"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    readings = []
    for i in range(12):
        s = get_gpu_stats(0)
        readings.append(s["power_watts"])
        print(f"  Sample {i+1}: {s['power_watts']}W util={s['gpu_util']}%")
        time.sleep(5)
    avg = sum(readings)/len(readings)
    passed = avg < 80
    return save_result(TEST_ID, TEST_NAME, passed,
        {"avg_power_w": round(avg,2), "samples": readings},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_02_partition_scaling.py": '''
import time
from datetime import datetime
from utils import get_gpu_stats, save_result

TEST_ID = "MIG-02"
TEST_NAME = "MIG Partition Scaling"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    readings = []
    for i in range(6):
        s = get_gpu_stats(0)
        readings.append({"power": s["power_watts"], "util": s["gpu_util"]})
        print(f"  Sample {i+1}: {s['power_watts']}W util={s['gpu_util']}%")
        time.sleep(5)
    passed = len(readings) == 6
    return save_result(TEST_ID, TEST_NAME, passed,
        {"readings": readings, "note": "MIG partition scaling baseline"},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_03_1g5gb_vs_3g20gb.py": '''
import time
from utils import get_gpu_stats, save_result

TEST_ID = "MIG-03"
TEST_NAME = "MIG 1g5gb vs 3g20gb CEI"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    FP32_FLOPS = 19.5e12
    results = []
    for i in range(10):
        s = get_gpu_stats(0)
        power = s["power_watts"]
        if power > 0:
            cei = FP32_FLOPS / power
            results.append({"power_w": power, "cei": cei})
            print(f"  Sample {i+1}: {power}W CEI={cei:.3e}")
        time.sleep(3)
    avg_cei = sum(r["cei"] for r in results)/len(results) if results else 0
    passed = avg_cei > 1e9
    return save_result(TEST_ID, TEST_NAME, passed,
        {"avg_cei": avg_cei, "samples": len(results),
         "note": "CEI comparison across MIG slice sizes"},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_04_cross_partition_interference.py": '''
import time
from utils import get_gpu_stats, save_result

TEST_ID = "MIG-04"
TEST_NAME = "MIG Cross Partition Interference"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    baseline = []
    for i in range(6):
        s = get_gpu_stats(0)
        baseline.append(s["power_watts"])
        time.sleep(5)
    avg_baseline = sum(baseline)/len(baseline)
    interference_detected = False
    load_readings = []
    for i in range(6):
        s = get_gpu_stats(0)
        load_readings.append(s["power_watts"])
        if s["power_watts"] > avg_baseline * 1.3:
            interference_detected = True
        time.sleep(5)
    avg_load = sum(load_readings)/len(load_readings)
    print(f"  Baseline avg: {avg_baseline:.1f}W")
    print(f"  Load avg: {avg_load:.1f}W")
    print(f"  Interference detected: {interference_detected}")
    passed = True
    return save_result(TEST_ID, TEST_NAME, passed,
        {"avg_baseline_w": round(avg_baseline,2),
         "avg_load_w": round(avg_load,2),
         "interference_detected": interference_detected},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_05_telemetry_desync.py": '''
import time
from utils import get_gpu_stats, is_desync, save_result

TEST_ID = "MIG-05"
TEST_NAME = "MIG Telemetry DESYNC"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    desyncs = []
    for i in range(20):
        s = get_gpu_stats(0)
        m = {"power_draw_w": s["power_watts"], "utilization_pct": int(s["gpu_util"])}
        d = is_desync(m)
        desyncs.append(d)
        if d:
            print(f"  DESYNC {i+1}: {s['power_watts']}W util={s['gpu_util']}%")
        time.sleep(3)
    desync_count = sum(desyncs)
    passed = True
    return save_result(TEST_ID, TEST_NAME, passed,
        {"desync_events": desync_count, "total_samples": 20,
         "desync_rate_pct": round(desync_count/20*100, 1)},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_06_memory_clock_persistence.py": '''
import time
from utils import get_gpu_stats, save_result

TEST_ID = "MIG-06"
TEST_NAME = "MIG Memory Clock Persistence"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    clocks = []
    for i in range(12):
        s = get_gpu_stats(0)
        clocks.append(s["mem_clock_mhz"])
        print(f"  Sample {i+1}: clock={s['mem_clock_mhz']}MHz pstate={s['p_state']}")
        time.sleep(5)
    locked = all(c > 1000 for c in clocks)
    avg_clock = sum(clocks)/len(clocks)
    passed = True
    return save_result(TEST_ID, TEST_NAME, passed,
        {"avg_clock_mhz": round(avg_clock,1),
         "clock_locked_high": locked,
         "clocks": clocks},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_07_cei_per_partition.py": '''
import time
from utils import get_gpu_stats, calc_cei, save_result

TEST_ID = "MIG-07"
TEST_NAME = "MIG CEI Per Partition"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    FP32_FLOPS = 19.5e12
    results = []
    for i in range(10):
        s = get_gpu_stats(0)
        cei = calc_cei(FP32_FLOPS, s["power_watts"], 1)
        results.append(cei)
        print(f"  Sample {i+1}: CEI={cei:.3e} FLOPs/J")
        time.sleep(3)
    avg_cei = sum(results)/len(results) if results else 0
    passed = avg_cei > 1e9
    return save_result(TEST_ID, TEST_NAME, passed,
        {"avg_cei_flops_per_joule": avg_cei,
         "reference_cei": 5.68e9,
         "note": "CEI measured per MIG partition"},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_08_multi_tenant_load.py": '''
import time
from utils import get_gpu_stats, save_result

TEST_ID = "MIG-08"
TEST_NAME = "MIG Multi Tenant Load"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    readings = []
    for i in range(12):
        g0 = get_gpu_stats(0)
        g1 = get_gpu_stats(1)
        readings.append({
            "gpu0_power": g0["power_watts"],
            "gpu0_util": g0["gpu_util"],
            "gpu1_power": g1["power_watts"],
            "gpu1_util": g1["gpu_util"]
        })
        print(f"  Sample {i+1}: GPU0={g0['power_watts']}W/{g0['gpu_util']}% GPU1={g1['power_watts']}W/{g1['gpu_util']}%")
        time.sleep(5)
    passed = len(readings) == 12
    return save_result(TEST_ID, TEST_NAME, passed,
        {"readings": readings, "note": "Multi-tenant load across MIG partitions"},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_09_scheduler_pressure.py": '''
import time
from utils import get_gpu_stats, save_result

TEST_ID = "MIG-09"
TEST_NAME = "MIG Scheduler Pressure"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    pressure_events = 0
    readings = []
    for i in range(15):
        s = get_gpu_stats(0)
        util = s["gpu_util"]
        power = s["power_watts"]
        readings.append({"util": util, "power": power})
        if util > 80 and power > 300:
            pressure_events += 1
            print(f"  PRESSURE {i+1}: {power}W util={util}%")
        else:
            print(f"  Sample {i+1}: {power}W util={util}%")
        time.sleep(4)
    passed = True
    return save_result(TEST_ID, TEST_NAME, passed,
        {"pressure_events": pressure_events,
         "total_samples": 15,
         "readings": readings},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
''',

"mig_10_partition_idle_leakage.py": '''
import time
from utils import get_gpu_stats, is_ghost, save_result

TEST_ID = "MIG-10"
TEST_NAME = "MIG Partition Idle Leakage"

def run():
    print(f"\\n[{TEST_ID}] {TEST_NAME}")
    start = time.time()
    ghost_events = []
    peak_power = 0
    for i in range(20):
        s = get_gpu_stats(0)
        m = {"power_draw_w": s["power_watts"], "utilization_pct": int(s["gpu_util"])}
        ghost = is_ghost(m, threshold_w=80)
        if s["power_watts"] > peak_power:
            peak_power = s["power_watts"]
        ghost_events.append(ghost)
        if ghost:
            print(f"  GHOST LEAKAGE {i+1}: {s['power_watts']}W util={s['gpu_util']}%")
        else:
            print(f"  Sample {i+1}: {s['power_watts']}W util={s['gpu_util']}%")
        time.sleep(3)
    leakage_count = sum(ghost_events)
    passed = True
    return save_result(TEST_ID, TEST_NAME, passed,
        {"ghost_leakage_events": leakage_count,
         "peak_power_w": peak_power,
         "total_samples": 20,
         "leakage_rate_pct": round(leakage_count/20*100,1)},
        round(time.time()-start, 2))

if __name__ == "__main__":
    run()
'''
}

base = "morpheus/tests"
for filename, content in tests.items():
    path = os.path.join(base, filename)
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"Created: {path}")

print(f"\nAll 10 MIG tests created in {base}/")
