# A100 PCIe Mixed Idle-Load Test (no cooldown)

- **Date:** 2026-05-11
- **Duration:** ~10 minutes (first few seconds idle, then load)
- **Idle power:** ~47.3 W at 0% util
- **Load power:** ~292–311 W at 99–100% util
- **Ghost power:** Not assessable (no cooldown phase)
- **File:** `a100_pcie_mixed_load_no_cooldown.csv`

This test shows normal operation: idle power around 47 W, load around 300 W.  
To detect ghost power, a cooldown phase after load is required (see test-02).
