@app.post("/api/v1/metrics")
async def receive_metrics(
    metrics: ClusterMetrics,
    authorization: Optional[str] = Header(None)
):
    print(f"DEBUG: Request received")
    print(f"DEBUG: Authorization header: {authorization}")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth format. Use Bearer token")
    
    api_key = authorization.replace("Bearer ", "")
    
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    print(f"DEBUG: Cluster ID: {metrics.cluster_id}")
    print(f"DEBUG: Number of GPUs: {len(metrics.gpus)}")
    
    # Save to memory
    if metrics.cluster_id not in metrics_store:
        metrics_store[metrics.cluster_id] = []
    metrics_store[metrics.cluster_id].append(metrics.model_dump())
    
    if len(metrics_store[metrics.cluster_id]) > 500:
        metrics_store[metrics.cluster_id] = metrics_store[metrics.cluster_id][-500:]
    
    print(f"✅ Saved to memory for cluster: {metrics.cluster_id}")
    
    # Try PostgreSQL
    try:
        db = SessionLocal()
        for gpu in metrics.gpus:
            db_metric = GPUMetric(
                cluster=metrics.cluster_id,
                gpu_index=gpu.gpu_id,
                power_draw=gpu.power_draw_watts,
                power_limit=700.0,
                temperature=gpu.temperature_celsius,
                memory_used=gpu.memory_used_gb,
                memory_total=gpu.memory_total_gb,
                gpu_util=gpu.utilization_percent
            )
            db.add(db_metric)
        db.commit()
        print(f"✅ Saved to PostgreSQL for cluster: {metrics.cluster_id}")
    except Exception as e:
        print(f"❌ PostgreSQL error: {e}")
    finally:
        db.close()
    
    return {"status": "ok", "received": True}
