# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 8: Execution Delta Tracker (FIXED)
Tracks before/after GPU state changes
"""

import torch
import pynvml
from typing import List, Dict

def calculate_efficiency_delta(metrics_history: List[Dict], baseline_sec: int = 60, after_sec: int = 60) -> Dict:
    """
    Compare GPU state before and after kernel execution
    """
    if not torch.cuda.is_available():
        return {"error": "CUDA not available"}
    
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        
        # Capture before state
        before_util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        
        # Run a test kernel
        x = torch.randn(4096, 4096, device="cuda")
        y = torch.randn(4096, 4096, device="cuda")
        
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        
        start.record()
        z = torch.matmul(x, y)
        end.record()
        
        torch.cuda.synchronize()
        
        # Capture after state
        after_util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        
        delta = after_util - before_util
        kernel_ms = start.elapsed_time(end)
        
        if delta > 0:
            conclusion = "GPU utilization increased - kernel executed successfully"
        elif delta == 0:
            conclusion = "No change - kernel may be too small or GPU busy"
        else:
            conclusion = "Utilization decreased - unexpected"
        
        return {
            "efficiency_delta": float(delta),
            "efficiency_gain_percent": round((delta / max(before_util, 1)) * 100, 2),
            "baseline_util_pct": before_util,
            "after_util_pct": after_util,
            "kernel_time_ms": round(kernel_ms, 2),
            "conclusion": conclusion
        }
        
    except Exception as e:
        return {"error": str(e)}
