# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 2: Idle Detection + Cost Waste
"""

from typing import List, Dict

def calculate_idle_waste(metrics_history: List[Dict], cost_per_hour: float = 3.50) -> Dict:
    if len(metrics_history) < 10:
        return {"error": "Insufficient data", "samples": len(metrics_history)}
    
    util_series, power_series = [], []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            util_series.append(gpu.get('utilization_percent', 0))
            power_series.append(gpu.get('power_draw_watts', 0))
    
    idle_periods, current_start = [], None
    for i, u in enumerate(util_series):
        if u < 5 and current_start is None:
            current_start = i
        elif u >= 5 and current_start is not None:
            duration = i - current_start
            if duration >= 2:
                idle_periods.append(duration)
            current_start = None
    
    total_idle = sum(idle_periods)
    total_time = len(util_series)
    idle_pct = (total_idle / total_time) * 100
    cost_waste = total_idle * (cost_per_hour / 3600)
    false_idle = sum(1 for u, p in zip(util_series, power_series) if u < 5 and p > 120)
    
    if idle_pct > 30:
        rec = f"GPU idle {idle_pct:.1f}% → reduce instances"
    elif idle_pct > 15:
        rec = f"GPU idle {idle_pct:.1f}% → consolidate workloads"
    else:
        rec = "Idle within acceptable range"
    
    return {
        "idle_percentage": round(idle_pct, 2),
        "total_idle_seconds": total_idle,
        "idle_periods": len(idle_periods),
        "cost_waste_usd": round(cost_waste, 4),
        "false_idle_detections": false_idle,
        "recommendation": rec
    }
