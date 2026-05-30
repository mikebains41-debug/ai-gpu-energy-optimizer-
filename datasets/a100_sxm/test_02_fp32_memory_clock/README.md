# A100 Test 02 — FP32 Memory Clock
**Researcher:** Mike Bains | mikebains41@gmail.com

## Key Numbers
- Baseline GPU0 = 65.07W | GPU1 = 67.19W
- FP32 peak GPU0 = 360.64W | GPU1 = 360.91W
- SM clock baseline = 210MHz | FP32 load = 1,410MHz
- HBM clock = 1,593MHz locked throughout ALL phases
- util.gpu = 100% during load
- util.memory = 4% (NVML underreporting)
- GPU1 consistently 2W higher than GPU0
