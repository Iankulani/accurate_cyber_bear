#!/bin/bash
# Accurate Cyber Bear - Linux/macOS Installation Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
INSTALL_DIR="/opt/accurate-cyber-bear"
CONFIG_DIR="$HOME/.accurate_cyber_bear"
PYTHON_VERSION="3.9"
REPO_URL="https://github.com/iank/accurate-cyber-bear.git"

# Print colored message
print_message() {
    echo -e "${2}${1}${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_message "⚠️  Running as root is not recommended for security reasons" "$YELLOW"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if [[ -f /etc/debian_version ]]; then
            DISTRO="debian"
        elif [[ -f /etc/redhat-release ]]; then
            DISTRO="redhat"
        elif [[ -f /etc/alpine-release ]]; then
            DISTRO="alpine"
        else
            DISTRO="other"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        DISTRO="macos"
    else
        print_message "❌ Unsupported OS: $OSTYPE" "$RED"
        exit 1
    fi
    print_message "✅ Detected OS: $OS ($DISTRO)" "$GREEN"
}

# Install system dependencies
install_dependencies() {
    print_message "📦 Installing system dependencies..." "$CYAN"
    
    case $DISTRO in
        debian)
            sudo apt-get update
            sudo apt-get install -y \
                python3 python3-pip python3-dev \
                nmap nikto curl wget git \
                net-tools iproute2 iptables \
                tcpdump tshark \
                openssh-client dnsutils \
                build-essential libssl-dev libffi-dev
            ;;
        redhat)
            sudo yum install -y epel-release
            sudo yum install -y \
                python3 python3-pip python3-devel \
                nmap nikto curl wget git \
                net-tools iproute iptables \
                tcpdump wireshark-cli \
                openssh-clients bind-utils \
                gcc openssl-devel libffi-devel
            ;;
        alpine)
            sudo apk add --no-cache \
                python3 py3-pip python3-dev \
                nmap nikto curl wget git \
                net-tools iproute2 iptables \
                tcpdump tshark \
                openssh-client bind-tools \
                gcc musl-dev libffi-dev openssl-dev
            ;;
        macos)
            if ! command -v brew &> /dev/null; then
                print_message "📦 Installing Homebrew..." "$YELLOW"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python@3.11 nmap nikto wget git net-tools
            ;;
    esac
    
    print_message "✅ System dependencies installed" "$GREEN"
}

# Install Python dependencies
install_python_deps() {
    print_message "🐍 Installing Python dependencies..." "$CYAN"
    
    # Upgrade pip
    pip3 install --upgrade pip setuptools wheel
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        pip3 install -r requirements.txt
    else
        pip3 install \
            requests psutil cryptography colorama \
            paramiko scapy whois python-nmap \
            discord.py telethon slack-sdk \
            flask flask-socketio plotly pandas \
            qrcode pyshorteners python-dotenv \
            schedule tabulate prettytable tqdm \
            sqlalchemy alembic
    fi
    
    print_message "✅ Python dependencies installed" "$GREEN"
}

# Clone or update repository
setup_repository() {
    print_message "📁 Setting up repository..." "$CYAN"
    
    if [[ -d "$INSTALL_DIR" ]]; then
        print_message "⚠️  Directory exists, updating..." "$YELLOW"
        cd "$INSTALL_DIR"
        git pull
    else
        sudo mkdir -p "$INSTALL_DIR"
        sudo git clone "$REPO_URL" "$INSTALL_DIR"
        sudo chown -R $(whoami):$(whoami) "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
    
    print_message "✅ Repository ready at $INSTALL_DIR" "$GREEN"
}

