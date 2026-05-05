import subprocess, time, requests

ENDPOINT = "http://YOUR_SERVER:5000/api/ingest"
TENANT_ID = "runpod_user_1"
INTERVAL = 30

def get_gpu_stats():
    try:
        models = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]).decode("utf-8").strip().split("\n")
        result = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,power.draw,memory.used", "--format=csv,noheader,nounits"]).decode("utf-8")
        stats = []
        for i, line in enumerate(result.strip().split("\n")):
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 3:
                continue
            stats.append({
                "gpu_id": str(i),
                "model": models[i] if i < len(models) else "unknown",
                "utilization": float(parts[0]),
                "power_watts": float(parts[1]),
                "memory_mb": float(parts[2])
            })
        return stats
    except Exception as e:
        print("nvidia-smi failed:", e)
        return []

def send():
    try:
        payload = {"tenant_id": TENANT_ID, "timestamp": time.time(), "gpus": get_gpu_stats()}
        r = requests.post(ENDPOINT, json=payload, timeout=5)
        if r.status_code != 200:
            print("Bad response:", r.text)
    except Exception as e:
        print("Error sending data:", e)

while True:
    start = time.time()
    send()
    elapsed = time.time() - start
    time.sleep(max(0, INTERVAL - elapsed))
