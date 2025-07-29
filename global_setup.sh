#!/bin/bash
#===============================================================================
# STDATALOG-PYSDK Global Setup Script for Linux
# This script automates the complete setup process for STDATALOG-PYSDK on Linux
# including USB drivers, Python environment, and all required packages
#===============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as a regular user."
   exit 1
fi

print_header "STDATALOG-PYSDK Global Setup for Linux"
echo ""
print_info "This script will:"
echo "  1. Check system requirements"
echo "  2. Install system dependencies"
echo "  3. Setup virtual environment"
echo "  4. Install STDATALOG-PYSDK packages"
echo "  5. Configure USB drivers for STWINBX1"
echo "  6. Test the installation"
echo ""

# Parse command line arguments
PROXY=""
NO_GUI=false
SKIP_USB=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --proxy)
            PROXY="$2"
            shift 2
            ;;
        --no-gui)
            NO_GUI=true
            shift
            ;;
        --skip-usb)
            SKIP_USB=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --proxy URL        Set proxy server (format: http://user:pass@server:port)"
            echo "  --no-gui          Skip GUI components installation"
            echo "  --skip-usb        Skip USB driver configuration"
            echo "  --help, -h        Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                                    # Standard installation"
            echo "  $0 --no-gui                         # Install without GUI"
            echo "  $0 --proxy http://user:pass@proxy:8080  # Install with proxy"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_header "Step 1: System Requirements Check"

# Check OS
if [[ "$(uname -s)" != "Linux" ]]; then
    print_error "This script is designed for Linux systems only"
    exit 1
fi

print_success "Running on Linux: $(uname -s) $(uname -r)"

# Check architecture
ARCH=$(uname -m)
print_info "Architecture: $ARCH"

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.10 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
print_success "Python version: $PYTHON_VERSION"

# Check if Python version is supported
if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
    print_success "Python version is supported (3.10+)"
else
    print_error "Python 3.10 or later is required. Current version: $PYTHON_VERSION"
    exit 1
fi

print_header "Step 2: Installing System Dependencies"

# Update package list
print_info "Updating package list..."
sudo apt-get update -qq

# Install basic dependencies
print_info "Installing basic system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    wget \
    curl \
    git \
    dos2unix \
    udev

# Install audio dependencies
print_info "Installing audio system dependencies..."
sudo apt-get install -y \
    libasound-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0

# Install X11/GUI dependencies (only if GUI is not disabled)
if [[ "$NO_GUI" != true ]]; then
    print_info "Installing GUI system dependencies..."
    sudo apt-get install -y \
        libxcb-cursor-dev \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libxkbcommon-x11-0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-xinerama0 \
        libxcb-xfixes0
fi

# Install USB development dependencies
if [[ "$SKIP_USB" != true ]]; then
    print_info "Installing USB development dependencies..."
    sudo apt-get install -y libudev-dev
fi

# Architecture-specific dependencies
if [[ "$ARCH" == "aarch64" || "$ARCH" == "armv7l" ]]; then
    print_info "Installing ARM-specific dependencies..."
    sudo apt-get install -y \
        libjpeg-dev \
        zlib1g-dev \
        libatlas-base-dev
fi

print_success "System dependencies installed successfully"

print_header "Step 3: Setting up Python Virtual Environment"

# Remove existing virtual environment if it exists
if [[ -d "$SCRIPT_DIR/.venv" ]]; then
    print_warning "Removing existing virtual environment..."
    rm -rf "$SCRIPT_DIR/.venv"
fi

# Create virtual environment
print_info "Creating Python virtual environment..."
cd "$SCRIPT_DIR"
python3 -m venv .venv

# Activate virtual environment
print_info "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
if [[ -n "$PROXY" ]]; then
    python -m pip install --upgrade pip --proxy="$PROXY"
else
    python -m pip install --upgrade pip
fi

print_success "Virtual environment created and activated"

print_header "Step 4: Installing STDATALOG-PYSDK Packages"

# Function to install wheel with proxy support
install_wheel() {
    local wheel_path="$1"
    local package_name="$2"
    
    if [[ ! -f "$wheel_path" ]]; then
        print_error "Wheel file not found: $wheel_path"
        return 1
    fi
    
    print_info "Installing $package_name..."
    
    # Check if package is already installed and uninstall if necessary
    if python -c "import pkg_resources; pkg_resources.require('$package_name')" 2>/dev/null; then
        print_warning "Uninstalling existing $package_name..."
        python -m pip uninstall "$package_name" -y
    fi
    
    # Install the wheel
    if [[ -n "$PROXY" ]]; then
        python -m pip install "$wheel_path" --proxy="$PROXY"
    else
        python -m pip install "$wheel_path"
    fi
    
    print_success "$package_name installed successfully"
}

# Install STDATALOG packages in dependency order
install_wheel "stdatalog_pnpl/dist/stdatalog_pnpl-1.2.0-py3-none-any.whl" "stdatalog_pnpl"
install_wheel "stdatalog_core/dist/stdatalog_core-1.2.0-py3-none-any.whl" "stdatalog_core"
install_wheel "stdatalog_dtk/dist/stdatalog_dtk-1.2.0-py3-none-any.whl" "stdatalog_dtk"

# Install GUI package only if not disabled
if [[ "$NO_GUI" != true ]]; then
    install_wheel "stdatalog_gui/dist/stdatalog_gui-1.2.0-py3-none-any.whl" "stdatalog_gui"
fi

# Install additional Python dependencies that might be needed
print_info "Installing additional Python dependencies..."
if [[ -n "$PROXY" ]]; then
    python -m pip install numpy matplotlib pandas --proxy="$PROXY"
else
    python -m pip install numpy matplotlib pandas
fi

print_success "All STDATALOG-PYSDK packages installed successfully"

print_header "Step 5: USB Driver Configuration"

if [[ "$SKIP_USB" == true ]]; then
    print_warning "Skipping USB driver configuration (--skip-usb flag set)"
else
    print_info "Configuring USB drivers for STWINBX1..."
    
    # Ask user to confirm the board is unplugged
    echo ""
    print_warning "IMPORTANT: Please unplug your STWINBX1 board before proceeding!"
    echo ""
    
    while true; do
        read -p "Have you unplugged the STWINBX1 board? [Y/n]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            break
        else
            echo ""
            print_warning "Please unplug the STWINBX1 board before continuing!"
            echo ""
        fi
    done
    
    # Configure files for Linux
    cd "$SCRIPT_DIR/linux_setup"
    dos2unix 30-hsdatalog.rules linux_USB_config_setup.sh linux_USB_config_removal.sh 2>/dev/null || true
    chmod +x linux_USB_config_setup.sh linux_USB_config_removal.sh
    
    # Architecture-specific library installation
    if [[ "$ARCH" == "armv7l" ]]; then
        print_info "Installing libraries for Raspberry Pi (ARMv7)..."
        sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/raspberryPi/libhs_datalog_v1.so" /usr/lib
        sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/raspberryPi/libhs_datalog_v2.so" /usr/lib
    elif [[ "$ARCH" == "aarch64" ]]; then
        print_info "Installing libraries for ARM64 (aarch64)..."
        
        # Install libusb from source for ARM64
        cd "$SCRIPT_DIR/linux_setup"
        if [[ ! -f "libusb-1.0.28.tar.bz2" ]]; then
            print_info "Downloading libusb..."
            wget https://github.com/libusb/libusb/releases/download/v1.0.28/libusb-1.0.28.tar.bz2
        fi
        
        if [[ ! -d "libusb-1.0.28" ]]; then
            print_info "Extracting libusb..."
            tar xjf libusb-1.0.28.tar.bz2
        fi
        
        cd libusb-1.0.28
        print_info "Building and installing libusb..."
        ./configure
        make -j$(nproc)
        sudo make install
        sudo ldconfig
        
        # Install appropriate architecture libraries
        if [[ "$(getconf LONG_BIT)" == "32" ]]; then
            print_info "Installing 32-bit ARM64 libraries..."
            sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/raspberryPi4_32bit/libhs_datalog_v1.so" /usr/lib
            sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/raspberryPi4_32bit/libhs_datalog_v2.so" /usr/lib
        else
            print_info "Installing 64-bit ARM64 libraries..."
            sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/raspberryPi4_64bit/libhs_datalog_v1.so" /usr/lib
            sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/raspberryPi4_64bit/libhs_datalog_v2.so" /usr/lib
        fi
    else
        print_info "Installing libraries for x86_64 Linux..."
        sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/linux/libhs_datalog_v1.so" /usr/lib
        sudo cp "$SCRIPT_DIR/stdatalog_core/stdatalog_core/HSD_link/communication/libhs_datalog/linux/libhs_datalog_v2.so" /usr/lib
    fi
    
    # Install udev rules
    print_info "Installing udev rules..."
    sudo cp "$SCRIPT_DIR/linux_setup/30-hsdatalog.rules" /etc/udev/rules.d/
    
    # Create hsdatalog group and add user
    if grep -q "hsdatalog" /etc/group; then
        print_success "hsdatalog group already exists"
    else
        print_info "Creating hsdatalog group and adding user..."
        sudo addgroup hsdatalog
        sudo usermod -aG hsdatalog $USER
        print_success "User $USER added to hsdatalog group"
    fi
    
    # Reload udev rules
    print_info "Reloading udev rules..."
    sudo udevadm control --reload
    
    print_success "USB drivers configured successfully"
fi

print_header "Step 6: Installation Verification"

cd "$SCRIPT_DIR"
source .venv/bin/activate

# Test package imports
print_info "Testing package imports..."

test_import() {
    local package="$1"
    if python -c "import $package" 2>/dev/null; then
        print_success "$package import successful"
        return 0
    else
        print_error "$package import failed"
        return 1
    fi
}

test_import "stdatalog_pnpl"
test_import "stdatalog_core"
test_import "stdatalog_dtk"

if [[ "$NO_GUI" != true ]]; then
    test_import "stdatalog_gui"
fi

# Test example availability
print_info "Checking example scripts..."
if [[ -f "stdatalog_examples/cli_applications/stdatalog/CLI/stdatalog_CLI.py" ]]; then
    print_success "CLI examples found"
else
    print_warning "CLI examples not found"
fi

if [[ "$NO_GUI" != true ]] && [[ -f "stdatalog_examples/gui_applications/stdatalog/GUI/stdatalog_GUI.py" ]]; then
    print_success "GUI examples found"
elif [[ "$NO_GUI" == true ]]; then
    print_info "GUI examples skipped (--no-gui flag set)"
else
    print_warning "GUI examples not found"
fi

print_header "Installation Complete!"

echo ""
print_success "STDATALOG-PYSDK has been successfully installed!"
echo ""
print_info "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Connect your STWINBX1 board"
echo ""

if [[ "$SKIP_USB" != true ]]; then
    echo "  3. Reboot your system to ensure USB drivers are loaded:"
    echo "     sudo reboot"
    echo ""
fi

echo "  4. Test the installation:"
if [[ "$NO_GUI" != true ]]; then
    echo "     python stdatalog_examples/gui_applications/stdatalog/GUI/stdatalog_GUI.py"
else
    echo "     python stdatalog_examples/cli_applications/stdatalog/CLI/stdatalog_CLI.py"
fi
echo ""

if [[ "$SKIP_USB" != true ]]; then
    print_warning "IMPORTANT: A system reboot is recommended to ensure USB drivers work correctly!"
fi

print_info "For more examples, check the stdatalog_examples directory"

echo ""
print_success "Setup completed successfully! 🎉"
