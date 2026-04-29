# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.
# Contact: Mikebains41@gmail.com
# Unauthorized use prohibited.

#!/usr/bin/env python3
import kopf
import requests
import os

GPU_OPTIMIZER_URL = os.environ.get("GPU_OPTIMIZER_URL", "http://localhost:10000")

@kopf.on.create('energy.gpu-optimizer.io', 'v1', 'powercaps')
def apply_power_cap(spec, **kwargs):
    gpu_id = spec.get('gpu_id')
    power_limit = spec.get('power_limit_watts')
    workload = spec.get('workload_type', 'inference')
    
    resp = requests.post(
        f"{GPU_OPTIMIZER_URL}/k8s/power-cap",
        params={"gpu_id": gpu_id, "power_limit_watts": power_limit, "workload_type": workload}
    )
    
    if resp.status_code == 200:
        return {"message": f"Power cap {power_limit}W applied to GPU {gpu_id}"}
    else:
        raise kopf.PermanentError(f"Failed: {resp.text}")

@kopf.on.delete('energy.gpu-optimizer.io', 'v1', 'powercaps')
def remove_power_cap(spec, **kwargs):
    gpu_id = spec.get('gpu_id')
    # Reset power cap to default (250W)
    requests.post(f"{GPU_OPTIMIZER_URL}/k8s/power-cap", params={"gpu_id": gpu_id, "power_limit_watts": 250})
    return {"message": f"Power cap removed from GPU {gpu_id}"}
