# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 3: Burst Detection - Detects micro-bursts missed by 1Hz sampling
"""

from typing import List, Dict

def detect_compute_bursts(metrics_history: List[Dict]) -> Dict:
    if len(metrics_history) < 10:
        return {"error": "Insufficient data", "burst_count": 0}
    
    power_series, util_series = [], []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            power_series.append(gpu.get('power_draw_watts', 0))
            util_series.append(gpu.get('utilization_percent', 0))
    
    bursts, confidence = [], {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for i in range(1, len(power_series)):
        power_delta = power_series[i] - power_series[i-1]
        util_delta = abs(util_series[i] - util_series[i-1])
        
        if power_delta > 50 and util_delta < 5:
            if power_delta > 100:
                conf = "HIGH"
            elif power_delta > 50:
                conf = "MEDIUM"
            else:
                conf = "LOW"
            confidence[conf] += 1
            bursts.append({"power_delta_w": round(power_delta, 1), "confidence": conf})
    
    minutes = len(metrics_history) / 60
    bursts_per_min = len(bursts) / minutes if minutes > 0 else 0
    
    return {
        "burst_count": len(bursts),
        "bursts_per_minute": round(bursts_per_min, 2),
        "peak_power_watts": round(max(power_series), 1) if power_series else 0,
        "confidence": confidence,
        "recent_bursts": bursts[-5:] if bursts else []
    }
