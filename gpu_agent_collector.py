import asyncio, aiohttp, datetime, os, sys
from collections import defaultdict
try:
    import pynvml
except ImportError:
    print("Run: pip install pynvml aiohttp"); sys.exit(1)

API_URL = os.getenv("API_URL", "http://localhost:8000")
NODE_ID = os.getenv("NODE_ID", "node-001")
POLL_S = 5
FLUSH_S = 30
RETRIES = 3
GHOST_W = 90.0
DESYNC_W = 100.0
DESYNC_PCT = 5.0

class GPUAgent:
    def __init__(self):
        pynvml.nvmlInit()
        self.count = pynvml.nvmlDeviceGetCount()
        self.handles = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.count)]
        self.buffer = defaultdict(list)
        self.last_flush = datetime.datetime.utcnow()
        print(f"GPUAgent: {self.count} GPU(s) on {NODE_ID}")

    def collect(self):
        t = datetime.datetime.utcnow().isoformat() + "Z"
        for i, h in enumerate(self.handles):
            try:
                pw = pynvml.nvmlDeviceGetPowerUsage(h) / 1000.0
                util = pynvml.nvmlDeviceGetUtilizationRates(h).gpu
                mem = pynvml.nvmlDeviceGetUtilizationRates(h).memory
                temp = pynvml.nvmlDeviceGetTemperature(h, pynvml.NVML_TEMPERATURE_GPU)
                try: mc = pynvml.nvmlDeviceGetClockInfo(h, pynvml.NVML_CLOCK_MEM)
                except: mc = 0
                try: ps = pynvml.nvmlDeviceGetPerformanceState(h)
                except: ps = -1
                ghost = (util == 0 and pw > GHOST_W)
                desync = (util < DESYNC_PCT and pw > DESYNC_W)
                if ghost: print(f"[GHOST] GPU{i} {pw:.1f}W @ 0%")
                if desync: print(f"[DESYNC] GPU{i} {pw:.1f}W @ {util}%")
                self.buffer[f"gpu-{i}"].append({"timestamp": t, "gpu_id": f"gpu-{i}", "node_id": NODE_ID, "power_watts": round(pw,2), "gpu_util": util, "mem_util": mem, "temp_c": temp, "ghost_flag": ghost, "desync_flag": desync, "mem_clock_mhz": mc, "p_state": ps})
            except Exception as e:
                print(f"GPU{i} error: {e}")

    def due(self):
        return (datetime.datetime.utcnow() - self.last_flush).total_seconds() >= FLUSH_S

    async def flush(self, session):
        payload = [s for samples in self.buffer.values() for s in samples]
        if not payload: return
        for attempt in range(RETRIES):
            try:
                async with session.post(f"{API_URL}/ingest/batch", json={"metrics": payload}, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    if r.status == 200:
                        print(f"Flushed {len(payload)} samples")
                        self.buffer.clear()
                        self.last_flush = datetime.datetime.utcnow()
                        return
            except Exception as e:
                print(f"Flush attempt {attempt+1}: {e}")
                await asyncio.sleep(2**attempt)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            while True:
                self.collect()
                if self.due(): await self.flush(session)
                await asyncio.sleep(POLL_S)

    def stop(self): pynvml.nvmlShutdown()

if __name__ == "__main__":
    agent = GPUAgent()
    try: asyncio.run(agent.run())
    except KeyboardInterrupt: agent.stop()