# Create configuration
setup_config() {
    print_message "⚙️  Creating configuration..." "$CYAN"
    
    mkdir -p "$CONFIG_DIR"
    
    # Create default config if not exists
    if [[ ! -f "$CONFIG_DIR/config.json" ]]; then
        cat > "$CONFIG_DIR/config.json" <<EOF
{
    "version": "3.0.0",
    "install_path": "$INSTALL_DIR",
    "data_path": "$CONFIG_DIR",
    "log_level": "INFO",
    "web_port": 8080,
    "api_port": 8081,
    "enable_discord": false,
    "enable_telegram": false,
    "enable_slack": false,
    "enable_imessage": false,
    "auto_start": false,
    "session_timeout": 3600,
    "max_log_size_mb": 100,
    "retention_days": 30
}
EOF
    fi
    
    print_message "✅ Configuration created at $CONFIG_DIR" "$GREEN"
}

# Create systemd service (Linux only)
setup_service() {
    if [[ "$OS" == "linux" ]]; then
        print_message "🔧 Creating systemd service..." "$CYAN"
        
        sudo cat > /etc/systemd/system/cyber-bear.service <<EOF
[Unit]
Description=Accurate Cyber Bear Security Platform
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/accurate_cyber_bear.py
Restart=on-failure
RestartSec=10
StandardOutput=append:$CONFIG_DIR/cyber-bear.log
StandardError=append:$CONFIG_DIR/cyber-bear-error.log

[Install]
WantedBy=multi-user.target
EOF
        
        sudo systemctl daemon-reload
        print_message "✅ Systemd service created" "$GREEN"
        print_message "   Start with: sudo systemctl start cyber-bear" "$YELLOW"
        print_message "   Enable at boot: sudo systemctl enable cyber-bear" "$YELLOW"
    fi
}

# Create launcher script
create_launcher() {
    print_message "🚀 Creating launcher script..." "$CYAN"
    
    sudo cat > /usr/local/bin/cyber-bear <<EOF
#!/bin/bash
cd $INSTALL_DIR
python3 accurate_cyber_bear.py "\$@"
EOF
    
    sudo chmod +x /usr/local/bin/cyber-bear
    
    print_message "✅ Launcher created: 'cyber-bear' command available" "$GREEN"
}

# Setup firewall rules (optional)
setup_firewall() {
    print_message "🛡️  Would you like to configure firewall rules? (y/N)" "$YELLOW"
    read -r configure_firewall
    
    if [[ "$configure_firewall" =~ ^[Yy]$ ]]; then
        if command -v ufw &> /dev/null; then
            sudo ufw allow 8080/tcp comment 'Cyber Bear Web Dashboard'
            sudo ufw allow 8081/tcp comment 'Cyber Bear API'
            sudo ufw reload
            print_message "✅ Firewall rules added (UFW)" "$GREEN"
        elif command -v firewall-cmd &> /dev/null; then
            sudo firewall-cmd --permanent --add-port=8080/tcp
            sudo firewall-cmd --permanent --add-port=8081/tcp
            sudo firewall-cmd --reload
            print_message "✅ Firewall rules added (firewalld)" "$GREEN"
        else
            print_message "⚠️  No firewall manager found, skipping" "$YELLOW"
        fi
    fi
}

# Main installation
main() {
    print_message "🐻 Accurate Cyber Bear Installation v3.0.0" "$CYAN"
    print_message "=========================================" "$CYAN"
    
    check_root
    detect_os
    install_dependencies
    setup_repository
    install_python_deps
    setup_config
    create_launcher
    setup_service
    setup_firewall
    
    print_message "\n✅ Installation Complete!" "$GREEN"
    print_message "=========================================" "$CYAN"
    print_message "📁 Installation Directory: $INSTALL_DIR" "$BLUE"
    print_message "⚙️  Config Directory: $CONFIG_DIR" "$BLUE"
    print_message "🚀 Run with: cyber-bear" "$GREEN"
    print_message "🌐 Web Dashboard: http://localhost:8080" "$GREEN"
    print_message "📝 Logs: $CONFIG_DIR/cyber-bear.log" "$BLUE"
    print_message "=========================================" "$CYAN"
}

# Run main
main