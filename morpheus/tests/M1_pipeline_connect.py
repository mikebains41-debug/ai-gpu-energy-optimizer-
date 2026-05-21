#!/usr/bin/env python3
"""
M1 - Pipeline Connect
Duration: 10 minutes
GPUs: 1
What: Connects to API, pulls live data, confirms flow
Pass: Data received, zero errors for 60 seconds
"""
import sys, os, time, datetime
sys.path.insert(0, os.getcwd())
from morpheus.tests.utils import get_gpu_name, save_result
try:
    import aiohttp, asyncio
except ImportError:
    os.system("pip install aiohttp -q")
    import aiohttp, asyncio

API_URL = os.getenv("API_URL", "https://ai-gpu-brain-v3.onrender.com")
DURATION = 60

async def main():
    print("="*55)
    print("M1: Pipeline Connect")
    print(f"GPU: {get_gpu_name(0)}")
    print(f"API: {API_URL}")
    print("="*55)
    errors = 0
    samples = 0
    start = time.time()
    async with aiohttp.ClientSession() as session:
        while time.time() - start < DURATION:
            try:
                async with session.get(
                    f"{API_URL}/metrics/a100",
                    timeout=aiohttp.ClientTimeout(total=10)) as r:
                    if r.status == 200:
                        samples += 1
                        print(f"[OK] Sample {samples} | Status {r.status}")
                    else:
                        errors += 1
                        print(f"[ERROR] Status {r.status}")
            except Exception as e:
                errors += 1
                print(f"[ERROR] {e}")
            await asyncio.sleep(5)
    duration = int(time.time() - start)
    passed = errors == 0 and samples > 0
    save_result("M1", "Pipeline Connect", passed,
        {"samples": samples, "errors": errors}, duration)
    print(f"\nM1: {'PASS' if passed else 'FAIL'}")
    print(f"Samples: {samples} | Errors: {errors}")
    sys.exit(0 if passed else 1)

asyncio.run(main())
