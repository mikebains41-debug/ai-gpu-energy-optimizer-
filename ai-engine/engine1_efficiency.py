# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.

"""
ENGINE 1: True Efficiency Model (Compute-First)
Uses kernel timing + FLOPs + power draw, NOT NVML utilization
"""

import math
from typing import List, Dict

MATRIX_SIZE = 4096  # matches torch workload

def estimate_flops(n: int) -> float:
    """FLOPs for matrix multiplication of n x n"""
    return 2 * (n ** 3)

class Engine1:
    def __init__(self):
        self.samples = []

    def add_sample(self, kernel_ms: float, power_watts: float):
        flops = estimate_flops(MATRIX_SIZE)
        seconds = kernel_ms / 1000.0

        if seconds <= 0 or power_watts <= 0:
            return None

        flops_per_sec = flops / seconds
        efficiency = flops_per_sec / power_watts  # FLOPs per watt

        self.samples.append({
            "flops_per_sec": flops_per_sec,
            "power": power_watts,
            "efficiency": efficiency
        })
        return efficiency

    def compute_consistency(self) -> float:
        if len(self.samples) < 3:
            return 0.0

        effs = [s["efficiency"] for s in self.samples]
        mean = sum(effs) / len(effs)
        variance = sum((x - mean) ** 2 for x in effs) / len(effs)
        std = math.sqrt(variance)

        consistency = 1 / (1 + std / (mean + 1e-9))
        return max(0.0, min(1.0, consistency))

    def compute_score(self) -> Dict:
        if not self.samples:
            return {
                "efficiency_score": 0.0,
                "efficiency_percentage": 0.0,
                "useful_compute_ratio": 0.0,
                "consistency": 0.0,
                "samples_analyzed": 0
            }

        avg_eff = sum(s["efficiency"] for s in self.samples) / len(self.samples)
        consistency = self.compute_consistency()

        normalized = math.log10(avg_eff + 1)
        efficiency_score = normalized * consistency
        efficiency_percentage = min(100.0, efficiency_score * 10)

        return {
            "efficiency_score": round(efficiency_score, 6),
            "efficiency_percentage": round(efficiency_percentage, 4),
            "useful_compute_ratio": round(consistency, 4),
            "consistency": round(consistency, 4),
            "samples_analyzed": len(self.samples)
        }

# Global instance for API compatibility
_engine = Engine1()

def calculate_true_efficiency(metrics_history: List[Dict]) -> Dict:
    """
    API-compatible wrapper for Engine 1
    Expects metrics_history with kernel_ms and power_draw_watts
    """
    global _engine
    _engine = Engine1()  # Reset for each call
    
    for m in metrics_history:
        if m.get('gpus') and len(m['gpus']) > 0:
            gpu = m['gpus'][0]
            kernel_ms = gpu.get('kernel_time_ms', 0)
            power = gpu.get('power_draw_watts', 0)
            if kernel_ms > 0 and power > 0:
                _engine.add_sample(kernel_ms, power)
    
    return _engine.compute_score()
