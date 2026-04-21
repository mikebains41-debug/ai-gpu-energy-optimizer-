import pynvml
import requests
import time
import json
import os

class GPUMonitorAgent:
    def __init__(self, backend_url, cluster_id, api_key):
        self.backend_url = backend_url
        self.cluster_id = cluster_id
        self.api_key = api_key
        
        try:
            pynvml.nvmlInit()
            self.gpu_count = pynvml.nvmlDeviceGetCount()
            print(f"Found {self.gpu_count} GPUs")
        except:
            self.gpu_count = 0
            print("No GPUs detected (mock mode)")
    
    def collect_metrics(self):
        metrics = {
            "cluster_id": self.cluster_id,
            "timestamp": time.time(),
            "gpus": []
        }
        
        if self.gpu_count == 0:
            # Mock data
            metrics["gpus"].append({
                "gpu_id": 0,
                "utilization_percent": 75.5,
                "memory_used_gb": 12.3,
                "temperature_celsius": 72.0,
                "power_draw_watts": 285.0
            })
        else:
            for i in range(self.gpu_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                temp = pynvml.nvmlDeviceGetTemperature(handle, 0)
                power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
                memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                
                metrics["gpus"].append({
                    "gpu_id": i,
                    "utilization_percent": float(util.gpu),
                    "memory_used_gb": memory.used / 1024**3,
                    "temperature_celsius": float(temp),
                    "power_draw_watts": float(power)
                })
        
        return metrics
    
    def send_to_backend(self):
        metrics = self.collect_metrics()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/metrics",
                json=metrics,
                headers=headers,
                timeout=5
            )
            print(f"Sent metrics: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"Failed: {e}")
            return False
    
    def run(self, interval=2):
        print(f"Starting monitor for cluster: {self.cluster_id}")
        while True:
            self.send_to_backend()
            time.sleep(interval)

if __name__ == "__main__":
    config = {
        "backend_url": "https://ai-gpu-brain-v2.onrender.com",
        "cluster_id": "test-cluster-1",
        "api_key": "test_key_123"
    }
    
    agent = GPUMonitorAgent(**config)
    agent.run()
