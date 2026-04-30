# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 5: Alert System - Thermal + Power + Idle
"""

from typing import List, Dict
import time

_last_alert = {}

def evaluate_alerts(metrics_history: List[Dict], cooldown: int = 300) -> Dict:
    if not metrics_history:
        return {"alerts": []}
    
    latest = metrics_history[-1]
    if not latest.get('gpus') or len(latest['gpus']) == 0:
        return {"alerts": []}
    
    gpu = latest['gpus'][0]
    temp = gpu.get('temperature_celsius', 0)
    util = gpu.get('utilization_percent', 0)
    cluster = latest.get('cluster_id', 'unknown')
    
    alerts, now = [], time.time()
    
    if temp > 85:
        key = f"{cluster}_temp_crit"
        if key not in _last_alert or (now - _last_alert[key]) > cooldown:
            alerts.append({"type": "TEMPERATURE", "severity": "CRITICAL", "value": temp, "message": f"GPU at {temp}°C - immediate action"})
            _last_alert[key] = now
    elif temp > 75:
        key = f"{cluster}_temp_warn"
        if key not in _last_alert or (now - _last_alert[key]) > cooldown:
            alerts.append({"type": "TEMPERATURE", "severity": "WARNING", "value": temp, "message": f"GPU at {temp}°C - reduce workload"})
            _last_alert[key] = now
    
    if util < 10:
        key = f"{cluster}_idle"
        if key not in _last_alert or (now - _last_alert[key]) > cooldown:
            alerts.append({"type": "IDLE", "severity": "INFO", "value": util, "message": f"GPU at {util}% utilization - potential waste"})
            _last_alert[key] = now
    
    return {"alert_count": len(alerts), "alerts": alerts}
