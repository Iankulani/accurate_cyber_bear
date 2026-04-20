#!/bin/bash
# Docker entrypoint script for Accurate Cyber Bear

set -e

echo "🐻 Starting Accurate Cyber Bear v3.0.0"
echo "========================================="

# Setup environment
export CYBER_BEAR_ENV=${CYBER_BEAR_ENV:-production}
export LOG_LEVEL=${LOG_LEVEL:-INFO}
export WEB_PORT=${WEB_PORT:-8080}
export API_PORT=${API_PORT:-8081}

# Create necessary directories
mkdir -p /app/.accurate_cyber_bear
mkdir -p /app/logs
mkdir -p /app/reports
mkdir -p /app/wordlists

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Running as root, adjusting permissions..."
    chown -R cyberbear:cyberbear /app
    # Drop privileges
    exec su -c "python3 /app/accurate_cyber_bear.py $@" cyberbear
else
    # Run normally
    exec python3 /app/accurate_cyber_bear.py "$@"
fi