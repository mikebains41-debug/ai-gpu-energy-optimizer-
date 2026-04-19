import random
import time
from datetime import datetime
from optimizer import GPUState

def generate_cluster_metrics() -> tuple[list[GPUState], float]:
    """
    Simulates real-time DCGM/BMS telemetry.
    Replace with actual API calls to NVIDIA DCGM or Prometheus later.
    """
    base_time = datetime.now()
    
    # NVIDIA H100 Cluster (US-West)
    h100 = GPUState(
        id="h100-west",
        name="NVIDIA H100 Cluster",
        location="US-West",
        utilization=random.uniform(85, 98),
        temperature=random.uniform(68, 76),
        power_draw=random.uniform(1.7, 2.1),  # MW
        renewable_pct=random.uniform(60, 75),
        active_gpus=243,
        total_gpus=256
    )
    
    # NVIDIA A100 Cluster (US-East)
    a100 = GPUState(
        id="a100-east",
        name="NVIDIA A100 Cluster",
        location="US-East",
        utilization=random.uniform(80, 95),
        temperature=random.uniform(74, 82),
        power_draw=random.uniform(0.85, 1.05),  # MW
        renewable_pct=random.uniform(40, 55),
        active_gpus=115,
        total_gpus=128
    )
    
    # Grid carbon intensity (0.0 = 100% renewable, 1.0 = 100% fossil)
    grid_carbon_intensity = random.uniform(0.3, 0.7)
    
    return [h100, a100], grid_carbon_intensity
