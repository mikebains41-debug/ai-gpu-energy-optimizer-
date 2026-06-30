#!/usr/bin/env python3
import time, json, datetime, sys
try:
    import pynvml
except ImportError:
    print("Run: pip install pynvml"); sys.exit(1)

def _measure_idle_baseline():
    """Sample power for 1s at startup to get a real idle baseline."""
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    samples = []
    for _ in range(5):
        pw = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
        samples.append(pw)
        time.sleep(0.2)
    return sum(samples) / len(samples)

_IDLE_BASELINE_W = _measure_idle_baseline()
GHOST_POWER_W = round(_IDLE_BASELINE_W + 8.0, 2)    # Dynamic idle+8W — same method as M2
DESYNC_POWER_W = round(_IDLE_BASELINE_W + 20.0, 2)  # Dynamic idle+20W for desync threshold
DESYNC_UTIL_PCT = 5.0
LOCKED_MEM_CLOCK = 1593
POLL_INTERVAL = 1.0
REPORT_FILE = "ghost_report.json"

def ts(): return datetime.datetime.utcnow().isoformat() + "Z"

def classify(pw, util, mem_clk, pstate):
    a = []
    if util == 0 and pw > GHOST_POWER_W: a.append("GHOST")
    if util < DESYNC_UTIL_PCT and pw > DESYNC_POWER_W: a.append("DESYNC")
    if pstate == 0 and util == 0: a.append("P0_LOCK")
    if mem_clk >= LOCKED_MEM_CLOCK and util == 0: a.append("MEM_CLOCK_LOCK")
    return a

def main():
    pynvml.nvmlInit()
    count = pynvml.nvmlDeviceGetCount()
    handles = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(count)]
    names = [pynvml.nvmlDeviceGetName(h) for h in handles]
    print("="*70)
    print("  GPU GHOST POWER DETECTOR")
    print("  github.com/mikebains41-debug/ai-gpu-energy-optimizer-")
    print("="*70)
    all_samples = {i: [] for i in range(count)}
    try:
        while True:
            for i, h in enumerate(handles):
                pw = pynvml.nvmlDeviceGetPowerUsage(h) / 1000.0
                util = pynvml.nvmlDeviceGetUtilizationRates(h).gpu
                try: mc = pynvml.nvmlDeviceGetClockInfo(h, pynvml.NVML_CLOCK_MEM)
                except: mc = 0
                try: ps = pynvml.nvmlDeviceGetPerformanceState(h)
                except: ps = -1
                temp = pynvml.nvmlDeviceGetTemperature(h, pynvml.NVML_TEMPERATURE_GPU)
                anom = classify(pw, util, mc, ps)
                tag = " | ".join(anom) if anom else "OK"
                print(f"[{ts()[11:19]}] GPU{i} {names[i][:20]:20s} | {pw:6.1f}W | {util:3d}% | P{ps} | {mc}MHz | {tag}")
                all_samples[i].append({"t": ts(), "pw": round(pw,2), "util": util, "mc": mc, "ps": ps, "temp": temp, "anom": anom})
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nSaving report...")
    report = {"ts": ts(), "author": "Manmohan Bains", "gpus": []}
    for i in range(count):
        s = all_samples[i]
        pws = [x["pw"] for x in s]
        ghosts = [x for x in s if "GHOST" in x["anom"]]
        report["gpus"].append({"gpu": names[i], "samples": len(s), "max_w": max(pws) if pws else 0, "ghost_events": len(ghosts), "verdict": "ANOMALY" if ghosts else "CLEAN", "data": s})
        print(f"GPU{i}: {len(ghosts)} GHOST events | max {max(pws) if pws else 0}W")
    with open(REPORT_FILE, "w") as f: json.dump(report, f, indent=2)
    print(f"Report saved: {REPORT_FILE}")
    pynvml.nvmlShutdown()

if __name__ == "__main__": main()
