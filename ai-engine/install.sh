#!/bin/bash
# AI GPU Energy Optimizer - One-Click Installer
# Run as: curl -sSL https://raw.githubusercontent.com/mikebains41-debug/ai-gpu-energy-optimizer-/main/ai-engine/install.sh | bash

set -e

echo "🚀 Installing AI GPU Energy Optimizer Agent..."

INSTALL_DIR="$HOME/gpu-optimizer"
REPO="mikebains41-debug/ai-gpu-energy-optimizer-"
BRANCH="main"
SUBDIR="ai-engine"

# 1. Create directory
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# 2. Download files from GitHub
echo "⬇️  Downloading agent files..."
curl -sSL "https://raw.githubusercontent.com/$REPO/$BRANCH/$SUBDIR/gpu_monitor_agent.py" -o gpu_monitor_agent.py
curl -sSL "https://raw.githubusercontent.com/$REPO/$BRANCH/$SUBDIR/agent_requirements.txt" -o agent_requirements.txt

# 3. Prompt for credentials
echo ""
echo "⚙️  Enter your beta credentials:"
read -p "Cluster ID: " CLUSTER_ID
read -p "API Key: " API_KEY
read -p "Backend URL (press Enter for default): " BACKEND_URL
BACKEND_URL="${BACKEND_URL:-https://ai-gpu-brain-v2.onrender.com}"

# 4. Create config file
cat > config.json << EOF
{
  "backend_url": "$BACKEND_URL",
  "cluster_id": "$CLUSTER_ID",
  "api_key": "$API_KEY",
  "check_interval_seconds": 2
}
EOF

# 5. Install dependencies
echo "📦 Installing Python dependencies..."
python3 -m venv venv || { echo "❌ Python 3 required. Install it and try again."; exit 1; }
source venv/bin/activate
pip install --quiet -r agent_requirements.txt

# 6. Create systemd service (Linux)
if command -v systemctl &> /dev/null; then
  echo "🔧 Setting up auto-start service..."
  sudo tee /etc/systemd/system/gpu-optimizer.service > /dev/null << EOF
[Unit]
Description=AI GPU Energy Optimizer Agent
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/gpu_monitor_agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
  sudo systemctl daemon-reload
  sudo systemctl enable --now gpu-optimizer
  echo "✅ Service started and enabled on boot."
else
  echo "⚠️  systemd not found. Running in background mode..."
  nohup venv/bin/python gpu_monitor_agent.py > agent.log 2>&1 &
  echo "✅ Agent running in background. Logs: $INSTALL_DIR/agent.log"
fi

echo ""
echo "🎉 Installation complete!"
echo "📊 View your dashboard: https://ai-gpu-energy-optimizer.vercel.app"
echo "📋 Manage service: sudo systemctl status gpu-optimizer"
