from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(
    title="AI GPU Energy Optimizer",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data/tests")

def load_test(gpu, test_id):
    path = os.path.join(DATA_DIR, gpu, test_id, "summary.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def load_all_tests(gpu):
    gpu_dir = os.path.join(DATA_DIR, gpu)
    results = []
    if os.path.exists(gpu_dir):
        for test_id in sorted(os.listdir(gpu_dir)):
            data = load_test(gpu, test_id)
            if data:
                results.append({"test_id": test_id, **data})
    return results

@app.get("/")
def root():
    return {"status": "ok", "service": "ai-gpu-brain-v3", "version": "3.0.0"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-gpu-brain-v3", "engines": 8}

@app.get("/results/a100")
def get_a100_results():
    return load_all_tests("a100")

@app.get("/results/h100")
def get_h100_results():
    return load_all_tests("h100")

@app.get("/results/a100/{test_id}")
def get_a100_test_result(test_id: str):
    return load_test("a100", test_id) or {"error": "Not found"}

@app.get("/results/h100/{test_id}")
def get_h100_test_result(test_id: str):
    return load_test("h100", test_id) or {"error": "Not found"}

@app.get("/metrics")
def get_metrics():
    return {"a100": load_all_tests("a100"), "h100": load_all_tests("h100")}

@app.get("/metrics/a100")
def get_a100_metrics():
    return load_all_tests("a100")

@app.get("/metrics/h100")
def get_h100_metrics():
    return load_all_tests("h100")

@app.get("/standards/cei")
def get_cei_standard():
    return {
        "metric": "CEI",
        "name": "Compute Energy Intensity",
        "formula": "Total FLOPs / Total Joules",
        "unit": "FLOPs/J",
        "reference": "https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-"
    }

@app.get("/standards")
def list_standards():
    return [{"metric": "CEI", "description": "Compute Energy Intensity — FLOPs per Joule"}]

@app.get("/compare/gpu")
def compare_gpu():
    return {
        "a100": load_all_tests("a100"),
        "h100": load_all_tests("h100")
    }

@app.get("/compare/precision")
def compare_precision():
    return {"description": "FP32 vs FP16 comparison", "data": load_all_tests("a100")}

@app.get("/compare")
def list_comparisons():
    return ["gpu", "precision", "workload", "matrix_size"]
