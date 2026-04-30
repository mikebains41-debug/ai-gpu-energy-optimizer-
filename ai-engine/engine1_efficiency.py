# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 1: True Efficiency Calculator
Formula: (useful_time/total_time) × (avg_util/avg_power) × consistency
"""

import numpy as np
from typing import List, Dict

def calculate_true_efficiency(metrics_history: List[Dict]) -> Dict:
    if len(metrics_history) < 2:
        return {"error": "Insufficient data", "samples": len(metrics_history)}
    
    util_series, power_series, timestamps = [], [], []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            util_series.append(gpu.get('utilization_percent', 0))
            power_series.append(gpu.get('power_draw_watts', 0))
            timestamps.append(m.get('timestamp', 0))
    
    if len(util_series) < 2:
        return {"error": "No valid GPU data"}
    
    total_time = timestamps[-1] - timestamps[0] if timestamps[-1] > timestamps[0] else len(util_series)
    useful_compute_time = sum(1 for u in util_series if u > 5)
    avg_util = np.mean(util_series) / 100.0
    avg_power = max(np.mean(power_series), 1.0)
    util_variance = np.var(util_series)
    normalized_variance = min(util_variance / 100.0, 1.0)
    consistency = 1.0 - normalized_variance
    
    efficiency = (useful_compute_time / total_time) * (avg_util / avg_power) * consistency
    efficiency = max(0.0, min(1.0, efficiency))
    
    return {
        "efficiency_score": round(efficiency, 4),
        "efficiency_percentage": round(efficiency * 100, 2),
        "useful_compute_ratio": round(useful_compute_time / total_time, 4),
        "consistency": round(consistency, 4),
        "samples_analyzed": len(util_series)
    }
