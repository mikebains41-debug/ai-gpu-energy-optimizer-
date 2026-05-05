import sqlite3, time
from fpdf import FPDF

DB_NAME = "gpu_optimizer.db"
price_per_kwh = 0.12

def get_data():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM gpu_logs ORDER BY gpu_id, timestamp")
    rows = c.fetchall()
    conn.close()
    return rows

def generate_report():
    rows = get_data()
    if not rows:
        print("No data")
        return

    # Idle baseline (10th percentile)
    powers = sorted([r["power_watts"] for r in rows])
    idle_baseline = powers[int(len(powers) * 0.1)] if powers else 70

    prev_time = {}
    total_cost = 0
    idle_waste = 0
    idle_count = 0
    total_time = 0

    for r in rows:
        gpu_id = r["gpu_id"]
        ts = r["timestamp"]
        power = r["power_watts"]
        util = r["utilization"]
        mem = r["memory_mb"]

        if gpu_id in prev_time:
            delta = ts - prev_time[gpu_id]
            if delta > 120:
                delta = 30

            effective_power = max(0, power - idle_baseline)
            cost = (effective_power * delta) / 3_600_000 * price_per_kwh

            total_cost += cost
            total_time += delta

            is_idle = (util < 5 and mem < 500)
            if is_idle:
                idle_waste += cost
                idle_count += 1

        prev_time[gpu_id] = ts

    total_minutes = total_time / 60
    idle_pct = (idle_count / len(rows) * 100) if rows else 0
    monthly_waste = idle_waste * (30 * 24 * 60 / total_minutes) if total_minutes > 0 else 0

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="GPU Optimizer Report", ln=True)
    pdf.cell(200, 10, txt=f"Observation window: {total_minutes:.1f} minutes", ln=True)
    pdf.cell(200, 10, txt=f"Idle power baseline: {idle_baseline:.0f}W", ln=True)
    pdf.cell(200, 10, txt=f"Total cost: ${total_cost:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Idle waste: ${idle_waste:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Idle percentage of time: {idle_pct:.1f}%", ln=True)
    pdf.cell(200, 10, txt=f"Estimated monthly waste (projected): ${monthly_waste:.2f}", ln=True)
    pdf.output("report.pdf")
    print("Report saved as report.pdf")

if __name__ == "__main__":
    generate_report()
