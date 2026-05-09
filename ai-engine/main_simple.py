from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

app = FastAPI(title="GPU Optimizer API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_store = []

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
def get_metrics():
    return metrics_store

@app.post("/api/v1/metrics")
async def ingest_metrics(metrics: dict):
    metrics_store.append(metrics)
    if len(metrics_store) > 10000:
        metrics_store.pop(0)
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "GPU Optimizer API", "version": "3.0.0"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
