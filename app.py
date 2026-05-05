from flask import Flask, request, jsonify
import sqlite3, time

app = Flask(__name__)
DB_NAME = "gpu_optimizer.db"

def get_db():
    return sqlite3.connect(DB_NAME, timeout=10)

@app.route("/api/ingest", methods=["POST"])
def ingest():
    data = request.json
    if not data or "gpus" not in data:
        return jsonify({"error": "invalid payload"}), 400

    tenant_id = data.get("tenant_id", "default")
    timestamp = data.get("timestamp", time.time())
    gpus = data.get("gpus", [])

    with get_db() as conn:
        c = conn.cursor()
        for gpu in gpus:
            c.execute("""
                INSERT INTO gpu_logs (tenant_id, timestamp, gpu_id, model, power_watts, utilization, memory_mb)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                tenant_id, timestamp,
                gpu.get("gpu_id"), gpu.get("model", "unknown"),
                float(gpu.get("power_watts") or 0),
                float(gpu.get("utilization") or 0),
                float(gpu.get("memory_mb") or 0)
            ))
        print(f"[{time.strftime('%H:%M:%S')}] Ingested {len(gpus)} GPUs for {tenant_id}")

    return jsonify({"status": "ok"})

@app.route("/")
def dashboard():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM gpu_logs ORDER BY timestamp DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No data yet"
    latest = rows[0]
    return f"<h2>GPU Optimizer</h2>Utilization: {latest['utilization']:.1f}%<br>Power: {latest['power_watts']:.0f}W"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
