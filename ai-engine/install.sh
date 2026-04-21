#!/bin/bash
# AI GPU Energy Optimizer - One-Click Installer
# Version: 2.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[OK]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root is not recommended. Continuing anyway..."
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
print_status "Python version detected: $PYTHON_VERSION"

# Installation directory
INSTALL_DIR="$HOME/gpu-optimizer"
REPO="mikebains41-debug/ai-gpu-energy-optimizer-"
BRANCH="main"
SUBDIR="ai-engine"

print_status "Installing AI GPU Energy Optimizer Agent..."
print_status "Installation directory: $INSTALL_DIR"

# Create install directory
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download agent files
print_status "Downloading agent files..."
FILES=("gpu_monitor_agent.py" "agent_requirements.txt")

for file in "${FILES[@]}"; do
    URL="https://raw.githubusercontent.com/$REPO/$BRANCH/$SUBDIR/$file"
    print_status "  Downloading $file..."
    if curl -sSL --fail "$URL" -o "$file"; then
        print_success "  Downloaded $file"
    else
        print_error "  Failed to download $file from $URL"
        exit 1
    fi
done

# Get user credentials
echo ""
print_status "=== Beta Credentials ==="
print_warning "You need beta credentials to continue."
echo "If you don't have them, email: Mikebains41@gmail.com"
echo ""

read -p "Cluster ID: " CLUSTER_ID
if [ -z "$CLUSTER_ID" ]; then
    print_error "Cluster ID cannot be empty"
    exit 1
fi

read -p "API Key: " API_KEY
if [ -z "$API_KEY" ]; then
    print_error "API Key cannot be empty"
    exit 1
fi

read -p "Backend URL (press Enter for default): " BACKEND_URL
BACKEND_URL="${BACKEND_URL:-https://ai-gpu-brain-v2.onrender.com}"

# Create config.json
cat > config.json << EOF
{
  "backend_url": "$BACKEND_URL",
  "cluster_id": "$CLUSTER_ID",
  "api_key": "$API_KEY",
  "check_interval_seconds": 2
}
EOF
print_success "Config file created: config.json"

# Install Python dependencies
print_status "Installing Python dependencies..."
if ! command -v python3 -m venv &> /dev/null; then
    print_error "python3-venv is not installed. Install it with: sudo apt install python3-venv"
    exit 1
fi

python3 -m venv venv
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r agent_requirements.txt
print_success "Dependencies installed"

# Test NVML availability
print_status "Testing NVIDIA NVML..."
if python3 -c "import pynvml; pynvml.nvmlInit(); print('NVML OK')" 2>/dev/null; then
    print_success "NVML detected - GPU monitoring available"
else
    print_warning "NVML not detected - Agent will run in MOCK mode"
    print_warning "Make sure NVIDIA drivers are installed for real GPU monitoring"
fi

# Setup auto-start service (systemd only)
if command -v systemctl &> /dev/null && [ -d "/etc/systemd/system" ]; then
    print_status "Setting up systemd service..."
    
    SERVICE_FILE="/etc/systemd/system/gpu-optimizer.service"
    
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=AI GPU Energy Optimizer Agent
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/gpu_monitor_agent.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable gpu-optimizer
    sudo systemctl start gpu-optimizer
    
    print_success "Systemd service installed and started"
    print_status "  Check status: sudo systemctl status gpu-optimizer"
    print_status "  View logs: sudo journalctl -u gpu-optimizer -f"
else
    print_warning "systemd not found. Running in background mode..."
    nohup venv/bin/python gpu_monitor_agent.py > agent.log 2>&1 &
    print_success "Agent running in background (PID: $!)"
    print_status "  Logs: $INSTALL_DIR/agent.log"
fi

# Final output
echo ""
print_success "🎉 Installation complete!"
echo ""
echo "=========================================="
echo "  AI GPU Energy Optimizer - Agent Running"
echo "=========================================="
echo ""
echo "📊 Dashboard: https://ai-gpu-energy-optimizer.vercel.app"
echo ""
echo "🔧 Commands:"
if command -v systemctl &> /dev/null; then
    echo "   Status:  sudo systemctl status gpu-optimizer"
    echo "   Logs:    sudo journalctl -u gpu-optimizer -f"
    echo "   Restart: sudo systemctl restart gpu-optimizer"
    echo "   Stop:    sudo systemctl stop gpu-optimizer"
else
    echo "   Logs:    tail -f $INSTALL_DIR/agent.log"
    echo "   Stop:    pkill -f gpu_monitor_agent.py"
fi
echo ""
echo "📧 Need help? Email: Mikebains41@gmail.com"
echo "=========================================="

# Test connection to backend
print_status "Testing connection to backend..."
if curl -s --fail "$BACKEND_URL/health" > /dev/null 2>&1; then
    print_success "Backend reachable"
else
    print_warning "Backend not reachable. Check your internet connection"
fi

exit 0
