# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.
# Contact: Mikebains41@gmail.com
# Unauthorized use prohibited.

"""
GPU Metrics Simulator - For testing without real NVIDIA GPUs
Generates realistic GPU telemetry data for development and demo
"""

import random
import time
import json
import sys
from datetime import datetime
from typing import List, Dict, Any

# Try to import optimizer, but don't fail if not available
try:
    from optimizer import GPUState, OptimizationEngine, Recommendation
    HAS_OPTIMIZER = True
except ImportError:
    HAS_OPTIMIZER = False
    print("⚠️ optimizer.py not found. Running in standalone mode.")

class GPUMetricsSimulator:
    """Simulates GPU metrics for testing without real hardware"""
    
    def __init__(self, num_gpus: int = 2):
        self.num_gpus = num_gpus
        self.base_utilization = [75.0] * num_gpus
        self.base_temperature = [70.0] * num_gpus
        self.base_power = [250.0] * num_gpus
        
    def generate_cluster_metrics(self) -> tuple:
        """
        Simulates real-time DCGM/BMS telemetry.
        Returns: (List[GPUState], grid_carbon_intensity)
        """
        clusters = []
        
        # Simulate NVIDIA H100 Cluster (US-West)
        h100_util = max(30, min(98, self.base_utilization[0] + random.uniform(-5, 5)))
        h100_temp = max(55, min(88, self.base_temperature[0] + random.uniform(-2, 3)))
        h100_power = max(1.0, min(2.5, self.base_power[0] / 1000 + random.uniform(-0.1, 0.2)))
        
        # Update base for next iteration (simulate trending)
        self.base_utilization[0] = h100_util
        self.base_temperature[0] = h100_temp
        self.base_power[0] = h100_power * 1000
        
        if HAS_OPTIMIZER:
            h100 = GPUState(
                id="h100-west",
                name="NVIDIA H100 Cluster",
                location="US-West",
                utilization=round(h100_util, 1),
                temperature=round(h100_temp, 1),
                power_draw=round(h100_power, 2),
                renewable_pct=round(random.uniform(60, 75), 1),
                active_gpus=random.randint(240, 256),
                total_gpus=256
            )
            
            # Simulate NVIDIA A100 Cluster (US-East)
            a100_util = max(30, min(98, self.base_utilization[1] + random.uniform(-8, 6)))
            a100_temp = max(60, min(85, self.base_temperature[1] + random.uniform(-1, 2)))
            a100_power = max(0.6, min(1.4, self.base_power[1] / 1000 + random.uniform(-0.05, 0.1)))
            
            self.base_utilization[1] = a100_util
            self.base_temperature[1] = a100_temp
            self.base_power[1] = a100_power * 1000
            
            a100 = GPUState(
                id="a100-east",
                name="NVIDIA A100 Cluster",
                location="US-East",
                utilization=round(a100_util, 1),
                temperature=round(a100_temp, 1),
                power_draw=round(a100_power, 2),
                renewable_pct=round(random.uniform(40, 55), 1),
                active_gpus=random.randint(100, 128),
                total_gpus=128
            )
            
            clusters = [h100, a100]
        else:
            # Fallback to dictionary format if optimizer not available
            clusters = [
                {
                    "id": "h100-west",
                    "name": "NVIDIA H100 Cluster",
                    "location": "US-West",
                    "utilization": round(h100_util, 1),
                    "temperature": round(h100_temp, 1),
                    "power_draw": round(h100_power, 2),
                    "renewable_pct": round(random.uniform(60, 75), 1),
                    "active_gpus": random.randint(240, 256),
                    "total_gpus": 256
                },
                {
                    "id": "a100-east",
                    "name": "NVIDIA A100 Cluster",
                    "location": "US-East",
                    "utilization": round(a100_util, 1),
                    "temperature": round(a100_temp, 1),
                    "power_draw": round(a100_power, 2),
                    "renewable_pct": round(random.uniform(40, 55), 1),
                    "active_gpus": random.randint(100, 128),
                    "total_gpus": 128
                }
            ]
        
        # Grid carbon intensity (0.0 = 100% renewable, 1.0 = 100% fossil)
        grid_carbon_intensity = round(random.uniform(0.3, 0.7), 3)
        
        return clusters, grid_carbon_intensity
    
    def generate_recommendations(self, clusters, grid_carbon_intensity: float = 0.45) -> List[Dict]:
        """Generate optimization recommendations based on current metrics"""
        recommendations = []
        
        for cluster in clusters:
            # Handle both GPUState objects and dicts
            if hasattr(cluster, 'temperature'):
                temp = cluster.temperature
                util = cluster.utilization
                name = cluster.name
                cluster_id = cluster.id
            else:
                temp = cluster.get('temperature', 70)
                util = cluster.get('utilization', 70)
                name = cluster.get('name', 'Unknown')
                cluster_id = cluster.get('id', 'unknown')
            
            # Thermal recommendations
            if temp > 85:
                recommendations.append({
                    "id": f"thermal_crit_{cluster_id}",
                    "cluster_id": cluster_id,
                    "action": "🔥 CRITICAL: Cap power immediately",
                    "estimated_savings_monthly": 0,
                    "priority": "critical"
                })
            elif temp > 75:
                recommendations.append({
                    "id": f"thermal_warn_{cluster_id}",
                    "cluster_id": cluster_id,
                    "action": "🟡 Increase cooling airflow",
                    "estimated_savings_monthly": round((temp - 70) * 150, 0),
                    "priority": "high"
                })
            
            # Low utilization recommendations
            if util < 40:
                savings = round((100 - util) / 100 * 5000, 0)
                recommendations.append({
                    "id": f"low_util_{cluster_id}",
                    "cluster_id": cluster_id,
                    "action": "⚡ Consolidate idle GPUs",
                    "estimated_savings_monthly": savings,
                    "priority": "medium"
                })
        
        return recommendations
    
    def generate_full_metrics(self) -> Dict[str, Any]:
        """Generate complete metrics payload for API response"""
        clusters, carbon = self.generate_cluster_metrics()
        
        if HAS_OPTIMIZER and clusters and isinstance(clusters[0], GPUState):
            engine = OptimizationEngine()
            recommendations = engine.analyze(clusters, carbon)
            recs_list = [rec.dict() for rec in recommendations]
        else:
            recs_list = self.generate_recommendations(clusters, carbon)
        
        total_power = sum(c.power_draw if hasattr(c, 'power_draw') else c.get('power_draw', 0) for c in clusters)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "clusters": [c.dict() if hasattr(c, 'dict') else c for c in clusters],
            "recommendations": recs_list,
            "total_power_mw": round(total_power, 2),
            "grid_carbon_intensity": carbon
        }

def run_simulation(interval_seconds: int = 2):
    """Run continuous simulation for testing"""
    simulator = GPUMetricsSimulator()
    print(f"🚀 Starting GPU Metrics Simulator")
    print(f"   Generating mock data every {interval_seconds} seconds")
    print("   Press Ctrl+C to stop\n")
    
    try:
        while True:
            metrics = simulator.generate_full_metrics()
            print(f"[{metrics['timestamp'][11:19]}] "
                  f"Power: {metrics['total_power_mw']}MW | "
                  f"Recommendations: {len(metrics['recommendations'])}")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n👋 Simulator stopped")

if __name__ == "__main__":
    run_simulation()
