# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 3: Kernel Burst Detection (FIXED)
Detects compute bursts from kernel execution timing
"""

import numpy as np
from typing import List, Dict

# Global store for kernel timestamps
_kernel_times = []

def detect_compute_bursts(metrics_history: List[Dict]) -> Dict:
    """
    Detect bursts from kernel execution windows
    """
    global _kernel_times
    
    if len(_kernel_times) < 10:
        return {
            "error": "Insufficient kernel data",
            "burst_count": 0,
            "bursts_per_minute": 0.0,
            "peak_power_watts": 0,
            "confidence": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        }
    
    threshold_ms = 10  # Bursts shorter than 10ms
    
    bursts = []
    current_burst = []
    
    for t in _kernel_times:
        if t < threshold_ms:
            current_burst.append(t)
        else:
            if current_burst:
                bursts.append(current_burst)
            current_burst = []
    
    if current_burst:
        bursts.append(current_burst)
    
    burst_count = len(bursts)
    
    # Calculate burst density (bursts per minute)
    total_time_seconds = sum(_kernel_times) / 1000
    bursts_per_minute = burst_count / max(total_time_seconds / 60, 1)
    
    return {
        "burst_count": burst_count,
        "bursts_per_minute": round(bursts_per_minute, 2),
        "avg_burst_duration_ms": round(np.mean(_kernel_times), 2) if _kernel_times else 0,
        "burst_density": round(burst_count / max(len(_kernel_times), 1), 4),
        "confidence": {"HIGH": burst_count, "MEDIUM": 0, "LOW": 0},
        "samples_analyzed": len(_kernel_times)
    }

def add_kernel_time(kernel_ms: float):
    """Add kernel execution time to history"""
    global _kernel_times
    _kernel_times.append(kernel_ms)
    if len(_kernel_times) > 1000:
        _kernel_times.pop(0)
