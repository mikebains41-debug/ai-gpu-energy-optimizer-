# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 7: Power State Analyzer - Detects high residency states
"""

from typing import List, Dict

def detect_power_state(metrics_history: List[Dict]) -> Dict:
    if len(metrics_history) < 10:
        return {"error": "Insufficient data"}
    
    low_util_high_power = 0
    for m in metrics_history[-60:]:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            if gpu.get('utilization_percent', 0) < 1 and gpu.get('power_draw_watts', 0) > 80:
                low_util_high_power += 1
    
    if low_util_high_power > 30:
        return {"power_state": "HIGH_RESIDENCY_STATE", "severity": "INFO", "message": "GPU in high-power residency state (normal datacenter behavior)", "samples": low_util_high_power}
    elif low_util_high_power > 10:
        return {"power_state": "INTERMITTENT_HIGH_POWER", "severity": "LOW", "message": "GPU shows intermittent high power at low utilization", "samples": low_util_high_power}
    else:
        return {"power_state": "NORMAL", "severity": "OK", "message": "GPU power state normal", "samples": low_util_high_power}
