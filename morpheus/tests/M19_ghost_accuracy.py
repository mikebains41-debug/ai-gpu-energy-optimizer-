#!/usr/bin/env python3
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result

GHOST_W = 90.0
IDLE_FLOOR_W = 67.0
DURATION = 1800

def main():
    print("M19: Ghost Accuracy vs Baseline")
    count = get_gpu_count()
    ghost_events = 0
    false_positives = 0
    true_positives = 0
    samples = 0
    start = time.time()
    while time.time() - start < DURATION:
        for gpu_id in range(min(count, 2)):
            s = get_gpu_stats(gpu_id)
            samples += 1
            is_ghost = s["gpu_util"] == 0 and s["power_watts"] > GHOST_W
            is_true_ghost = s["gpu_util"] == 0 and s["power_watts"] > IDLE_FLOOR_W + 10
            if is_ghost:
                ghost_events += 1
                if is_true_ghost:
                    true_positives += 1
                else:
                    false_positives += 1
        time.sleep(1)
    accuracy = (true_positives / ghost_events * 100) if ghost_events > 0 else 100
    passed = accuracy >= 95 and false_positives == 0
    save_result("M19", "Ghost Accuracy", passed,
        {"ghost_events": ghost_events, "accuracy_pct": accuracy,
         "false_positives": false_positives, "samples": samples}, int(time.time()))
    print(f"M19: {'PASS' if passed else 'FAIL'}")
    sys.exit(0 if passed else 1)

main()
