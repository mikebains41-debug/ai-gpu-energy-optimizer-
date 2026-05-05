import sqlite3

DB_NAME = "gpu_optimizer.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS gpu_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT, timestamp REAL, gpu_id TEXT, model TEXT,
            power_watts REAL, utilization REAL, memory_mb REAL
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_gpu_time ON gpu_logs(gpu_id, timestamp);")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
