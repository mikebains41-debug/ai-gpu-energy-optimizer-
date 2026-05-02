#!/usr/bin/env python3
"""
Experiment 1: Nsight + nvidia-smi parallel capture
"""

import subprocess
import time
import json
from datetime import datetime

def run_nsight_trace(duration=60):
    cmd = [
        "nsys", "profile",
        "--trace=cuda,nvtx,osrt",
        "--output=gpu_trace",
        "--force-overwrite=true",
        "--duration=" + str(duration),
        "python", "-c", "import torch; x=torch.randn(4096,4096,device='cuda'); [torch.matmul(x,x) for _ in range(100)]"
    ]
    try:
        subprocess.run(cmd, timeout=duration+10)
        return {"status": "success", "output": "gpu_trace.nsys-rep"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

def check_nvidia_smi():
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=power.draw,utilization.gpu", "--format=csv,noheader"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def main():
    print("=" * 60)
    print("EXPERIMENT 1: Nsight + nvidia-smi Parallel Capture")
    print("=" * 60)
    
    results = {"timestamp": datetime.now().isoformat(), "nsight": run_nsight_trace(60), "smi_samples": []}
    
    for i in range(30):
        smi = check_nvidia_smi()
        results["smi_samples"].append({"time": i*2, "smi": smi})
        print(f"Sample {i+1}/30: {smi}")
        time.sleep(2)
    
    with open("experiment1_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Saved to experiment1_results.json")

if __name__ == "__main__":
    main()
