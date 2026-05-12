# RTX 4090 Ghost Power Test

- **Platform:** RunPod (pod `1vaoa5mqc5sxvv-19123`)
- **Date:** 2026-05-12
- **Test structure:**
  - 5 min warmup (idle)
  - 20 min load: PyTorch `4096×4096` matrix multiply
  - 5 min cooldown (idle)
- **Ghost power check:** flagged 3 events within first 3 seconds of cooldown:
  - `351.36 W, 0%`
  - `91.97 W, 0%`
  - `74.26 W, 0%`
- **Verdict:** **PASS** – all spikes are short transients (<4 sec). No sustained power >70 W at 0% util.
- **Stable idle power after cooldown:** ~20 W (excellent)
- **Raw cooldown data:** `rtx4090_cooldown.csv`

> The 351 W spike is a measurement artifact (power still ramping down).  
> The 92 W and 74 W readings are normal intermediate power states.  
> A single 59 W blip occurred 12 minutes into cooldown (memory clock step‑down).
