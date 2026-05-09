#!/bin/bash
echo "🔧 Installing GPU Optimizer Agent..."

command -v curl >/dev/null 2>&1 || { echo "❌ Install curl: pkg install curl"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Install python: pkg install python"; exit 1; }

mkdir -p ~/gpu-optimizer
cd ~/gpu-optimizer

echo "📥 Downloading agent..."
curl -sSL https://raw.githubusercontent.com/mikebains41-debug/ai-gpu-energy-optimizer-/main/ai-engine/gpu_monitor_agent.py -o gpu_monitor_agent.py

echo "Enter API Key:"
read API_KEY
echo "Enter Cluster ID:"
read CLUSTER_ID

echo "{\"backend_url\":\"https://ai-gpu-brain-v3.onrender.com\",\"cluster_id\":\"$CLUSTER_ID\",\"api_key\":\"$API_KEY\",\"check_interval_seconds\":2}" > config.json

pip3 install requests --quiet

echo "✅ Done! Starting agent..."
python3 gpu_monitor_agent.py
