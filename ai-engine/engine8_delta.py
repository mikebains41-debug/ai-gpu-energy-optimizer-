# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 8: Efficiency Delta Tracker - Before vs After Workload
"""

from typing import List, Dict

def calculate_efficiency_delta(metrics_history: List[Dict], baseline_sec: int = 60, after_sec: int = 60) -> Dict:
    if len(metrics_history) < baseline_sec + after_sec:
        return {"error": f"Insufficient data. Need {baseline_sec + after_sec} samples, have {len(metrics_history)}"}
    
    baseline, after = metrics_history[:baseline_sec], metrics_history[-after_sec:]
    
    def avg_util(data): utils = [m['gpus'][0].get('utilization_percent', 0) for m in data if m.get('gpus')]; return sum(utils)/len(utils) if utils else 0
    def avg_power(data): powers = [m['gpus'][0].get('power_draw_watts', 0) for m in data if m.get('gpus')]; return sum(powers)/len(powers) if powers else 0
    
    base_util, after_util = avg_util(baseline), avg_util(after)
    base_power, after_power = avg_power(baseline), avg_power(after)
    
    base_eff = base_util / base_power if base_power > 0 else 0
    after_eff = after_util / after_power if after_power > 0 else 0
    delta = after_eff - base_eff
    gain = (delta / base_eff) * 100 if base_eff > 0 else 0
    
    if delta > 0: conclusion = "Workload scaling improved efficiency"
    elif delta < 0: conclusion = "Workload scaling is inefficient - wasting power"
    else: conclusion = "No change in efficiency"
    
    return {
        "efficiency_delta": round(delta, 4),
        "efficiency_gain_percent": round(gain, 2),
        "baseline_efficiency": round(base_eff, 4),
        "after_efficiency": round(after_eff, 4),
        "baseline_util_pct": round(base_util, 1),
        "after_util_pct": round(after_util, 1),
        "conclusion": conclusion
    }
