"""
AI Optimization Engine for GPU Data Centers
Rule-based decision engine with ML-ready architecture
"""

from datetime import datetime, timedelta
import numpy as np
from typing import List, Optional
from pydantic import BaseModel

class GPUState(BaseModel):
    id: str
    name: str
    location: str
    utilization: float      # 0-100%
    temperature: float      # °C
    power_draw: float       # MW
    renewable_pct: float    # 0-100%
    active_gpus: int
    total_gpus: int

class Recommendation(BaseModel):
    id: str
    type: str               # "power_cap", "workload_shift", "cooling_boost", "consolidation"
    priority: str           # "critical", "high", "medium", "low"
    title: str
    description: str
    estimated_savings_monthly: float  # USD
    auto_apply: bool
    target_gpus: List[str]

class OptimizationEngine:
    def __init__(self):
        self.history: List[GPUState] = []
        self.max_history = 1000
        
    def analyze(self, clusters: List[GPUState], grid_carbon_intensity: float = 0.45) -> List[Recommendation]:
        """
        Main optimization loop. Analyzes state → generates recommendations.
        """
        recommendations = []
        
        for cluster in clusters:
            # Store in history
            self.history.append(cluster)
            if len(self.history) > self.max_history:
                self.history.pop(0)
            
            # 1. THERMAL OPTIMIZATION
            if cluster.temperature > 85:
                recommendations.append(Recommendation(
                    id=f"thermal_crit_{cluster.id}",
                    type="power_cap",
                    priority="critical",
                    title="🚨 Critical Thermal Event",
                    description=f"{cluster.name} at {cluster.temperature}°C. Immediately cap power to 80%.",
                    estimated_savings_monthly=0,
                    auto_apply=True,
                    target_gpus=[cluster.id]
                ))
            elif cluster.temperature > 75:
                savings = (cluster.temperature - 70) * 150
                recommendations.append(Recommendation(
                    id=f"thermal_warn_{cluster.id}",
                    type="cooling_boost",
                    priority="high",
                    title="🟡 Elevated Temperature",
                    description=f"Increase cooling airflow by 15%. Shift non-urgent jobs.",
                    estimated_savings_monthly=savings,
                    auto_apply=False,
                    target_gpus=[cluster.id]
                ))
                
            # 2. POWER EFFICIENCY
            if cluster.utilization < 40 and cluster.active_gpus > 0:
                idle_power = cluster.power_draw * (1 - cluster.utilization/100)
                savings = idle_power * 24 * 30 * 0.12  # 24h, 30 days, $0.12/kWh
                recommendations.append(Recommendation(
                    id=f"power_idle_{cluster.id}",
                    type="consolidation",
                    priority="medium",
                    title="⚡ Low Utilization Detected",
                    description=f"Consolidate workloads and suspend idle GPUs. Savings: ${savings:.0f}/mo",
                    estimated_savings_monthly=savings,
                    auto_apply=False,
                    target_gpus=[cluster.id]
                ))
                
            # 3. CARBON-AWARE SCHEDULING
            if grid_carbon_intensity > 0.6 and cluster.utilization > 70:
                recommendations.append(Recommendation(
                    id=f"carbon_high_{cluster.id}",
                    type="workload_shift",
                    priority="medium",
                    title="🌍 High Grid Carbon Intensity",
                    description="Defer batch training jobs. Switch to battery storage or renewable regions.",
                    estimated_savings_monthly=cluster.power_draw * 0.08 * 24 * 30,
                    auto_apply=False,
                    target_gpus=[cluster.id]
                ))
        
        # 4. CROSS-CLUSTER LOAD BALANCING (if multiple clusters)
        if len(clusters) > 1:
            high_util = [c for c in clusters if c.utilization > 85]
            low_util = [c for c in clusters if c.utilization < 30]
            
            if high_util and low_util:
                recommendations.append(Recommendation(
                    id="cross_cluster_balance",
                    type="workload_shift",
                    priority="high",
                    title="🔄 Cross-Cluster Load Balance",
                    description=f"Shift jobs from {high_util[0].name} ({high_util[0].utilization}%) to {low_util[0].name} ({low_util[0].utilization}%)",
                    estimated_savings_monthly=5000,
                    auto_apply=False,
                    target_gpus=[high_util[0].id, low_util[0].id]
                ))
                
        return recommendations
    
    def get_energy_savings_prediction(self, clusters: List[GPUState]) -> float:
        """Predict potential energy savings based on current state"""
        total_power = sum(c.power_draw for c in clusters)
        
        # Simple prediction model: 15-30% savings based on utilization
        avg_util = np.mean([c.utilization for c in clusters])
        
        if avg_util < 40:
            savings_pct = 0.25  # 25% savings for low utilization
        elif avg_util > 85:
            savings_pct = 0.10  # 10% savings for maxed out
        else:
            savings_pct = 0.18  # 18% savings for normal
        
        return total_power * savings_pct * 24 * 30 * 0.12  # Monthly USD

