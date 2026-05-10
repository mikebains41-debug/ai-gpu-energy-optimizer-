#!/usr/bin/env python3
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.
# Contact: mikebains41@gmail.com

import sys
import time

def main():
    try:
        import pynvml
    except ImportError:
        print("ERROR: pynvml not installed")
        return

    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    gpu_name = pynvml.nvmlDeviceGetName(handle)
    
    print(f"GPU: {gpu_name}")
    print("Scanning for ghost power (60 seconds)...")
    
    ghost_events = []
    
    for i in range(60):
        power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
        util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        
        if power > 70 and util == 0:
            ghost_events.append((i, power))
        
        print(f"  {i+1}s: {power:.1f}W, {util}%")
        time.sleep(1)
    
    print("\n=== RESULTS ===")
    if ghost_events:
        print(f"⚠️ GHOST POWER: {len(ghost_events)} events")
        for t, p in ghost_events[:3]:
            print(f"   Time {t}s: {p:.1f}W at 0% util")
    else:
        print("✅ No ghost power detected")
    
    pynvml.nvmlShutdown()

if __name__ == "__main__":
    main()
