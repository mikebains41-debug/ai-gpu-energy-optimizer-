# Test 25 - VRAM Baseline
**Date:** 2026-05-29 | **GPU:** A100 SXM x2 | **Pod:** ff9ab4afab02 | **Platform:** RunPod container

## Result: PASS

## Memory State
| Metric | GPU0 | GPU1 |
|---|---|---|
| memory.used | 0 MB | 0 MB |
| memory.free | 81,154 MB | 81,154 MB |
| memory.total | 81,920 MB | 81,920 MB |
| driver reservation | 766 MB | 766 MB |
| util.memory | 0% | 0% |

## Ghost Power Active With Zero VRAM
| GPU | Power |
|---|---|
| GPU0 | 65.84W |
| GPU1 | 64.32W |

## Coordinated Burst 22:45:13
| | Before | Burst |
|---|---|---|
| GPU0 | 65.84W | 86.31W |
| GPU1 | 64.65W | 84.62W |
| VRAM | 0 MB | 0 MB |

## Conclusion
Ghost power is NOT VRAM-content-driven. HBM clock locked 1593MHz 24/7. Active with nothing to move. 57 tests. 7 architectures. SXM = ghost power. PCIe = clean.
