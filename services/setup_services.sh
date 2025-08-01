#!/bin/bash
# STDatalog Services Setup Script

set -e

echo "🔧 Setting up STDatalog Services..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root for systemd operations
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${RED}❌ Don't run this script as root. We'll use sudo when needed.${NC}"
        exit 1
    fi
}

# Install required Python packages
install_dependencies() {
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    /home/kirwinr/Desktop/stdatalog/.venv/bin/pip install flask psutil
}

# Create log directory
setup_logs() {
    echo -e "${BLUE}📁 Creating log directories...${NC}"
    sudo mkdir -p /home/kirwinr/logs
    sudo touch /home/kirwinr/logs/stdatalog-cli.log
    sudo touch /home/kirwinr/logs/stdatalog-ble.log
    sudo touch /home/kirwinr/logs/service-monitor.log
    sudo touch /home/kirwinr/logs/stdatalog-usboffload.log
    sudo touch /home/kirwinr/logs/stdatalog-browser.log
    sudo chown kirwinr:kirwinr /home/kirwinr/logs/*.log
    sudo chmod 664 /home/kirwinr/logs/*.log
}

# Copy service files to systemd
install_services() {
    echo -e "${BLUE}⚙️ Installing systemd service files...${NC}"
    
    # Copy service files
    sudo cp /home/kirwinr/Desktop/stdatalog/services/*.service /etc/systemd/system/
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    echo -e "${GREEN}✅ Service files installed${NC}"
}

# Enable and start services
enable_services() {
    echo -e "${BLUE}🚀 Enabling services...${NC}"
    
    # Enable all services to auto-start on boot and restart on failure
    sudo systemctl enable stdatalog-monitor
    sudo systemctl start stdatalog-monitor
    
    sudo systemctl enable stdatalog-ble
    sudo systemctl start stdatalog-ble
    
    sudo systemctl enable stdatalog-cli
    sudo systemctl start stdatalog-cli
    
    sudo systemctl enable stdatalog-usboffload
    sudo systemctl start stdatalog-usboffload
    
    # Enable browser service (runs once on graphical login)
    sudo systemctl enable stdatalog-browser
    
    echo -e "${GREEN}✅ All services enabled and started${NC}"
}

# Show status
show_status() {
    echo -e "\n${BLUE}📊 Service Status:${NC}"
    echo "----------------------------------------"
    
    services=("stdatalog-monitor" "stdatalog-ble" "stdatalog-cli" "stdatalog-usboffload" "stdatalog-browser")
    for service in "${services[@]}"; do
        status=$(systemctl is-active $service 2>/dev/null || echo "inactive")
        if [ "$status" = "active" ]; then
            echo -e "${service}: ${GREEN}${status}${NC}"
        else
            echo -e "${service}: ${RED}${status}${NC}"
        fi
    done
    
    echo ""
    echo -e "${BLUE}🌐 Dashboard URLs:${NC}"
    echo "  Network:  http://$(hostname -I | cut -d' ' -f1):8080"
    echo ""
    echo -e "${BLUE}📋 Useful Commands:${NC}"
    echo "  Start CLI:      sudo systemctl start stdatalog-cli"
    echo "  Stop CLI:       sudo systemctl stop stdatalog-cli"
    echo "  Restart BLE:    sudo systemctl restart stdatalog-ble"
    echo "  Restart USB:    sudo systemctl restart stdatalog-usboffload"
    echo "  Open Browser:   sudo systemctl start stdatalog-browser"
    echo "  View logs:      tail -f /home/kirwinr/logs/stdatalog-*.log"
    echo "  Service status: systemctl status stdatalog-cli"
}

# Run find_root.py to generate stdatalog_root.json
echo -e "${BLUE}🔍 Running stdatalog root finder...${NC}"
python3 "$(dirname "$0")/../thread/find_root.py"

# Main execution
main() {
    echo -e "${GREEN}🎯 STDatalog Service Setup${NC}"
    echo "========================================="
    
    check_sudo
    install_dependencies
    setup_logs
    install_services
    enable_services
    show_status
    
    echo -e "\n${GREEN}🎉 Setup complete!${NC}"
    echo -e "${YELLOW}⚠️ Remember: CLI service might requires manual start after hardware reset${NC}"
}

# Run main function
main "$@"
