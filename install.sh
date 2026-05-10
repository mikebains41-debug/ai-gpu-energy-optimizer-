#!/bin/bash
# GPU Agent Installer - Proprietary
# Contact: mikebains41@gmail.com

set -e

echo "=== GPU Ghost Power Detector ==="
echo ""

if ! command -v nvidia-smi &> /dev/null; then
    echo "ERROR: No NVIDIA GPU detected"
    exit 1
fi

echo "✓ GPU detected"

echo "Installing dependencies..."
pip install pynvml torch -q

echo "Downloading agent..."
curl -sSL https://raw.githubusercontent.com/mikebains41-debug/ai-gpu-energy-optimizer-/main/gpu_agent.py -o gpu_agent.py

chmod +x gpu_agent.py

echo ""
echo "=== Ready to scan ==="
echo "Run: python3 gpu_agent.py --scan"
