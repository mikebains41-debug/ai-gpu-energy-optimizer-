#!/usr/bin/env python3
"""
Shared GPU stats utility
Uses pynvml with nvidia-smi fallback
Works on all RunPod instances
Author: Manmohan Bains
"""
import subprocess, os

def get_gpu_stats(gpu_id=0):
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        pw = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
        util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        mem = pynvml.nvmlDeviceGetUtilizationRates(handle).memory
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        try:
            mc = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        except:
            mc = 0
        try:
            ps = pynvml.nvmlDeviceGetPerformanceState(handle)
        except:
            ps = -1
        return {"power_watts": pw, "gpu_util": util, "mem_util": mem, "temp_c": temp, "mem_clock_mhz": mc, "p_state": ps, "source": "pynvml"}
    except:
        try:
            result = subprocess.run(
                ["nvidia-smi",
                 f"--id={gpu_id}",
                 "--query-gpu=power.draw,utilization.gpu,utilization.memory,temperature.gpu,clocks.mem",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=10
            )
            parts = result.stdout.strip().split(", ")
            return {"power_watts": float(parts[0]), "gpu_util": float(parts[1]), "mem_util": float(parts[2]), "temp_c": float(parts[3]), "mem_clock_mhz": float(parts[4]), "p_state": -1, "source": "nvidia-smi"}
        except Exception as e:
            return {"power_watts": 0, "gpu_util": 0, "mem_util": 0, "temp_c": 0, "mem_clock_mhz": 0, "p_state": -1, "source": "error", "error": str(e)}

def get_gpu_count():
    try:
        import pynvml
        pynvml.nvmlInit()
        return pynvml.nvmlDeviceGetCount()
    except:
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10
            )
            return len(result.stdout.strip().split("\n"))
        except:
            return 0

def get_gpu_name(gpu_id=0):
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        return pynvml.nvmlDeviceGetName(handle)
    except:
        try:
            result = subprocess.run(
                ["nvidia-smi", f"--id={gpu_id}", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip()
        except:
            return "Unknown GPU"

def save_result(test_id, name, passed, data, duration):
    import json, datetime, os
    os.makedirs("morpheus/tests/results", exist_ok=True)
    result = {
        "test_id": test_id,
        "name": name,
        "status": "PASS" if passed else "FAIL",
        "duration_seconds": duration,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "gpu": get_gpu_name(0),
        "data": data
    }
    path = f"morpheus/tests/results/{test_id}_result.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result saved: {path}")
    return result