# Global instance
engine = OptimizationEngine()
# ============================================================
# H100 vs A100 Benchmark Integration (Added for PoP)
# ============================================================

import json
import os
import subprocess
from pathlib import Path

class BenchmarkIntegration:
    """
    Adds GPU performance benchmarking to the Optimization Engine.
    Measures real TFLOPS, memory bandwidth, and FP8 capability.
    """
    
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.benchmark_results = {}
        self.benchmark_file = "pop_results.json"
    
    def run_benchmark(self, gpu_id: str = "all"):
        """
        Run H100_benchmark.py on specified GPU(s)
        """
        print(f"[Benchmark] Running performance test on {gpu_id}")
        
        # Check if benchmark script exists
        script_path = Path(__file__).parent / "H100_benchmark.py"
        if not script_path.exists():
            print("[Benchmark] ERROR: H100_benchmark.py not found in ai-engine/")
            return None
        
        # Run the benchmark
        result = subprocess.run(
            ["python3", str(script_path)],
            capture_output=True,
            text=True
        )
        
        # Load results
        if os.path.exists(self.benchmark_file):
            with open(self.benchmark_file, 'r') as f:
                self.benchmark_results = json.load(f)
            print(f"[Benchmark] Complete: {self.benchmark_results.get('gpu')} - {self.benchmark_results.get('tflops', 0):.1f} TFLOPS")
            return self.benchmark_results
        
        print(f"[Benchmark] Failed: {result.stderr}")
        return None
    
    def get_gpu_capabilities(self) -> dict:
        """
        Return GPU performance data for optimization decisions
        """
        if not self.benchmark_results:
            return {"benchmark_available": False}
        
        gpu_name = self.benchmark_results.get("gpu", "Unknown")
        
        return {
            "benchmark_available": True,
            "gpu_type": "H100" if "H100" in gpu_name else "A100" if "A100" in gpu_name else "Unknown",
            "tflops_fp16": self.benchmark_results.get("tflops", 0),
            "has_native_fp8": "H100" in gpu_name,
            "timestamp": self.benchmark_results.get("timestamp", ""),
            "expected_speedup_vs_other": "3.0x" if "H100" in gpu_name else "baseline"
        }
    
    def enhance_recommendations(self, original_recommendations: list) -> list:
        """
        Add benchmark-aware recommendations to the existing ones
        """
        caps = self.get_gpu_capabilities()
        
        if not caps["benchmark_available"]:
            return original_recommendations
        
        benchmark_recs = []
        
        # Add FP8 recommendation for H100
        if caps["has_native_fp8"]:
            benchmark_recs.append({
                "type": "fp8_optimization",
                "priority": "high",
                "title": "⚡ Enable FP8 Quantization",
                "description": f"H100 detected (TFLOPS: {caps['tflops_fp16']:.1f}). Enable FP8 for 2x inference throughput.",
                "estimated_savings": "2x speed, half energy"
            })
        
        # Add compute vs memory bound guidance
        if caps["tflops_fp16"] < 400 and caps["gpu_type"] == "H100":
            benchmark_recs.append({
                "type": "bottleneck_detected",
                "priority": "medium",
                "title": "⚠️ Performance Below Expectation",
                "description": "H100 TFLOPS lower than expected. Check: CPU data loading, PCIe bandwidth, or batch size.",
                "estimated_savings": "Up to 3x improvement"
            })
        
        return original_recommendations + benchmark_recs


# Attach benchmark to your existing engine
benchmark = BenchmarkIntegration(engine)

# Optional: Run benchmark once on startup
# benchmark.run_benchmark()
