# Test 22 – Persistence Mode Disable Attempt (Different RunPod Instance)

## Purpose
Attempt to disable persistence mode on a different RunPod A100 SXM instance to check consistency with Test 16.

## Environment
- GPU: NVIDIA A100 SXM (RunPod instance `47cdd71daf80`)
- Command: `nvidia-smi -pm 0`
- Verification: `nvidia-smi --query-gpu=persistence_mode` and `nvidia-smi --query-gpu=power.draw,pstate,clocks.current.memory`

## Result
- **Command output:** `Disabled persistence mode for GPU 00000000:87:00.0. All done.`
- **Post‑check persistence mode:** `Enabled` (unchanged)
- **Power, P‑state, memory clock after:** `66.16 W, P0, 1593 MHz`

## Interpretation
The command claimed success, but the setting did not change. The GPU remained in P0 with max memory clock. This is different from Test 16, where the command returned an `Unknown Error`. It suggests that the hypervisor may acknowledge the command but ignore it, or the change is reverted immediately.

## Conclusion
Effective persistence mode disable is not possible on this RunPod instance. Tenants cannot reduce idle power by disabling persistence mode.

## Files
- `screenshot_01.jpg` – terminal output
- `summary.json` – test metadata
- `metrics.json` – observed metrics
- `evidence.json` – raw outputs
- `README.md` – this explanation
