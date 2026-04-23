@app.post("/api/v1/metrics")
async def receive_metrics(
    metrics: ClusterMetrics,
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth format. Use Bearer token")
    
    api_key = authorization.replace("Bearer ", "")
    
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Save to PostgreSQL database
    db = SessionLocal()
    try:
        for gpu in metrics.gpus:
            db_metric = GPUMetric(
                cluster=metrics.cluster_id,
                gpu_index=gpu.gpu_id,
                power_draw=gpu.power_draw_watts,
                power_limit=700.0,  # Max power for H100
                temperature=gpu.temperature_celsius,
                memory_used=gpu.memory_used_gb,
                memory_total=gpu.memory_total_gb,
                gpu_util=gpu.utilization_percent
            )
            db.add(db_metric)
        
        # Also save to in-memory store for /metrics endpoint
        if metrics.cluster_id not in metrics_store:
            metrics_store[metrics.cluster_id] = []
        metrics_store[metrics.cluster_id].append(metrics.model_dump())
        
        if len(metrics_store[metrics.cluster_id]) > 500:
            metrics_store[metrics.cluster_id] = metrics_store[metrics.cluster_id][-500:]
        
        db.commit()
        print(f"✅ Saved {len(metrics.gpus)} GPUs to PostgreSQL for cluster: {metrics.cluster_id}")
    finally:
        db.close()
    
    return {"status": "ok", "received": True}
