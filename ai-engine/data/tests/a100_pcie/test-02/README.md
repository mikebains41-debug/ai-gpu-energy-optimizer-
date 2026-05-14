# A100 PCIe Ghost Power Test (cooldown after load)

- **Date:** 2026-05-11
- **Cooldown duration:** ~2 hours (7440 seconds)
- **Idle power during cooldown:** starts ~50.5 W, ends ~45.1 W
- **GPU utilization during cooldown:** 0%
- **Maximum power during cooldown:** 50.46 W
- **Ghost power threshold:** 70 W
- **Verdict:** PASS – no power spike above 70 W at 0% util

Power gradually declines from 50 W to 45 W as the GPU enters low-power states.  
This is normal behaviour for A100 PCIe.
