import pynvml
import time
import json

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

print("Logging GPU telemetry. Press Ctrl+C to stop.")

try:
    while True:
        power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
        util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        
        data = {
            "timestamp": time.time(),
            "power_w": round(power, 2),
            "util": util
        }
        
        if power > 70 and util == 0:
            data["event"] = "desync_detected"
            print(f"⚠️ DESYNC: {power}W at {util}%")
        
        with open("gpu_log.jsonl", "a") as f:
            f.write(json.dumps(data) + "\n")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped. Log saved to gpu_log.jsonl")
