# 🐻 Accurate Cyber Bear v3.0.0

<img width="636" height="524" alt="bear12" src="https://github.com/user-attachments/assets/e5ed469f-da94-40e9-8201-cd5cba5c4f09" />



Accurate Cyber Bear 

[![GitHub stars](https://img.shields.io/github/stars/Iankulani/accurate_cyber_bear)](https://github.com/Iankulani/accurate_cyber_bear/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Iankulani/accurate_cyber_bear)](https://github.com/Iankulani/accurate_cyber_bear/issues)
[![Docker Image Size](https://img.shields.io/docker/image-size/iankulani/accurate_cyber_bear/latest)](https://hub.docker.com/r/iankulani/accurate_cyber_bear)

**Ultimate Cybersecurity Command Center with Multi-Platform Integration**

---

## ✨ Features

- 🔌 **SSH Remote Command Execution** - Manage multiple SSH servers
- 🚀 **REAL Traffic Generation** - ICMP, TCP, UDP, HTTP, HTTPS, DNS
- 🕷️ **Nikto Web Vulnerability Scanner** - Comprehensive web security scanning
- 🔐 **CRUNCH Password Generator** - Advanced wordlist generation
- 🔒 **IP Management & Threat Detection** - Real-time threat monitoring
- 📊 **Advanced Data Visualization** - Interactive charts and graphs
- 📱 **Multi-Platform Bot Support** - Discord, Telegram, Slack, iMessage, Web
- 🌐 **Web Dashboard** - Real-time analytics and control
- 📈 **1000+ Security Commands** - Complete cybersecurity toolkit

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Pull and run
docker pull ghcr.io/Iankulani/accurate-cyber-bear:latest
docker run -d --name cyber-bear -p 8080:8080 --privileged ghcr.io/iank/accurate-cyber-bear:latest

# Or use docker-compose
git clone https://github.com/Iankulani/accurate_cyber_bear.git
cd accurate-cyber-bear
docker-compose up -d


# Linux/macOS
```bash
# One-liner installation
curl -fsSL https://raw.githubusercontent.com/Iankulani//accurate-cyber-bear/main/scripts/install.sh | bash
```
# Or manual
```bash
git clone https://github.com/Iankulani/accurate_cyber_bear.git
cd accurate-cyber-bear
```
python3 -m venv venv
source venv/bin/activate
```bash
pip install -r requirements.txt
python3 accurate_cyber_bear.py
```
# Windows
# Run as Administrator
```bash
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```
# Or use batch file
```bash
scripts\install.bat
📊 Web Dashboard
Access the interactive dashboard at: http://localhost:8080
```
# Features:

* Real-time threat visualization

* Platform usage analytics

* Traffic type statistics

* Daily activity charts

* Command execution interface

# 🤖 Bot Integration
```bash
Discord
python
# Configure in config/discord_config.json
{
    "enabled": true,
    "token": "YOUR_BOT_TOKEN",
    "prefix": "!"
}
Telegram
python
# Configure in config/telegram_config.json
{
    "enabled": true,
    "api_id": "YOUR_API_ID",
    "api_hash": "YOUR_API_HASH",
    "bot_token": "YOUR_BOT_TOKEN"
}
Slack
python
# Configure in config/slack_config.json
{
    "enabled": true,
    "bot_token": "YOUR_BOT_TOKEN",
    "channel_id": "general"
}
```
# 📝 Command Reference

Category	Commands
Basic	help, status, system, time, date
Network	ping, scan, nmap, traceroute, whois, dns, location
SSH	ssh_add, ssh_list, ssh_connect, ssh_exec, ssh_disconnect
Traffic	generate_traffic, traffic_types, traffic_status, traffic_stop
Wordlist	crunch, crunch_list
Scanner	nikto, nikto_status
IP Mgmt	add_ip, remove_ip, block_ip, unblock_ip, list_ips, ip_info
Reports	threats, report, dashboard, chart

Examples
# Network scanning
```bash
ping 8.8.8.8
scan 192.168.1.1
nmap example.com -p 80,443
```
# Traffic generation
```bash
generate_traffic icmp 8.8.8.8 10
generate_traffic http_get 192.168.1.1 30 80
```
# Password generation
```bash
crunch 4 8 alphanumeric mywordlist.txt
```
# Web scanning
nikto example.com

# IP management
```bash
add_ip 192.168.1.100
block_ip 192.168.1.100 "Suspicious activity"
```
# Dashboard

dashboard
chart threats
chart platform
🐳 Docker Deployment
Build locally
```bash
docker build -t cyber-bear:latest .
docker run -d --name cyber-bear -p 8080:8080 --privileged cyber-bear:latest
Docker Compose (Full Stack)
bash
docker-compose up -d
```
# With monitoring stack
```bash
docker-compose --profile monitoring up -d
Environment Variables
```

# See config/.env.example for all options
```bash
docker run -d \
  --name cyber-bear \
  -p 8080:8080 \
  -e WEB_PORT=8080 \
  -e LOG_LEVEL=DEBUG \
  -v cyber-bear-data:/app/.accurate_cyber_bear \
  --privileged \
  cyber-bear:latest
🔧 Development
Setup Development Environment
```
# Clone repository

```bash
git clone https://github.com/Iankulani/accurate_cyber_bear.git
cd accurate-cyber-bear
```

# Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
# Install development dependencies
```bash
pip install -r requirements-dev.txt
pip install -e .
```

# Run tests
```bash
pytest tests/ -v --cov=accurate_cyber_bear
```
# Run linting
```bash
flake8 accurate_cyber_bear.py
black accurate_cyber_bear.py
Building Documentation
bash
pip install sphinx sphinx-rtd-theme
cd docs
make html
```



