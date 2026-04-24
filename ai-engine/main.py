@app.get("/optimize")
def get_optimization():
    # If we have stored metrics, return the latest one for each cluster
    if metrics_store:
        # Convert stored metrics into the format the frontend expects
        clusters = []
        for cluster_id, measurements in metrics_store.items():
            if measurements:
                latest = measurements[-1]
                # Extract gpu metrics (assuming at least one GPU)
                gpu_data = latest.get("gpus", [{}])[0]
                clusters.append({
                    "id": cluster_id,
                    "name": cluster_id.upper().replace("-", " "),
                    "location": "Unknown",
                    "gpu_utilization": gpu_data.get("utilization_percent", 0),
                    "memory_usage": gpu_data.get("memory_used_gb", 0),
                    "temperature": gpu_data.get("temperature_celsius", 0),
                    "power_draw": gpu_data.get("power_draw_watts", 0) / 1000,  # convert W to kW
                    "efficiency_score": 90 + (gpu_data.get("utilization_percent", 0) / 10),
                    "active_gpus": 1,   # you can improve later
                    "total_gpus": 1,
                    "renewable_pct": 50
                })
        return {
            "clusters": clusters,
            "recommendations": [],  # or generate some based on real data
            "total_power_mw": sum(c.get("power_draw", 0) for c in clusters),
            "grid_carbon_intensity": 0.45
        }
    else:
        # fallback to mock data if no real metrics yet
        return generate_realistic_metrics()
