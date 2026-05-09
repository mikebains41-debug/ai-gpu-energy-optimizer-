#!/bin/bash
# AI GPU Energy Optimizer - One-line Installer

set -e

echo "🔧 Installing GPU Optimizer Agent..."
echo ""

# Check requirements
command -v curl >/dev/null 2>&1 || { echo "❌ curl required. Install: pkg install curl"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 required. Install: pkg install python"; exit 1; }

# Create directory
mkdir -p ~/gpu-optimizer
cd ~/gpu-optimizer

# Download agent
echo "📥 Downloading agent..."
curl -sSL https://raw.githubusercontent.com/mikebains41-debug/ai-gpu-energy-optimizer-/main/ai-engine/gpu_monitor_agent.py -o gpu_monitor_agent.py

# Get credentials
echo ""
echo "📝 Enter your credentials (from email: mikebains41@gmail.com)"
read -p "API Key: " API_KEY
read -p "Cluster ID: " CLUSTER_ID

# Create config
cat > config.json << EOF
{
    "backend_url": "https://ai-gpu-brain-v3.onrender.com",
    "cluster_id": "$CLUSTER_ID",
    "api_key": "$API_KEY",
    "check_interval_seconds": 2
}
