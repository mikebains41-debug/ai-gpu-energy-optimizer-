#!/usr/bin/env python3
import sys, os, time
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_stats, get_gpu_count, save_result
try:
    import torch
except ImportError:
    os.system("pip install torch -q")
    import torch

GHOST_W = 90.0
DESYNC_W = 100.0
DESYNC_PCT = 5.0
DURATION = 1800

def main():
    print("M21: False Positive Rate")
    count = get_gpu_count()
    device = torch.device("cuda:0")
    a = torch.randn(4096, 4096, device=device)
    b = torch.randn(4096, 4096, device=device)
    samples = 0
    false_ghost = 0
    false_desync = 0
    start = time.time()
    while time.time() - start < DURATION:
        torch.matmul(a, b)
        torch.cuda.synchronize()
        for gpu_id in range(min(count, 2)):
            s = get_gpu_stats(gpu_id)
            samples += 1
            if s["gpu_util"] == 0 and s["power_watts"] > GHOST_W:
                false_ghost += 1
            if s["gpu_util"] < DESYNC_PCT and s["power_watts"] > DESYNC_W:
                false_desync += 1
            if samples % 100 == 0:
                fp_rate = (false_ghost + false_desync) / samples * 100
                print(f"[OK] samples={samples} fp_rate={fp_rate:.3f}%")
        time.sleep(1)
    fp_rate = (false_ghost + false_desync) / samples * 100 if samples > 0 else 0
    passed = fp_rate < 1.0
    save_result("M21", "False Positive Rate", passed,
        {"samples": samples, "false_ghost": false_ghost,
         "false_desync": false_desync, "fp_rate_pct": fp_rate},
        int(time.time()))
    print(f"M21: {'PASS' if passed else 'FAIL'}")
    print(f"FP Rate: {fp_rate:.3f}%")
    sys.exit(0 if passed else 1)

main()
