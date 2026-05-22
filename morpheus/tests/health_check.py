#!/usr/bin/env python3
"""
Pre-flight health check — run before starting 30 tests on RunPod.
Verifies nvidia-smi works and both GPUs are visible.
"""
import subprocess, sys

def check():
    print("GPU Health Check\n" + "="*40)
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,name,power.draw,utilization.gpu,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            print("FAIL: nvidia-smi returned error")
            print(result.stderr)
            sys.exit(1)

        gpus = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        print(f"GPUs found: {len(gpus)}")
        for gpu in gpus:
            parts = [p.strip() for p in gpu.split(",")]
            print(f"  GPU {parts[0]}: {parts[1]} | Power: {parts[2]}W | Util: {parts[3]}% | Temp: {parts[4]}C")

        if len(gpus) < 2:
            print("\nWARNING: Expected 2 GPUs, found fewer. Multi-GPU tests may fail.")
        else:
            print("\nPASS: Both GPUs visible and responding.")

        print("="*40)
        print("Ready to run: python morpheus/tests/run_all.py")

    except FileNotFoundError:
        print("FAIL: nvidia-smi not found. Not on a GPU instance.")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check()
