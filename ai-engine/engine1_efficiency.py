# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 1: True Efficiency Calculator (UPDATED)
Replaces unreliable utilization with power + burst signals
"""

import numpy as np
from typing import List, Dict
from .engine3_burst import detect_compute_bursts
from .engine4_sampling import estimate_sampling_gap

def calculate_true_efficiency(metrics_history: List[Dict]) -> Dict:
    """
    Calculate true efficiency using power + burst signals instead of utilization
    """
    if len(metrics_history) < 10:
        return {"error": "Insufficient data", "samples": len(metrics_history)}
    
    # Extract data
    power_series = []
    timestamps = []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            power_series.append(gpu.get('power_draw_watts', 0))
            timestamps.append(m.get('timestamp', 0))
    
    if len(power_series) < 5:
        return {"error": "No valid power data", "samples": len(power_series)}
    
    # Constants
    IDLE_POWER_BASELINE = 70  # Watts (A100 idle baseline)
    MAX_POWER = 400           # Watts (A100 max TDP)
    
    # 1. POWER ACTIVITY RATIO
    avg_power = np.mean(power_series)
    power_activity_ratio = min(avg_power / MAX_POWER, 1.0)
    
    # 2. ACTIVE POWER RATIO (% time power > idle baseline)
    active_power_count = sum(1 for p in power_series if p > IDLE_POWER_BASELINE)
    active_power_ratio = active_power_count / len(power_series)
    
    # 3. BURST DENSITY from Engine 3
    bursts = detect_compute_bursts(metrics_history)
    burst_count = bursts.get("burst_count", 0)
    total_time_seconds = timestamps[-1] - timestamps[0] if len(timestamps) > 1 else len(power_series)
    burst_density = burst_count / max(total_time_seconds, 1)
    burst_density = min(burst_density, 1.0)  # Cap at 1
    
    # 4. CONSISTENCY (power variance penalty)
    power_variance = np.var(power_series)
    normalized_variance = min(power_variance / 10000, 1.0)
    consistency = 1.0 - normalized_variance
    
    # 5. TRUE ACTIVITY SCORE (weighted combination)
    true_activity_score = (
        (power_activity_ratio * 0.40) +
        (active_power_ratio * 0.25) +
        (burst_density * 0.20) +
        (consistency * 0.15)
    )
    true_activity_score = max(0.0, min(1.0, true_activity_score))
    
    # 6. USEFUL COMPUTE TIME (based on power activity)
    useful_compute_ratio = active_power_ratio
    
    # 7. FINAL EFFICIENCY
    efficiency = true_activity_score * useful_compute_ratio * consistency
    efficiency = max(0.0, min(1.0, efficiency))
    
    return {
        "efficiency_score": round(efficiency, 4),
        "efficiency_percentage": round(efficiency * 100, 2),
        "true_activity_score": round(true_activity_score, 4),
        "power_activity_ratio": round(power_activity_ratio, 4),
        "active_power_ratio": round(active_power_ratio, 4),
        "burst_density": round(burst_density, 4),
        "consistency": round(consistency, 4),
        "avg_power_watts": round(avg_power, 1),
        "burst_count": burst_count,
        "samples_analyzed": len(power_series)
    }
