from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"status": "working"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return {"message": "Test app working"}
