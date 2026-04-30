# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 4: Sampling Gap Estimator - Depends on Engine 3
"""

from typing import List, Dict
from .engine3_burst import detect_compute_bursts

def estimate_sampling_gap(metrics_history: List[Dict]) -> Dict:
    burst = detect_compute_bursts(metrics_history)
    burst_count = burst.get("burst_count", 0)
    
    missed_sec = burst_count * 0.05  # 50ms per burst
    total_time = len(metrics_history)
    gap_pct = (missed_sec / total_time) * 100 if total_time > 0 else 0
    
    if gap_pct > 5:
        severity, msg = "HIGH", f"Monitoring misses ~{gap_pct:.1f}% of compute activity"
    elif gap_pct > 1:
        severity, msg = "MEDIUM", f"Monitoring misses ~{gap_pct:.1f}% of compute activity"
    else:
        severity, msg = "LOW", f"Sampling gap is {gap_pct:.2f}% - acceptable"
    
    return {
        "sampling_gap_percent": round(gap_pct, 2),
        "severity": severity,
        "message": msg,
        "estimated_missed_seconds": round(missed_sec, 3),
        "burst_count": burst_count
    }
