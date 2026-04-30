# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 6: Dataset Export - CSV + JSON
"""

from typing import List, Dict
from datetime import datetime

def export_dataset(metrics_history: List[Dict], format: str = "json") -> Dict:
    if not metrics_history:
        return {"error": "No data to export"}
    
    metadata = {
        "export_date": datetime.now().isoformat(),
        "samples": len(metrics_history),
        "sampling_rate_hz": 1,
        "gpu_type": "A100/H100"
    }
    
    if format == "json":
        return {"metadata": metadata, "data": metrics_history}
    
    rows = []
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            rows.append({
                "timestamp": m.get('timestamp'),
                "utilization": gpu.get('utilization_percent'),
                "power_w": gpu.get('power_draw_watts'),
                "temperature": gpu.get('temperature_celsius')
            })
    
    return {"format": "csv", "rows": rows, "metadata": metadata, "row_count": len(rows)}
