from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

ghost_gauge  = Gauge('gpu_ghost_power_watts',  'Ghost power watts',   ['gpu_id', 'node_id'])
power_gauge  = Gauge('gpu_power_watts',         'GPU power watts',     ['gpu_id', 'node_id'])
util_gauge   = Gauge('gpu_utilization_pct',     'GPU utilization %',   ['gpu_id', 'node_id'])
cei_gauge    = Gauge('gpu_cei_flops_per_joule', 'CEI FLOPs/J',         ['gpu_id', 'node_id'])
desync_gauge = Gauge('gpu_desync_events_total', 'DESYNC events',       ['gpu_id', 'node_id'])

def update_metrics(gpu_id, node_id, power_w, util_pct, cei=0.0, ghost_flag=False, desync_flag=False):
    power_gauge.labels(gpu_id=gpu_id, node_id=node_id).set(power_w)
    util_gauge.labels(gpu_id=gpu_id, node_id=node_id).set(util_pct)
    ghost_gauge.labels(gpu_id=gpu_id, node_id=node_id).set(power_w if ghost_flag else 0)
    if cei > 0: cei_gauge.labels(gpu_id=gpu_id, node_id=node_id).set(cei)
    if desync_flag: desync_gauge.labels(gpu_id=gpu_id, node_id=node_id).inc()

# Add to main.py:
# @app.get("/metrics")
# async def metrics():
#     return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
