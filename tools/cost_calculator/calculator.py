#!/usr/bin/env python3
"""
GPU Energy Cost Calculator
Accounts for ghost power waste — the only calculator that does.
Author: Manmohan Bains
"""

GPU_PROFILES = {
    "A100_SXM": {"idle_w": 67, "ghost_w": 146.66, "peak_w": 400, "cei_flops_j": 5.68e9},
    "H100_SXM": {"idle_w": 70, "ghost_w": 0, "peak_w": 412, "cei_flops_j": 8.24e9},
    "A40":      {"idle_w": 30, "ghost_w": 0, "peak_w": 300, "cei_flops_j": 3.2e9},
    "T4":       {"idle_w": 10, "ghost_w": 0, "peak_w": 70,  "cei_flops_j": 1.1e9},
}

COST_PER_KWH = 0.10

def calculate(gpu_type, num_gpus, active_hours_per_day):
    g = GPU_PROFILES.get(gpu_type)
    if not g:
        print(f"Unknown GPU. Options: {list(GPU_PROFILES.keys())}")
        return

    idle_hours = 24 - active_hours_per_day
    ghost_w = g["ghost_w"]
    idle_w = g["idle_w"]
    peak_w = g["peak_w"]

    # Daily energy per GPU (kWh)
    active_kwh = (peak_w * active_hours_per_day) / 1000
    idle_kwh   = (idle_w * idle_hours) / 1000
    ghost_kwh  = (ghost_w * idle_hours) / 1000

    # Without ghost awareness
    reported_kwh = active_kwh + idle_kwh
    # With ghost power included
    true_kwh = active_kwh + ghost_kwh

    waste_kwh = (ghost_kwh - idle_kwh) * num_gpus
    waste_cost_day = waste_kwh * COST_PER_KWH
    waste_cost_month = waste_cost_day * 30
    waste_cost_year = waste_cost_day * 365

    print(f"\n{'='*55}")
    print(f"  GPU Energy Cost Calculator — {gpu_type} x{num_gpus}")
    print(f"{'='*55}")
    print(f"  Active hours/day:     {active_hours_per_day}h")
    print(f"  Idle hours/day:       {idle_hours}h")
    print(f"  Ghost power:          {ghost_w}W")
    print(f"  True idle power:      {idle_w}W")
    print(f"  Hidden waste/GPU/day: {(ghost_kwh - idle_kwh):.3f} kWh")
    print(f"{'='*55}")
    print(f"  FLEET GHOST WASTE:")
    print(f"  Per day:   ${waste_cost_day:.2f}")
    print(f"  Per month: ${waste_cost_month:.2f}")
    print(f"  Per year:  ${waste_cost_year:.2f}")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    calculate("A100_SXM", num_gpus=500, active_hours_per_day=12)
    calculate("H100_SXM", num_gpus=500, active_hours_per_day=12)
