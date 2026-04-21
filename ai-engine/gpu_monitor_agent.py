import pynvml
import requests
import time
import json
import os
import sys
import signal

class GPUMonitorAgent:
    def __init__(self, config_path="config.json"):
        # Load config
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            print("Please run install.sh first to generate config.json")
            sys.exit(1)
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.backend_url = config.get("backend_url", "https://ai-gpu-brain-v2.onrender.com")
        self.cluster_id = config.get("cluster_id")
        self.api_key = config.get("api_key")
        self.check_interval = config.get("check_interval_seconds", 2)
        
        # Validate required fields
        if not self.cluster_id or self.cluster_id == "YOUR_CLUSTER_ID_HERE":
            print("❌ Invalid cluster_id in config.json")
            sys.exit(1)
        
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            print("❌ Invalid api_key in config.json")
            sys.exit(1)
        
        print(f"✅ Config loaded: Cluster={self.cluster_id}, Backend={self.backend_url}")
        
        # Initialize NVML
        try:
            pynvml.nvmlInit()
            self.gpu_count = pynvml.nvmlDeviceGetCount()
            print(f"✅ Found {self.gpu_count} NVIDIA GPU(s)")
        except Exception as e:
            print(f"⚠️ No NVIDIA GPUs detected: {e}")
            print("   Running in MOCK mode with simulated data")
            self.gpu_count = 0
        
        # Metrics tracking for retry logic
        self.consecutive_failures = 0
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
    
    def shutdown(self, signum, frame):
        print("\n🛑 Shutting down agent...")
        self.running = False
    
    def collect_metrics(self):
        """Collect GPU metrics via NVML or generate mock data"""
        metrics = {
            "cluster_id": self.cluster_id,
            "timestamp": time.time(),
            "gpus": []
        }
        
        if self.gpu_count == 0:
            # Mock data for testing
            metrics["gpus"].append({
                "gpu_id": 0,
                "utilization_percent": 75.5,
                "memory_used_gb": 12.3,
                "memory_total_gb": 80.0,
                "temperature_celsius": 72.0,
                "power_draw_watts": 285.0
            })
        else:
            for i in range(self.gpu_count):
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    
                    # Get utilization
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    
                    # Get temperature
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    
                    # Get power draw
                    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # mW to W
                    
                    # Get memory info
                    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    
                    metrics["gpus"].append({
                        "gpu_id": i,
                        "utilization_percent": float(util.gpu),
                        "memory_used_gb": memory.used / 1024**3,
                        "memory_total_gb": memory.total / 1024**3,
                        "temperature_celsius": float(temp),
                        "power_draw_watts": float(power)
                    })
                except Exception as e:
                    print(f"⚠️ Failed to read GPU {i}: {e}")
                    # Return mock data for this GPU as fallback
                    metrics["gpus"].append({
                        "gpu_id": i,
                        "utilization_percent": 50.0,
                        "memory_used_gb": 20.0,
                        "memory_total_gb": 80.0,
                        "temperature_celsius": 65.0,
                        "power_draw_watts": 200.0
                    })
        
        return metrics
    
    def send_to_backend_with_retry(self, metrics, max_retries=3):
        """Send metrics with exponential backoff retry"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.backend_url}/api/v1/metrics",
                    json=metrics,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.consecutive_failures = 0
                    return True
                elif response.status_code == 401:
                    print(f"❌ Authentication failed: Invalid API key")
                    return False
                else:
                    print(f"⚠️ Backend returned {response.status_code}: {response.text[:100]}")
                    
            except requests.exceptions.Timeout:
                print(f"⚠️ Timeout (attempt {attempt + 1}/{max_retries})")
            except requests.exceptions.ConnectionError:
                print(f"⚠️ Connection error (attempt {attempt + 1}/{max_retries})")
            except Exception as e:
                print(f"⚠️ Error: {e} (attempt {attempt + 1}/{max_retries})")
            
            # Exponential backoff: 1s, 2s, 4s
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        self.consecutive_failures += 1
        return False
    
    def run(self):
        """Main loop with health checks"""
        print(f"🚀 Starting GPU Monitor Agent for cluster: {self.cluster_id}")
        print(f"   Sending metrics every {self.check_interval} seconds")
        print("   Press Ctrl+C to stop\n")
        
        last_health_check = 0
        
        while self.running:
            try:
                # Collect metrics
                metrics = self.collect_metrics()
                
                # Send to backend
                success = self.send_to_backend_with_retry(metrics)
                
                if success:
                    gpu_count = len(metrics["gpus"])
                    print(f"✅ [{time.strftime('%H:%M:%S')}] Sent {gpu_count} GPU(s) metrics")
                else:
                    print(f"❌ [{time.strftime('%H:%M:%S')}] Failed to send metrics")
                
                # Health check every 60 seconds
                if time.time() - last_health_check > 60:
                    try:
                        health_response = requests.get(
                            f"{self.backend_url}/health",
                            timeout=5
                        )
                        if health_response.status_code == 200:
                            print(f"💚 Backend health: OK")
                        else:
                            print(f"⚠️ Backend health: {health_response.status_code}")
                    except Exception as e:
                        print(f"⚠️ Backend health check failed: {e}")
                    last_health_check = time.time()
                
                # Wait for next interval
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                time.sleep(5)
        
        # Cleanup
        if self.gpu_count > 0:
            pynvml.nvmlShutdown()
        print("👋 Agent stopped")

if __name__ == "__main__":
    agent = GPUMonitorAgent()
    agent.run()
