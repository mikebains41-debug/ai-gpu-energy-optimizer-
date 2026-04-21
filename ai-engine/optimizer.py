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
