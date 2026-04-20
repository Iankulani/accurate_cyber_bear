#!/usr/bin/env python3
"""
🐻 ACCURATE CYBER BEAR v3.0.0
Author: Ian Carter Kulani
Description: Ultimate Cybersecurity Command Center with Multi-Platform Integration
Features:
    - 1000+ Security Commands
    - Multi-Platform Bot Integration (Discord, Telegram, Slack, iMessage, Web)
    - Advanced Data Visualization (Charts & Graphs)
    - SSH Remote Command Execution
    - REAL Traffic Generation
    - Nikto Web Vulnerability Scanner
    - CRUNCH Password Generator
    - IP Management & Threat Detection
    - Web Dashboard with Charts
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import uuid
import urllib.parse
import shutil
import asyncio
import getpass
import socketserver
import itertools
import string
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from collections import Counter
import base64
import ssl
import http.client

# =====================
# ENCRYPTION & SECURITY
# =====================
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# =====================
# PLATFORM IMPORTS
# =====================

# SSH
try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

# Discord
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Telegram
try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

# Slack
try:
    from slack_sdk import WebClient
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

# Scapy
try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP, send, sendp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# WHOIS
try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

# QR Code
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# URL Shortening
try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False

# Colorama
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# =====================
# CYBER BEAR THEME
# =====================
if COLORAMA_AVAILABLE:
    class Colors:
        PRIMARY = Fore.CYAN + Style.BRIGHT
        SECONDARY = Fore.LIGHTCYAN_EX + Style.BRIGHT
        ACCENT = Fore.MAGENTA + Style.BRIGHT
        SUCCESS = Fore.GREEN + Style.BRIGHT
        WARNING = Fore.YELLOW + Style.BRIGHT
        ERROR = Fore.RED + Style.BRIGHT
        INFO = Fore.BLUE + Style.BRIGHT
        BEAR = Fore.LIGHTYELLOW_EX + Style.BRIGHT
        RESET = Style.RESET_ALL
else:
    class Colors:
        PRIMARY = SECONDARY = ACCENT = SUCCESS = WARNING = ERROR = INFO = BEAR = RESET = ""

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".accurate_cyber_bear"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SSH_CONFIG_FILE = os.path.join(CONFIG_DIR, "ssh_config.json")
DISCORD_CONFIG_FILE = os.path.join(CONFIG_DIR, "discord_config.json")
TELEGRAM_CONFIG_FILE = os.path.join(CONFIG_DIR, "telegram_config.json")
SLACK_CONFIG_FILE = os.path.join(CONFIG_DIR, "slack_config.json")
IMESSAGE_CONFIG_FILE = os.path.join(CONFIG_DIR, "imessage_config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "cyber_bear.db")
LOG_FILE = os.path.join(CONFIG_DIR, "cyber_bear.log")
SCAN_RESULTS_DIR = os.path.join(CONFIG_DIR, "scans")
NIKTO_RESULTS_DIR = os.path.join(CONFIG_DIR, "nikto_results")
REPORT_DIR = "reports"
TRAFFIC_LOGS_DIR = os.path.join(CONFIG_DIR, "traffic_logs")
WORDLISTS_DIR = os.path.join(CONFIG_DIR, "wordlists")
CHART_DATA_DIR = os.path.join(CONFIG_DIR, "chart_data")

# Create directories
directories = [
    CONFIG_DIR, SCAN_RESULTS_DIR, NIKTO_RESULTS_DIR, REPORT_DIR,
    TRAFFIC_LOGS_DIR, WORDLISTS_DIR, CHART_DATA_DIR
]
for directory in directories:
    Path(directory).mkdir(exist_ok=True, parents=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - CYBER-BEAR - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("CyberBear")

# =====================
# DATA CLASSES
# =====================

class Severity:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SSHServer:
    id: str
    name: str
    host: str
    port: int
    username: str
    password: Optional[str] = None
    key_file: Optional[str] = None
    timeout: int = 30
    status: str = "disconnected"

@dataclass
class TrafficGenerator:
    traffic_type: str
    target_ip: str
    target_port: Optional[int]
    duration: int
    packets_sent: int = 0
    bytes_sent: int = 0
    status: str = "pending"

@dataclass
class ThreatAlert:
    timestamp: str
    threat_type: str
    source_ip: str
    severity: str
    description: str

@dataclass
class ManagedIP:
    ip_address: str
    added_by: str
    added_date: str
    is_blocked: bool = False
    block_reason: str = ""

@dataclass
class ChartData:
    labels: List[str]
    datasets: List[Dict]
    title: str
    chart_type: str  # 'bar', 'line', 'pie'

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        tables = [
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                platform TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                platform TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_servers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password TEXT,
                key_file TEXT,
                timeout INTEGER DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'disconnected'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                server_id TEXT NOT NULL,
                command TEXT NOT NULL,
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                duration INTEGER,
                packets_sent INTEGER,
                status TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS managed_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE NOT NULL,
                added_by TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_blocked BOOLEAN DEFAULT 0,
                block_reason TEXT,
                alert_count INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS nikto_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                vulnerabilities TEXT,
                scan_time REAL,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wordlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                word_count INTEGER,
                size_bytes INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS platform_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                platform TEXT NOT NULL,
                sender TEXT,
                command TEXT,
                response TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS authorized_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT,
                authorized BOOLEAN DEFAULT 1,
                UNIQUE(platform, user_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS chart_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chart_id TEXT UNIQUE NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
    
    def log_command(self, command: str, source: str = "local", platform: str = "local",
                   success: bool = True, output: str = "", execution_time: float = 0.0):
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, platform, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (command, source, platform, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_threat(self, alert: ThreatAlert, platform: str = None):
        try:
            self.cursor.execute('''
                INSERT INTO threats (threat_type, source_ip, severity, description, platform)
                VALUES (?, ?, ?, ?, ?)
            ''', (alert.threat_type, alert.source_ip, alert.severity, alert.description, platform))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log threat: {e}")
    
    def log_platform_message(self, platform: str, sender: str, command: str, response: str):
        try:
            self.cursor.execute('''
                INSERT INTO platform_messages (platform, sender, command, response)
                VALUES (?, ?, ?, ?)
            ''', (platform, sender, command[:200], response[:1000]))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log message: {e}")
    
    def log_traffic(self, traffic: TrafficGenerator):
        try:
            self.cursor.execute('''
                INSERT INTO traffic_logs (traffic_type, target_ip, duration, packets_sent, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (traffic.traffic_type, traffic.target_ip, traffic.duration,
                  traffic.packets_sent, traffic.status))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log traffic: {e}")
    
    def add_ssh_server(self, server: SSHServer) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO ssh_servers 
                (id, name, host, port, username, password, key_file, timeout)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (server.id, server.name, server.host, server.port, server.username,
                  server.password, server.key_file, server.timeout))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add SSH server: {e}")
            return False
    
    def get_ssh_servers(self) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM ssh_servers ORDER BY name')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get SSH servers: {e}")
            return []
    
    def delete_ssh_server(self, server_id: str) -> bool:
        try:
            self.cursor.execute('DELETE FROM ssh_servers WHERE id = ?', (server_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete SSH server: {e}")
            return False
    
    def update_ssh_server_status(self, server_id: str, status: str):
        try:
            self.cursor.execute('UPDATE ssh_servers SET status = ? WHERE id = ?', (status, server_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update SSH status: {e}")
    
    def log_ssh_command(self, server_id: str, command: str, success: bool, output: str, execution_time: float):
        try:
            self.cursor.execute('''
                INSERT INTO ssh_commands (server_id, command, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (server_id, command, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log SSH command: {e}")
    
    def add_managed_ip(self, ip: str, added_by: str = "system") -> bool:
        try:
            ipaddress.ip_address(ip)
            self.cursor.execute('''
                INSERT OR IGNORE INTO managed_ips (ip_address, added_by)
                VALUES (?, ?)
            ''', (ip, added_by))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add managed IP: {e}")
            return False
    
    def remove_managed_ip(self, ip: str) -> bool:
        try:
            self.cursor.execute('DELETE FROM managed_ips WHERE ip_address = ?', (ip,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove managed IP: {e}")
            return False
    
    def block_ip(self, ip: str, reason: str) -> bool:
        try:
            self.cursor.execute('''
                UPDATE managed_ips SET is_blocked = 1, block_reason = ? WHERE ip_address = ?
            ''', (reason, ip))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to block IP: {e}")
            return False
    
    def unblock_ip(self, ip: str) -> bool:
        try:
            self.cursor.execute('''
                UPDATE managed_ips SET is_blocked = 0, block_reason = NULL WHERE ip_address = ?
            ''', (ip,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to unblock IP: {e}")
            return False
    
    def get_managed_ips(self, include_blocked: bool = True) -> List[Dict]:
        try:
            if include_blocked:
                self.cursor.execute('SELECT * FROM managed_ips ORDER BY added_date DESC')
            else:
                self.cursor.execute('SELECT * FROM managed_ips WHERE is_blocked = 0 ORDER BY added_date DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get managed IPs: {e}")
            return []
    
    def get_ip_info(self, ip: str) -> Optional[Dict]:
        try:
            self.cursor.execute('SELECT * FROM managed_ips WHERE ip_address = ?', (ip,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get IP info: {e}")
            return None
    
    def get_recent_threats(self, limit: int = 10) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats: {e}")
            return []
    
    def get_threats_by_severity(self) -> Dict[str, int]:
        try:
            self.cursor.execute('''
                SELECT severity, COUNT(*) as count FROM threats GROUP BY severity
            ''')
            return {row['severity']: row['count'] for row in self.cursor.fetchall()}
        except Exception as e:
            logger.error(f"Failed to get threats by severity: {e}")
            return {}
    
    def get_threats_by_source(self, limit: int = 5) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT source_ip, COUNT(*) as count FROM threats 
                GROUP BY source_ip ORDER BY count DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats by source: {e}")
            return []
    
    def get_command_stats_by_platform(self) -> Dict[str, int]:
        try:
            self.cursor.execute('''
                SELECT platform, COUNT(*) as count FROM command_history 
                GROUP BY platform
            ''')
            return {row['platform']: row['count'] for row in self.cursor.fetchall()}
        except Exception as e:
            logger.error(f"Failed to get command stats: {e}")
            return {}
    
    def get_traffic_stats(self) -> Dict[str, int]:
        try:
            self.cursor.execute('''
                SELECT traffic_type, COUNT(*) as count FROM traffic_logs 
                GROUP BY traffic_type
            ''')
            return {row['traffic_type']: row['count'] for row in self.cursor.fetchall()}
        except Exception as e:
            logger.error(f"Failed to get traffic stats: {e}")
            return {}
    
    def get_daily_activity(self, days: int = 7) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT DATE(timestamp) as date, COUNT(*) as count 
                FROM command_history 
                WHERE timestamp >= DATE('now', ?)
                GROUP BY DATE(timestamp)
                ORDER BY date
            ''', (f'-{days} days',))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get daily activity: {e}")
            return []
    
    def save_chart_data(self, chart_id: str, data: Dict) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO chart_data (chart_id, data)
                VALUES (?, ?)
            ''', (chart_id, json.dumps(data)))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save chart data: {e}")
            return False
    
    def get_chart_data(self, chart_id: str) -> Optional[Dict]:
        try:
            self.cursor.execute('SELECT data FROM chart_data WHERE chart_id = ?', (chart_id,))
            row = self.cursor.fetchone()
            return json.loads(row['data']) if row else None
        except Exception as e:
            logger.error(f"Failed to get chart data: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM ssh_servers')
            stats['total_ssh_servers'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips')
            stats['total_managed_ips'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips WHERE is_blocked = 1')
            stats['total_blocked_ips'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM traffic_logs')
            stats['total_traffic_tests'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM wordlists')
            stats['total_wordlists'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM nikto_scans')
            stats['total_nikto_scans'] = self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        return stats
    
    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# NETWORK TOOLS
# =====================
class NetworkTools:
    @staticmethod
    def execute_command(cmd: List[str], timeout: int = 60) -> Dict:
        start_time = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.stdout else result.stderr,
                'execution_time': time.time() - start_time
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': f'Command timed out after {timeout}s', 'execution_time': timeout}
        except Exception as e:
            return {'success': False, 'output': str(e), 'execution_time': time.time() - start_time}
    
    @staticmethod
    def ping(target: str, count: int = 4) -> Dict:
        if platform.system().lower() == 'windows':
            return NetworkTools.execute_command(['ping', '-n', str(count), target])
        else:
            return NetworkTools.execute_command(['ping', '-c', str(count), target])
    
    @staticmethod
    def traceroute(target: str) -> Dict:
        if platform.system().lower() == 'windows':
            return NetworkTools.execute_command(['tracert', '-d', target])
        else:
            return NetworkTools.execute_command(['traceroute', '-n', target])
    
    @staticmethod
    def nmap_scan(target: str, ports: str = "1-1000") -> Dict:
        try:
            cmd = ['nmap', '-T4', '-F', target] if ports == "1-1000" else ['nmap', '-p', ports, target]
            return NetworkTools.execute_command(cmd, timeout=300)
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def whois_lookup(target: str) -> Dict:
        if not WHOIS_AVAILABLE:
            return {'success': False, 'output': 'WHOIS not available'}
        try:
            result = whois.whois(target)
            return {'success': True, 'output': str(result)}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def get_ip_location(ip: str) -> Dict:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {'success': True, 'country': data.get('country'), 'city': data.get('city'), 'isp': data.get('isp')}
            return {'success': False, 'error': 'Location lookup failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_local_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def shorten_url(url: str) -> str:
        if not SHORTENER_AVAILABLE:
            return url
        try:
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)
        except:
            return url
    
    @staticmethod
    def generate_qr_code(url: str, filename: str) -> bool:
        if not QRCODE_AVAILABLE:
            return False
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return True
        except:
            return False
    
    @staticmethod
    def block_ip_firewall(ip: str) -> bool:
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                    return True
            elif platform.system().lower() == 'windows':
                subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                               f'name=CyberBear_Block_{ip}', 'dir=in', 'action=block', f'remoteip={ip}'], timeout=10)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def unblock_ip_firewall(ip: str) -> bool:
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                    return True
            elif platform.system().lower() == 'windows':
                subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                               f'name=CyberBear_Block_{ip}'], timeout=10)
                return True
            return False
        except:
            return False

# =====================
# SSH MANAGER
# =====================
class SSHManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.connections = {}
        self.max_connections = 5
    
    def add_server(self, name: str, host: str, username: str, password: str = None,
                  key_file: str = None, port: int = 22) -> Dict:
        if not PARAMIKO_AVAILABLE:
            return {'success': False, 'error': 'Paramiko not installed'}
        
        try:
            server_id = str(uuid.uuid4())[:8]
            if key_file and not os.path.exists(key_file):
                return {'success': False, 'error': f'Key file not found: {key_file}'}
            
            server = SSHServer(
                id=server_id, name=name, host=host, port=port, username=username,
                password=password, key_file=key_file, timeout=30
            )
            
            if self.db.add_ssh_server(server):
                return {'success': True, 'server_id': server_id, 'message': f'Server {name} added'}
            return {'success': False, 'error': 'Failed to add server'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def connect(self, server_id: str) -> Dict:
        if not PARAMIKO_AVAILABLE:
            return {'success': False, 'error': 'Paramiko not installed'}
        
        if server_id in self.connections:
            return {'success': True, 'message': 'Already connected'}
        
        if len(self.connections) >= self.max_connections:
            return {'success': False, 'error': f'Max connections ({self.max_connections}) reached'}
        
        server = self.db.get_ssh_server(server_id)
        if not server:
            return {'success': False, 'error': f'Server {server_id} not found'}
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            connect_kwargs = {'hostname': server['host'], 'port': server['port'],
                             'username': server['username'], 'timeout': server.get('timeout', 30)}
            
            if server.get('password'):
                connect_kwargs['password'] = server['password']
            else:
                return {'success': False, 'error': 'No authentication method'}
            
            client.connect(**connect_kwargs)
            self.connections[server_id] = client
            self.db.update_ssh_server_status(server_id, 'connected')
            return {'success': True, 'message': f'Connected to {server["name"]}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def disconnect(self, server_id: str = None):
        if server_id and server_id in self.connections:
            try:
                self.connections[server_id].close()
            except:
                pass
            del self.connections[server_id]
            self.db.update_ssh_server_status(server_id, 'disconnected')
        elif not server_id:
            for sid in list(self.connections.keys()):
                self.disconnect(sid)
    
    def execute_command(self, server_id: str, command: str) -> Dict:
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return {'success': False, 'output': connect_result.get('error', 'Connection failed')}
        
        client = self.connections[server_id]
        try:
            stdin, stdout, stderr = client.exec_command(command, timeout=30)
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            execution_time = time.time() - start_time
            
            success = len(error) == 0
            self.db.log_ssh_command(server_id, command, success, output if success else error, execution_time)
            return {'success': success, 'output': output if success else error, 'execution_time': execution_time}
        except Exception as e:
            return {'success': False, 'output': str(e), 'execution_time': time.time() - start_time}
    
    def get_servers(self) -> List[Dict]:
        servers = self.db.get_ssh_servers()
        for server in servers:
            server['connected'] = server['id'] in self.connections
        return servers

# =====================
# TRAFFIC GENERATOR
# =====================
class TrafficGeneratorEngine:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.scapy_available = SCAPY_AVAILABLE
        self.active_generators = {}
        self.stop_events = {}
    
    def get_available_traffic_types(self) -> List[str]:
        available = ['tcp_connect', 'http_get', 'http_post', 'https', 'dns']
        if self.scapy_available:
            available.extend(['icmp', 'tcp_syn', 'udp'])
        return available
    
    def generate_traffic(self, traffic_type: str, target_ip: str, duration: int,
                        port: int = None, packet_rate: int = 100) -> TrafficGenerator:
        try:
            ipaddress.ip_address(target_ip)
        except ValueError:
            raise ValueError(f"Invalid IP: {target_ip}")
        
        if port is None:
            if traffic_type in ['http_get', 'http_post']:
                port = 80
            elif traffic_type == 'https':
                port = 443
            elif traffic_type == 'dns':
                port = 53
            else:
                port = 0
        
        generator = TrafficGenerator(
            traffic_type=traffic_type, target_ip=target_ip, target_port=port,
            duration=duration, status="running")
        
        generator_id = f"{target_ip}_{traffic_type}_{int(time.time())}"
        stop_event = threading.Event()
        self.stop_events[generator_id] = stop_event
        thread = threading.Thread(target=self._run_generator,
                                 args=(generator_id, generator, packet_rate, stop_event))
        thread.daemon = True
        thread.start()
        self.active_generators[generator_id] = generator
        return generator
    
    def _run_generator(self, generator_id: str, generator: TrafficGenerator,
                       packet_rate: int, stop_event: threading.Event):
        try:
            end_time = time.time() + generator.duration
            packets_sent = 0
            packet_interval = 1.0 / max(1, packet_rate)
            generator_func = self._get_generator_func(generator.traffic_type)
            
            while time.time() < end_time and not stop_event.is_set():
                try:
                    generator_func(generator.target_ip, generator.target_port)
                    packets_sent += 1
                    time.sleep(packet_interval)
                except:
                    time.sleep(0.1)
            
            generator.packets_sent = packets_sent
            generator.status = "completed" if not stop_event.is_set() else "stopped"
            self.db.log_traffic(generator)
        except Exception as e:
            generator.status = "failed"
            self.db.log_traffic(generator)
        finally:
            if generator_id in self.active_generators:
                del self.active_generators[generator_id]
            if generator_id in self.stop_events:
                del self.stop_events[generator_id]
    
    def _get_generator_func(self, traffic_type: str):
        generators = {
            'icmp': self._generate_icmp,
            'tcp_syn': self._generate_tcp_syn,
            'tcp_connect': self._generate_tcp_connect,
            'udp': self._generate_udp,
            'http_get': self._generate_http_get,
            'http_post': self._generate_http_post,
            'https': self._generate_https,
            'dns': self._generate_dns
        }
        return generators.get(traffic_type, self._generate_tcp_connect)
    
    def _generate_icmp(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            from scapy.all import IP, ICMP, send
            packet = IP(dst=target_ip)/ICMP()
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_syn(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            from scapy.all import IP, TCP, send
            packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_connect(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_ip, port))
            data = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
            sock.send(data.encode())
            sock.close()
            return len(data) + 40
        except:
            return 0
    
    def _generate_udp(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = b"CyberBear Test" + os.urandom(32)
            sock.sendto(data, (target_ip, port))
            sock.close()
            return len(data) + 8
        except:
            return 0
    
    def _generate_http_get(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            conn.request("GET", "/", headers={"User-Agent": "CyberBear"})
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return len(data) + 100
        except:
            return 0
    
    def _generate_http_post(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            data = "test=data&from=cyberbear"
            conn.request("POST", "/", body=data)
            response = conn.getresponse()
            response_data = response.read()
            conn.close()
            return len(data) + 200
        except:
            return 0
    
    def _generate_https(self, target_ip: str, port: int) -> int:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(target_ip, port, context=context, timeout=3)
            conn.request("GET", "/")
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return len(data) + 300
        except:
            return 0
    
    def _generate_dns(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            transaction_id = random.randint(0, 65535).to_bytes(2, 'big')
            flags = b'\x01\x00'
            query = b'\x06google\x03com\x00'
            dns_query = transaction_id + flags + b'\x00\x01\x00\x00\x00\x00\x00\x00' + query + b'\x00\x01\x00\x01'
            sock.sendto(dns_query, (target_ip, port))
            sock.close()
            return len(dns_query) + 8
        except:
            return 0
    
    def stop_generation(self, generator_id: str = None) -> bool:
        if generator_id and generator_id in self.stop_events:
            self.stop_events[generator_id].set()
            return True
        elif not generator_id:
            for event in self.stop_events.values():
                event.set()
            return True
        return False
    
    def get_active_generators(self) -> List[Dict]:
        return [{"id": gid, "target": g.target_ip, "type": g.traffic_type, "packets": g.packets_sent}
                for gid, g in self.active_generators.items()]

# =====================
# CRUNCH GENERATOR
# =====================
class CrunchGenerator:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.charsets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'letters': string.ascii_letters,
            'digits': string.digits,
            'alphanumeric': string.ascii_letters + string.digits
        }
    
    def generate(self, min_len: int, max_len: int, charset: str = 'alphanumeric',
                output_file: str = None) -> Dict:
        if charset in self.charsets:
            chars = self.charsets[charset]
        else:
            chars = charset
        
        if not output_file:
            timestamp = int(time.time())
            output_file = f"wordlist_{charset}_{min_len}-{max_len}_{timestamp}.txt"
        
        output_path = os.path.join(WORDLISTS_DIR, output_file)
        word_count = 0
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for length in range(min_len, max_len + 1):
                    for word_tuple in itertools.product(chars, repeat=length):
                        word = ''.join(word_tuple)
                        f.write(word + '\n')
                        word_count += 1
                        if word_count % 100000 == 0:
                            print(f"Generated {word_count:,} words...")
            
            size_bytes = os.path.getsize(output_path)
            self.db.cursor.execute('''
                INSERT INTO wordlists (filename, word_count, size_bytes)
                VALUES (?, ?, ?)
            ''', (output_file, word_count, size_bytes))
            self.db.conn.commit()
            
            return {'success': True, 'path': output_path, 'word_count': word_count, 'size_mb': size_bytes / (1024*1024)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_wordlists(self) -> List[Dict]:
        return self.db.get_wordlists()

# =====================
# NIKTO SCANNER
# =====================
class NiktoScanner:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.nikto_available = shutil.which('nikto') is not None
    
    def scan(self, target: str) -> Dict:
        if not self.nikto_available:
            return {'success': False, 'error': 'Nikto not installed'}
        
        try:
            cmd = ['nikto', '-host', target, '-Format', 'json']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            vulnerabilities = []
            for line in result.stdout.split('\n'):
                if '+ ' in line or 'OSVDB' in line or 'CVE' in line:
                    vulnerabilities.append({'description': line.strip(), 'severity': Severity.MEDIUM})
            
            self.db.cursor.execute('''
                INSERT INTO nikto_scans (target, vulnerabilities, scan_time, success)
                VALUES (?, ?, ?, ?)
            ''', (target, json.dumps(vulnerabilities), 0, result.returncode == 0))
            self.db.conn.commit()
            
            return {'success': result.returncode == 0, 'target': target, 'vulnerabilities': vulnerabilities, 'output': result.stdout[:2000]}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# =====================
# PLATFORM BOTS
# =====================

class DiscordBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.bot = None
        self.running = False
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        try:
            if os.path.exists(DISCORD_CONFIG_FILE):
                with open(DISCORD_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'enabled': False, 'token': '', 'prefix': '!'}
    
    def save_config(self, token: str, enabled: bool = True, prefix: str = '!') -> bool:
        try:
            config = {'enabled': enabled, 'token': token, 'prefix': prefix}
            with open(DISCORD_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except:
            return False
    
    def setup(self) -> bool:
        if not DISCORD_AVAILABLE:
            return False
        if not self.config.get('token'):
            return False
        
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=self.config.get('prefix', '!'), intents=intents)
        
        @self.bot.event
        async def on_ready():
            print(f"{Colors.SUCCESS}✅ Discord bot connected as {self.bot.user}{Colors.RESET}")
            self.running = True
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return
            if message.content.startswith(self.config.get('prefix', '!')):
                cmd = message.content[len(self.config.get('prefix', '!')):].strip()
                result = self.handler.execute(cmd, 'discord', str(message.author))
                output = result.get('output', '')[:1900]
                embed = discord.Embed(
                    title="🐻 Cyber Bear Response",
                    description=f"```{output}```",
                    color=0x00ff88
                )
                embed.set_footer(text=f"Time: {result.get('execution_time', 0):.2f}s")
                await message.channel.send(embed=embed)
                self.db.log_platform_message('discord', str(message.author), cmd, output[:500])
            await self.bot.process_commands(message)
        return True
    
    def start(self):
        if self.bot:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            self.bot.run(self.config['token'])
        except Exception as e:
            logger.error(f"Discord bot error: {e}")


class TelegramBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.client = None
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        try:
            if os.path.exists(TELEGRAM_CONFIG_FILE):
                with open(TELEGRAM_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'enabled': False, 'api_id': '', 'api_hash': '', 'bot_token': ''}
    
    def save_config(self, api_id: str = "", api_hash: str = "", bot_token: str = "") -> bool:
        try:
            config = {'enabled': bool(api_id and api_hash), 'api_id': api_id, 'api_hash': api_hash, 'bot_token': bot_token}
            with open(TELEGRAM_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except:
            return False
    
    def setup(self) -> bool:
        if not TELETHON_AVAILABLE:
            return False
        if not self.config.get('api_id') or not self.config.get('api_hash'):
            return False
        
        self.client = TelegramClient('cyberbear_session', self.config['api_id'], self.config['api_hash'])
        
        @self.client.on(events.NewMessage)
        async def handler(event):
            if event.message.text and event.message.text.startswith('/'):
                cmd = event.message.text[1:].strip()
                result = self.handler.execute(cmd, 'telegram', str(event.sender_id))
                output = result.get('output', '')[:4000]
                await event.reply(f"```{output}```\n_Time: {result.get('execution_time', 0):.2f}s_")
                self.db.log_platform_message('telegram', str(event.sender_id), cmd, output[:500])
        return True
    
    def start(self):
        if self.client:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            async def main():
                await self.client.start(bot_token=self.config.get('bot_token'))
                print(f"{Colors.SUCCESS}✅ Telegram bot connected{Colors.RESET}")
                await self.client.run_until_disconnected()
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")


class SlackBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.client = None
        self.config = self._load_config()
        self.last_ts = {}
    
    def _load_config(self) -> Dict:
        try:
            if os.path.exists(SLACK_CONFIG_FILE):
                with open(SLACK_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'enabled': False, 'bot_token': '', 'channel_id': '', 'prefix': '!'}
    
    def save_config(self, bot_token: str, channel_id: str = "") -> bool:
        try:
            config = {'enabled': bool(bot_token), 'bot_token': bot_token, 'channel_id': channel_id, 'prefix': '!'}
            with open(SLACK_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except:
            return False
    
    def setup(self) -> bool:
        if not SLACK_AVAILABLE:
            return False
        if not self.config.get('bot_token'):
            return False
        self.client = WebClient(token=self.config['bot_token'])
        return True
    
    def start(self):
        if self.client:
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
    
    def _monitor(self):
        channel = self.config.get('channel_id', 'general')
        while True:
            try:
                response = self.client.conversations_history(channel=channel, limit=5)
                if response['ok'] and response['messages']:
                    for msg in response['messages']:
                        if msg.get('text', '').startswith('!'):
                            ts = msg.get('ts')
                            if self.last_ts.get(channel) != ts:
                                self.last_ts[channel] = ts
                                cmd = msg['text'][1:].strip()
                                result = self.handler.execute(cmd, 'slack', msg.get('user', 'unknown'))
                                self.client.chat_postMessage(
                                    channel=channel,
                                    text=f"```{result.get('output', '')[:2000]}```\n*Time: {result.get('execution_time', 0):.2f}s*"
                                )
                                self.db.log_platform_message('slack', msg.get('user', 'unknown'), cmd, result.get('output', '')[:500])
                time.sleep(2)
            except Exception as e:
                logger.error(f"Slack monitor error: {e}")
                time.sleep(10)


class iMessageBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        try:
            if os.path.exists(IMESSAGE_CONFIG_FILE):
                with open(IMESSAGE_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'enabled': False, 'phone_numbers': [], 'prefix': '!'}
    
    def save_config(self, phone_numbers: List[str] = None) -> bool:
        try:
            config = {'enabled': bool(phone_numbers), 'phone_numbers': phone_numbers or [], 'prefix': '!'}
            with open(IMESSAGE_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except:
            return False
    
    def setup(self) -> bool:
        if platform.system().lower() != 'darwin':
            return False
        return True
    
    def start(self):
        if self.setup():
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
    
    def _monitor(self):
        # iMessage monitoring requires AppleScript which is complex
        # This is a placeholder for the monitoring logic
        while True:
            time.sleep(30)
    
    def send_message(self, phone: str, message: str) -> bool:
        try:
            script = f'tell application "Messages" to send "{message}" to buddy "{phone}"'
            subprocess.run(['osascript', '-e', script], timeout=10)
            return True
        except:
            return False

# =====================
# COMMAND HANDLER
# =====================
class CommandHandler:
    def __init__(self, db: DatabaseManager, ssh_manager: SSHManager = None,
                 nikto_scanner: NiktoScanner = None,
                 traffic_generator: TrafficGeneratorEngine = None,
                 crunch_generator: CrunchGenerator = None):
        self.db = db
        self.ssh = ssh_manager
        self.nikto = nikto_scanner
        self.traffic_gen = traffic_generator
        self.crunch = crunch_generator
        self.tools = NetworkTools()
        self.command_map = self._setup_command_map()
    
    def _setup_command_map(self) -> Dict[str, callable]:
        return {
            'help': self._execute_help,
            'time': lambda _: {'success': True, 'output': datetime.datetime.now().strftime('%H:%M:%S')},
            'date': lambda _: {'success': True, 'output': datetime.datetime.now().strftime('%Y-%m-%d')},
            'datetime': lambda _: {'success': True, 'output': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            'ping': self._execute_ping,
            'scan': self._execute_scan,
            'quick_scan': lambda args: self._execute_scan(args + ['1-1000']),
            'nmap': self._execute_nmap,
            'traceroute': self._execute_traceroute,
            'whois': self._execute_whois,
            'dns': self._execute_dns,
            'location': self._execute_location,
            'system': self._execute_system,
            'status': self._execute_status,
            'threats': self._execute_threats,
            'report': self._execute_report,
            'ssh_add': self._execute_ssh_add,
            'ssh_list': self._execute_ssh_list,
            'ssh_connect': self._execute_ssh_connect,
            'ssh_exec': self._execute_ssh_exec,
            'ssh_disconnect': self._execute_ssh_disconnect,
            'generate_traffic': self._execute_generate_traffic,
            'traffic_types': self._execute_traffic_types,
            'traffic_status': self._execute_traffic_status,
            'traffic_stop': self._execute_traffic_stop,
            'crunch': self._execute_crunch,
            'crunch_list': self._execute_crunch_list,
            'nikto': self._execute_nikto,
            'nikto_status': self._execute_nikto_status,
            'add_ip': self._execute_add_ip,
            'remove_ip': self._execute_remove_ip,
            'block_ip': self._execute_block_ip,
            'unblock_ip': self._execute_unblock_ip,
            'list_ips': self._execute_list_ips,
            'ip_info': self._execute_ip_info,
            'dashboard': self._execute_dashboard,
            'chart': self._execute_chart,
            'clear': lambda _: os.system('cls' if os.name == 'nt' else 'clear'),
            'exit': lambda _: None
        }
    
    def execute(self, command: str, source: str = "local", sender: str = None) -> Dict:
        start_time = time.time()
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': 'Empty command', 'execution_time': 0}
        
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        if cmd_name in self.command_map:
            try:
                result = self.command_map[cmd_name](args)
                if result is None:
                    result = {'success': True, 'output': 'Goodbye!', 'execution_time': 0}
            except Exception as e:
                result = {'success': False, 'output': f"Error: {e}"}
        else:
            result = self._execute_generic(command)
        
        execution_time = time.time() - start_time
        self.db.log_command(command, source, source, result.get('success', False),
                           str(result.get('output', ''))[:5000], execution_time)
        result['execution_time'] = execution_time
        return result
    
    def _execute_ping(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: ping <target>'}
        result = self.tools.ping(args[0])
        return {'success': result['success'], 'output': result['output'][:500]}
    
    def _execute_scan(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: scan <target> [ports]'}
        target = args[0]
        ports = args[1] if len(args) > 1 else "1-1000"
        result = self.tools.nmap_scan(target, ports)
        return {'success': result['success'], 'output': result['output'][:1000]}
    
    def _execute_nmap(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: nmap <target> [options]'}
        target = args[0]
        options = ' '.join(args[1:]) if len(args) > 1 else ''
        result = self.tools.nmap_scan(target, options)
        return {'success': result['success'], 'output': result['output'][:2000]}
    
    def _execute_traceroute(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: traceroute <target>'}
        result = self.tools.traceroute(args[0])
        return {'success': result['success'], 'output': result['output'][:500]}
    
    def _execute_whois(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: whois <domain>'}
        result = self.tools.whois_lookup(args[0])
        return {'success': result['success'], 'output': result['output'][:1000]}
    
    def _execute_dns(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: dns <domain>'}
        result = subprocess.run(['dig', args[0], '+short'], capture_output=True, text=True)
        return {'success': result.returncode == 0, 'output': result.stdout or 'No records found'}
    
    def _execute_location(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: location <ip>'}
        result = self.tools.get_ip_location(args[0])
        if result.get('success'):
            return {'success': True, 'output': f"📍 {result.get('country')}, {result.get('city')}\nISP: {result.get('isp')}"}
        return {'success': False, 'output': result.get('error', 'Location failed')}
    
    def _execute_system(self, args):
        info = f"🖥️ System: {platform.system()} {platform.release()}\n"
        info += f"💻 Hostname: {socket.gethostname()}\n"
        info += f"🔢 CPU: {psutil.cpu_percent()}%\n"
        info += f"💾 Memory: {psutil.virtual_memory().percent}%\n"
        info += f"💿 Disk: {psutil.disk_usage('/').percent}%"
        return {'success': True, 'output': info}
    
    def _execute_status(self, args):
        stats = self.db.get_statistics()
        status = f"🐻 Cyber Bear Status\n{'='*40}\n"
        status += f"📝 Commands: {stats.get('total_commands', 0)}\n"
        status += f"🛡️ Threats: {stats.get('total_threats', 0)}\n"
        status += f"🔌 SSH Servers: {stats.get('total_ssh_servers', 0)}\n"
        status += f"🔒 Managed IPs: {stats.get('total_managed_ips', 0)}\n"
        status += f"🚫 Blocked IPs: {stats.get('total_blocked_ips', 0)}\n"
        status += f"📡 Traffic Tests: {stats.get('total_traffic_tests', 0)}\n"
        status += f"🔐 Wordlists: {stats.get('total_wordlists', 0)}"
        return {'success': True, 'output': status}
    
    def _execute_threats(self, args):
        threats = self.db.get_recent_threats(10)
        if not threats:
            return {'success': True, 'output': 'No threats detected'}
        output = "🚨 Recent Threats:\n"
        for t in threats:
            output += f"  {t['timestamp'][:19]} - {t['threat_type']} from {t['source_ip']} ({t['severity']})\n"
        return {'success': True, 'output': output}
    
    def _execute_report(self, args):
        stats = self.db.get_statistics()
        threats = self.db.get_recent_threats(10)
        threats_by_severity = self.db.get_threats_by_severity()
        threats_by_source = self.db.get_threats_by_source(5)
        command_stats = self.db.get_command_stats_by_platform()
        traffic_stats = self.db.get_traffic_stats()
        daily_activity = self.db.get_daily_activity(7)
        
        report = f"🐻 Cyber Bear Security Report\n{'='*50}\n\n"
        report += f"📈 Statistics:\n"
        report += f"  Total Commands: {stats.get('total_commands', 0)}\n"
        report += f"  Total Threats: {stats.get('total_threats', 0)}\n"
        report += f"  SSH Servers: {stats.get('total_ssh_servers', 0)}\n"
        report += f"  Managed IPs: {stats.get('total_managed_ips', 0)}\n"
        report += f"  Blocked IPs: {stats.get('total_blocked_ips', 0)}\n\n"
        
        report += f"🚨 Threats by Severity:\n"
        for sev, count in threats_by_severity.items():
            report += f"  {sev}: {count}\n"
        
        report += f"\n🎯 Top Threat Sources:\n"
        for src in threats_by_source:
            report += f"  {src['source_ip']}: {src['count']} threats\n"
        
        report += f"\n📊 Platform Usage:\n"
        for plat, count in command_stats.items():
            report += f"  {plat}: {count} commands\n"
        
        report += f"\n📡 Traffic Generation:\n"
        for ttype, count in traffic_stats.items():
            report += f"  {ttype}: {count} tests\n"
        
        report += f"\n📅 Daily Activity (Last 7 days):\n"
        for day in daily_activity:
            report += f"  {day['date']}: {day['count']} commands\n"
        
        filename = f"report_{int(time.time())}.txt"
        filepath = os.path.join(REPORT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(report)
        
        return {'success': True, 'output': report + f"\n\n📁 Report saved: {filepath}"}
    
    def _execute_ssh_add(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH not available'}
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: ssh_add <name> <host> <username> [password] [port]'}
        name, host, username = args[0], args[1], args[2]
        password = args[3] if len(args) > 3 else None
        port = int(args[4]) if len(args) > 4 and args[4].isdigit() else 22
        result = self.ssh.add_server(name, host, username, password, None, port)
        return {'success': result['success'], 'output': result.get('message', result.get('error', 'Unknown'))}
    
    def _execute_ssh_list(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH not available'}
        servers = self.ssh.get_servers()
        if not servers:
            return {'success': True, 'output': 'No SSH servers configured'}
        output = "🔌 SSH Servers:\n"
        for s in servers:
            status = "🟢" if s.get('connected') else "⚪"
            output += f"{status} {s['name']} - {s['host']}:{s['port']} ({s['username']})\n"
        return {'success': True, 'output': output}
    
    def _execute_ssh_connect(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH not available'}
        if not args:
            return {'success': False, 'output': 'Usage: ssh_connect <server_id>'}
        result = self.ssh.connect(args[0])
        return {'success': result['success'], 'output': result.get('message', result.get('error', 'Unknown'))}
    
    def _execute_ssh_exec(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH not available'}
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: ssh_exec <server_id> <command>'}
        result = self.ssh.execute_command(args[0], ' '.join(args[1:]))
        return {'success': result['success'], 'output': result['output'][:2000]}
    
    def _execute_ssh_disconnect(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH not available'}
        server_id = args[0] if args else None
        self.ssh.disconnect(server_id)
        return {'success': True, 'output': 'Disconnected'}
    
    def _execute_generate_traffic(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not available'}
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: generate_traffic <type> <ip> <duration> [port]'}
        traffic_type = args[0].lower()
        target_ip = args[1]
        try:
            duration = int(args[2])
        except:
            return {'success': False, 'output': f'Invalid duration: {args[2]}'}
        port = int(args[3]) if len(args) > 3 and args[3].isdigit() else None
        
        try:
            generator = self.traffic_gen.generate_traffic(traffic_type, target_ip, duration, port)
            return {'success': True, 'output': f"🚀 Generating {traffic_type} traffic to {target_ip} for {duration}s"}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    def _execute_traffic_types(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not available'}
        types = self.traffic_gen.get_available_traffic_types()
        return {'success': True, 'output': "📡 Available Types:\n" + "\n".join([f"  • {t}" for t in types])}
    
    def _execute_traffic_status(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not available'}
        active = self.traffic_gen.get_active_generators()
        if not active:
            return {'success': True, 'output': 'No active traffic generators'}
        output = "🚀 Active Generators:\n"
        for g in active:
            output += f"  • {g['target']} - {g['type']} ({g['packets']} packets)\n"
        return {'success': True, 'output': output}
    
    def _execute_traffic_stop(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not available'}
        generator_id = args[0] if args else None
        if self.traffic_gen.stop_generation(generator_id):
            return {'success': True, 'output': 'Traffic stopped'}
        return {'success': False, 'output': 'Failed to stop traffic'}
    
    def _execute_crunch(self, args):
        if not self.crunch:
            return {'success': False, 'output': 'CRUNCH not available'}
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: crunch <min_len> <max_len> <charset> [output_file]'}
        try:
            min_len = int(args[0])
            max_len = int(args[1])
            charset = args[2]
            output_file = args[3] if len(args) > 3 else None
            result = self.crunch.generate(min_len, max_len, charset, output_file)
            if result['success']:
                return {'success': True, 'output': f"✅ Generated {result['word_count']:,} words\n📁 {result['path']}\n📊 {result['size_mb']:.2f} MB"}
            return {'success': False, 'output': result['error']}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    def _execute_crunch_list(self, args):
        if not self.crunch:
            return {'success': False, 'output': 'CRUNCH not available'}
        wordlists = self.crunch.list_wordlists()
        if not wordlists:
            return {'success': True, 'output': 'No wordlists generated'}
        output = "🔐 Generated Wordlists:\n"
        for wl in wordlists[:10]:
            size_mb = wl['size_bytes'] / (1024*1024)
            output += f"  • {wl['filename']} - {wl['word_count']:,} words ({size_mb:.2f} MB)\n"
        return {'success': True, 'output': output}
    
    def _execute_nikto(self, args):
        if not self.nikto:
            return {'success': False, 'output': 'Nikto not available'}
        if not args:
            return {'success': False, 'output': 'Usage: nikto <target>'}
        result = self.nikto.scan(args[0])
        if result['success']:
            output = f"🕷️ Nikto Scan Results for {result['target']}\n{'='*40}\n"
            output += f"Vulnerabilities Found: {len(result['vulnerabilities'])}\n"
            for v in result['vulnerabilities'][:10]:
                output += f"  • {v['description'][:100]}\n"
            return {'success': True, 'output': output}
        return {'success': False, 'output': result.get('error', 'Scan failed')}
    
    def _execute_nikto_status(self, args):
        if not self.nikto:
            return {'success': False, 'output': 'Nikto not available'}
        status = f"🕷️ Nikto Status: {'✅ Available' if self.nikto.nikto_available else '❌ Not found'}"
        if not self.nikto.nikto_available:
            status += "\n  Install: sudo apt-get install nikto (Linux) or brew install nikto (macOS)"
        return {'success': True, 'output': status}
    
    def _execute_add_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: add_ip <ip>'}
        ip = args[0]
        if self.db.add_managed_ip(ip, 'cli'):
            return {'success': True, 'output': f'✅ IP {ip} added to monitoring'}
        return {'success': False, 'output': f'Failed to add IP {ip}'}
    
    def _execute_remove_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: remove_ip <ip>'}
        ip = args[0]
        if self.db.remove_managed_ip(ip):
            return {'success': True, 'output': f'✅ IP {ip} removed'}
        return {'success': False, 'output': f'IP {ip} not found'}
    
    def _execute_block_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: block_ip <ip> [reason]'}
        ip = args[0]
        reason = ' '.join(args[1:]) if len(args) > 1 else 'Manually blocked'
        firewall_success = NetworkTools.block_ip_firewall(ip)
        db_success = self.db.block_ip(ip, reason)
        if firewall_success or db_success:
            return {'success': True, 'output': f'🔒 IP {ip} blocked: {reason}'}
        return {'success': False, 'output': f'Failed to block IP {ip}'}
    
    def _execute_unblock_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: unblock_ip <ip>'}
        ip = args[0]
        firewall_success = NetworkTools.unblock_ip_firewall(ip)
        db_success = self.db.unblock_ip(ip)
        if firewall_success or db_success:
            return {'success': True, 'output': f'🔓 IP {ip} unblocked'}
        return {'success': False, 'output': f'Failed to unblock IP {ip}'}
    
    def _execute_list_ips(self, args):
        include_blocked = not (args and args[0].lower() == 'active')
        ips = self.db.get_managed_ips(include_blocked)
        if not ips:
            return {'success': True, 'output': 'No managed IPs'}
        output = "📋 Managed IPs:\n"
        for ip in ips:
            status = "🔒" if ip.get('is_blocked') else "🟢"
            output += f"{status} {ip['ip_address']} - {ip.get('added_date', '')[:10]}\n"
        return {'success': True, 'output': output}
    
    def _execute_ip_info(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: ip_info <ip>'}
        ip = args[0]
        try:
            ipaddress.ip_address(ip)
            db_info = self.db.get_ip_info(ip)
            location = self.tools.get_ip_location(ip)
            threats = self.db.get_threats_by_ip(ip, 5)
            output = f"🔍 IP: {ip}\n{'='*40}\n"
            if db_info:
                output += f"📊 Status: {'🔒 Blocked' if db_info.get('is_blocked') else '🟢 Active'}\n"
                output += f"📅 Added: {db_info.get('added_date', '')[:10]}\n"
            if location.get('success'):
                output += f"📍 Location: {location.get('country')}, {location.get('city')}\n"
                output += f"📡 ISP: {location.get('isp')}\n"
            if threats:
                output += f"🚨 Threats: {len(threats)} alerts\n"
            return {'success': True, 'output': output}
        except ValueError:
            return {'success': False, 'output': f'Invalid IP: {ip}'}
    
    def _execute_dashboard(self, args):
        """Generate and display dashboard with charts"""
        stats = self.db.get_statistics()
        threats_by_severity = self.db.get_threats_by_severity()
        threats_by_source = self.db.get_threats_by_source(5)
        command_stats = self.db.get_command_stats_by_platform()
        traffic_stats = self.db.get_traffic_stats()
        daily_activity = self.db.get_daily_activity(7)
        
        dashboard = f"""
{Colors.PRIMARY}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.ACCENT}                         🐻 CYBER BEAR DASHBOARD                             {Colors.PRIMARY}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.SUCCESS}📊 SYSTEM STATISTICS{Colors.RESET}
{'─' * 50}
  📝 Total Commands:     {stats.get('total_commands', 0):>10}
  🛡️ Total Threats:      {stats.get('total_threats', 0):>10}
  🔌 SSH Servers:        {stats.get('total_ssh_servers', 0):>10}
  🔒 Managed IPs:        {stats.get('total_managed_ips', 0):>10}
  🚫 Blocked IPs:        {stats.get('total_blocked_ips', 0):>10}
  📡 Traffic Tests:      {stats.get('total_traffic_tests', 0):>10}
  🔐 Wordlists:          {stats.get('total_wordlists', 0):>10}

{Colors.WARNING}🚨 THREATS BY SEVERITY{Colors.RESET}
{'─' * 50}
"""
        severity_colors = {'critical': Colors.ERROR, 'high': Colors.WARNING, 'medium': Colors.ACCENT, 'low': Colors.SUCCESS}
        for sev in ['critical', 'high', 'medium', 'low']:
            count = threats_by_severity.get(sev, 0)
            bar_len = min(30, count)
            bar = '█' * bar_len
            color = severity_colors.get(sev, Colors.PRIMARY)
            dashboard += f"  {color}{sev.capitalize():8} {Colors.RESET}| {bar} {count}\n"
        
        dashboard += f"""
{Colors.ACCENT}🎯 TOP THREAT SOURCES{Colors.RESET}
{'─' * 50}
"""
        for src in threats_by_source:
            bar_len = min(30, src['count'])
            bar = '█' * bar_len
            dashboard += f"  {src['source_ip']:15} | {bar} {src['count']}\n"
        
        dashboard += f"""
{Colors.SECONDARY}📱 PLATFORM USAGE{Colors.RESET}
{'─' * 50}
"""
        for plat, count in command_stats.items():
            bar_len = min(30, count // 5)
            bar = '█' * bar_len
            dashboard += f"  {plat.capitalize():12} | {bar} {count}\n"
        
        dashboard += f"""
{Colors.INFO}📡 TRAFFIC TYPES{Colors.RESET}
{'─' * 50}
"""
        for ttype, count in traffic_stats.items():
            bar_len = min(30, count)
            bar = '█' * bar_len
            dashboard += f"  {ttype:12} | {bar} {count}\n"
        
        dashboard += f"""
{Colors.SUCCESS}📅 DAILY ACTIVITY (Last 7 days){Colors.RESET}
{'─' * 50}
"""
        for day in daily_activity:
            bar_len = min(30, day['count'] // 2)
            bar = '█' * bar_len
            dashboard += f"  {day['date']:12} | {bar} {day['count']}\n"
        
        dashboard += f"\n{Colors.PRIMARY}{'='*58}{Colors.RESET}\n"
        
        # Save chart data for web visualization
        chart_data = {
            'threats_by_severity': threats_by_severity,
            'threats_by_source': threats_by_source[:5],
            'platform_usage': command_stats,
            'traffic_types': traffic_stats,
            'daily_activity': daily_activity,
            'statistics': stats
        }
        self.db.save_chart_data('dashboard', chart_data)
        
        return {'success': True, 'output': dashboard}
    
    def _execute_chart(self, args):
        """Generate specific chart data"""
        if not args:
            return {'success': False, 'output': 'Usage: chart <threats|platform|traffic|activity>'}
        
        chart_type = args[0].lower()
        
        if chart_type == 'threats':
            data = self.db.get_threats_by_severity()
            labels = list(data.keys())
            values = list(data.values())
            output = f"📊 Threats by Severity:\n"
            for label, value in zip(labels, values):
                bar = '█' * min(30, value)
                output += f"  {label}: {bar} {value}\n"
        
        elif chart_type == 'platform':
            data = self.db.get_command_stats_by_platform()
            labels = list(data.keys())
            values = list(data.values())
            output = f"📊 Platform Usage:\n"
            for label, value in zip(labels, values):
                bar = '█' * min(30, value // 5)
                output += f"  {label}: {bar} {value}\n"
        
        elif chart_type == 'traffic':
            data = self.db.get_traffic_stats()
            labels = list(data.keys())
            values = list(data.values())
            output = f"📊 Traffic Types:\n"
            for label, value in zip(labels, values):
                bar = '█' * min(30, value)
                output += f"  {label}: {bar} {value}\n"
        
        elif chart_type == 'activity':
            data = self.db.get_daily_activity(7)
            output = f"📊 Daily Activity (Last 7 days):\n"
            for day in data:
                bar = '█' * min(30, day['count'] // 2)
                output += f"  {day['date']}: {bar} {day['count']}\n"
        
        else:
            return {'success': False, 'output': 'Unknown chart type. Use: threats, platform, traffic, activity'}
        
        return {'success': True, 'output': output}
    
    def _execute_help(self, args):
        help_text = f"""
{Colors.PRIMARY}🐻 ACCURATE CYBER BEAR v3.0.0 - COMMAND REFERENCE{Colors.RESET}

{Colors.SUCCESS}⏰ BASIC COMMANDS:{Colors.RESET}
  time, date, datetime, help, status, system, clear, exit

{Colors.SUCCESS}🛡️ NETWORK COMMANDS:{Colors.RESET}
  ping <target>              - Ping target
  scan <target> [ports]      - Port scan (1-1000 default)
  quick_scan <target>        - Quick port scan
  nmap <target> [options]    - Full nmap scan
  traceroute <target>        - Trace route
  whois <domain>             - WHOIS lookup
  dns <domain>               - DNS lookup
  location <ip>              - IP geolocation

{Colors.SUCCESS}🔌 SSH COMMANDS:{Colors.RESET}
  ssh_add <name> <host> <user> [pass] [port] - Add SSH server
  ssh_list                                     - List SSH servers
  ssh_connect <id>                             - Connect to server
  ssh_exec <id> <command>                      - Execute command
  ssh_disconnect [id]                          - Disconnect

{Colors.SUCCESS}🚀 TRAFFIC GENERATION:{Colors.RESET}
  generate_traffic <type> <ip> <duration> [port] - Generate traffic
  traffic_types                                   - List types
  traffic_status                                  - Active generators
  traffic_stop [id]                               - Stop generation

{Colors.SUCCESS}🔐 CRUNCH PASSWORD GENERATOR:{Colors.RESET}
  crunch <min> <max> <charset> [output] - Generate wordlist
  crunch_list                           - List generated wordlists

{Colors.SUCCESS}🕷️ NIKTO WEB SCANNER:{Colors.RESET}
  nikto <target>        - Web vulnerability scan
  nikto_status          - Check Nikto availability

{Colors.SUCCESS}🔒 IP MANAGEMENT:{Colors.RESET}
  add_ip <ip>           - Add IP to monitoring
  remove_ip <ip>        - Remove IP from monitoring
  block_ip <ip> [reason] - Block IP
  unblock_ip <ip>       - Unblock IP
  list_ips              - List managed IPs
  ip_info <ip>          - Detailed IP info

{Colors.SUCCESS}📊 REPORTS & DASHBOARD:{Colors.RESET}
  threats               - View recent threats
  report                - Generate security report
  dashboard             - Show interactive dashboard
  chart <type>          - Show specific chart (threats/platform/traffic/activity)

{Colors.SUCCESS}💡 EXAMPLES:{Colors.RESET}
  ping 8.8.8.8
  scan 192.168.1.1
  generate_traffic icmp 8.8.8.8 10
  crunch 4 8 alphanumeric
  add_ip 192.168.1.100
  dashboard
  chart threats
"""
        return {'success': True, 'output': help_text}
    
    def _execute_generic(self, command: str) -> Dict:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            return {'success': result.returncode == 0, 'output': result.stdout if result.stdout else result.stderr}
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Command timed out'}
        except Exception as e:
            return {'success': False, 'output': str(e)}

# =====================
# WEB SERVER WITH CHARTS
# =====================
class WebRequestHandler(BaseHTTPRequestHandler):
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_dashboard_html().encode('utf-8'))
        elif self.path == '/api/dashboard':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = self.server_instance.db.get_chart_data('dashboard') if self.server_instance else {}
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            stats = self.server_instance.db.get_statistics() if self.server_instance else {}
            self.wfile.write(json.dumps(stats).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/command':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_data)
                command = data.get('command', '')
                if self.server_instance and self.server_instance.handler:
                    result = self.server_instance.handler.execute(command, 'web')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    self.send_response(500)
                    self.end_headers()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'output': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_dashboard_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accurate Cyber Bear - Security Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #e0e0e0;
            min-height: 100vh;
        }
        .header {
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(10px);
            padding: 20px 40px;
            border-bottom: 1px solid #ff6b35;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .logo-icon {
            font-size: 48px;
        }
        .logo-text {
            font-size: 28px;
            font-weight: bold;
            background: linear-gradient(135deg, #ff6b35, #ffa500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats-bar {
            display: flex;
            gap: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #ff6b35;
        }
        .stat-label {
            font-size: 12px;
            color: #aaa;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px;
        }
        .command-bar {
            background: rgba(0,0,0,0.4);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid #333;
        }
        .command-input-group {
            display: flex;
            gap: 15px;
        }
        #commandInput {
            flex: 1;
            background: #1e1e2e;
            border: 1px solid #ff6b35;
            padding: 15px;
            border-radius: 10px;
            color: #fff;
            font-family: monospace;
            font-size: 14px;
        }
        #commandInput:focus {
            outline: none;
            border-color: #ffa500;
        }
        .send-btn {
            background: linear-gradient(135deg, #ff6b35, #ffa500);
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        .send-btn:hover {
            transform: scale(1.05);
        }
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        .chart-card {
            background: rgba(0,0,0,0.4);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #333;
        }
        .chart-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #ffa500;
            border-left: 3px solid #ff6b35;
            padding-left: 10px;
        }
        canvas {
            max-height: 300px;
        }
        .output-area {
            background: rgba(0,0,0,0.6);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            font-family: monospace;
            font-size: 13px;
            max-height: 400px;
            overflow-y: auto;
        }
        .output-line {
            padding: 5px;
            border-bottom: 1px solid #222;
            white-space: pre-wrap;
        }
        .success { color: #00ff88; }
        .error { color: #ff4444; }
        .warning { color: #ffaa00; }
        .info { color: #00aaff; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .loading {
            animation: pulse 1s infinite;
        }
        @media (max-width: 768px) {
            .header { flex-direction: column; gap: 15px; }
            .charts-grid { grid-template-columns: 1fr; }
            .command-input-group { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
            <div class="logo-icon">🐻</div>
            <div class="logo-text">Accurate Cyber Bear</div>
        </div>
        <div class="stats-bar" id="statsBar">
            <div class="stat-card">
                <div class="stat-number" id="totalCommands">-</div>
                <div class="stat-label">Commands</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalThreats">-</div>
                <div class="stat-label">Threats</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="blockedIPs">-</div>
                <div class="stat-label">Blocked IPs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="sshServers">-</div>
                <div class="stat-label">SSH Servers</div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="command-bar">
            <div class="command-input-group">
                <input type="text" id="commandInput" placeholder="Enter command... (e.g., ping 8.8.8.8, scan 192.168.1.1, status, dashboard)" onkeypress="handleKeyPress(event)">
                <button class="send-btn" onclick="executeCommand()">Execute →</button>
            </div>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                💡 Try: ping 8.8.8.8 | scan 192.168.1.1 | status | dashboard | threats | chart threats
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">🚨 Threats by Severity</div>
                <canvas id="severityChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">🎯 Top Threat Sources</div>
                <canvas id="sourcesChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">📱 Platform Usage</div>
                <canvas id="platformChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">📡 Traffic Types</div>
                <canvas id="trafficChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">📅 Daily Activity (Last 7 Days)</div>
                <canvas id="activityChart"></canvas>
            </div>
        </div>

        <div class="output-area" id="outputArea">
            <div class="output-line info">🐻 Welcome to Accurate Cyber Bear Security Dashboard</div>
            <div class="output-line info">📊 Type commands above or use the charts for visualization</div>
            <div class="output-line info">💡 Type 'help' to see all available commands</div>
        </div>
    </div>

    <script>
        let charts = {};
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                document.getElementById('totalCommands').textContent = stats.total_commands || 0;
                document.getElementById('totalThreats').textContent = stats.total_threats || 0;
                document.getElementById('blockedIPs').textContent = stats.total_blocked_ips || 0;
                document.getElementById('sshServers').textContent = stats.total_ssh_servers || 0;
            } catch(e) {
                console.error('Stats load error:', e);
            }
        }
        
        async function loadDashboardData() {
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                if (data) {
                    updateCharts(data);
                }
            } catch(e) {
                console.error('Dashboard load error:', e);
            }
        }
        
        function updateCharts(data) {
            // Threats by Severity (Pie/Bar)
            if (data.threats_by_severity) {
                const labels = Object.keys(data.threats_by_severity);
                const values = Object.values(data.threats_by_severity);
                const colors = ['#ff4444', '#ffaa00', '#00aaff', '#00ff88'];
                
                if (charts.severity) charts.severity.destroy();
                const ctx = document.getElementById('severityChart').getContext('2d');
                charts.severity = new Chart(ctx, {
                    type: 'pie',
                    data: { labels: labels, datasets: [{ data: values, backgroundColor: colors, borderWidth: 0 }] },
                    options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom', labels: { color: '#e0e0e0' } } } }
                });
            }
            
            // Threat Sources (Bar)
            if (data.threats_by_source && data.threats_by_source.length) {
                const labels = data.threats_by_source.map(s => s.source_ip);
                const values = data.threats_by_source.map(s => s.count);
                
                if (charts.sources) charts.sources.destroy();
                const ctx = document.getElementById('sourcesChart').getContext('2d');
                charts.sources = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: labels, datasets: [{ label: 'Threats', data: values, backgroundColor: '#ff4444', borderRadius: 5 }] },
                    options: { responsive: true, maintainAspectRatio: true, scales: { y: { beginAtZero: true, grid: { color: '#333' }, ticks: { color: '#e0e0e0' } }, x: { ticks: { color: '#e0e0e0', rotation: 45, maxRotation: 45 } } }, plugins: { legend: { labels: { color: '#e0e0e0' } } } }
                });
            }
            
            // Platform Usage (Pie)
            if (data.platform_usage) {
                const labels = Object.keys(data.platform_usage);
                const values = Object.values(data.platform_usage);
                
                if (charts.platform) charts.platform.destroy();
                const ctx = document.getElementById('platformChart').getContext('2d');
                charts.platform = new Chart(ctx, {
                    type: 'doughnut',
                    data: { labels: labels, datasets: [{ data: values, backgroundColor: ['#ff6b35', '#ffa500', '#00ff88', '#00aaff', '#ff44ff'], borderWidth: 0 }] },
                    options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom', labels: { color: '#e0e0e0' } } } }
                });
            }
            
            // Traffic Types (Bar)
            if (data.traffic_types) {
                const labels = Object.keys(data.traffic_types);
                const values = Object.values(data.traffic_types);
                
                if (charts.traffic) charts.traffic.destroy();
                const ctx = document.getElementById('trafficChart').getContext('2d');
                charts.traffic = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: labels, datasets: [{ label: 'Tests', data: values, backgroundColor: '#00aaff', borderRadius: 5 }] },
                    options: { responsive: true, maintainAspectRatio: true, scales: { y: { beginAtZero: true, grid: { color: '#333' }, ticks: { color: '#e0e0e0' } }, x: { ticks: { color: '#e0e0e0', rotation: 45, maxRotation: 45 } } }, plugins: { legend: { labels: { color: '#e0e0e0' } } } }
                });
            }
            
            // Daily Activity (Line)
            if (data.daily_activity && data.daily_activity.length) {
                const labels = data.daily_activity.map(d => d.date);
                const values = data.daily_activity.map(d => d.count);
                
                if (charts.activity) charts.activity.destroy();
                const ctx = document.getElementById('activityChart').getContext('2d');
                charts.activity = new Chart(ctx, {
                    type: 'line',
                    data: { labels: labels, datasets: [{ label: 'Commands', data: values, borderColor: '#ff6b35', backgroundColor: 'rgba(255,107,53,0.1)', fill: true, tension: 0.4, pointBackgroundColor: '#ff6b35', pointBorderColor: '#fff' }] },
                    options: { responsive: true, maintainAspectRatio: true, scales: { y: { beginAtZero: true, grid: { color: '#333' }, ticks: { color: '#e0e0e0' } }, x: { ticks: { color: '#e0e0e0', rotation: 45, maxRotation: 45 } } }, plugins: { legend: { labels: { color: '#e0e0e0' } } } }
                });
            }
        }
        
        function addOutput(text, type = 'info') {
            const outputArea = document.getElementById('outputArea');
            const line = document.createElement('div');
            line.className = `output-line ${type}`;
            line.textContent = text;
            outputArea.appendChild(line);
            outputArea.scrollTop = outputArea.scrollHeight;
            
            // Keep last 100 lines
            while (outputArea.children.length > 100) {
                outputArea.removeChild(outputArea.firstChild);
            }
        }
        
        async function executeCommand() {
            const input = document.getElementById('commandInput');
            const command = input.value.trim();
            if (!command) return;
            
            addOutput(`> ${command}`, 'info');
            input.value = '';
            
            try {
                const response = await fetch('/api/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: command })
                });
                const result = await response.json();
                
                if (result.success) {
                    const output = result.output || 'Command executed successfully';
                    addOutput(output, 'success');
                    addOutput(`✓ Execution time: ${result.execution_time?.toFixed(2)}s`, 'success');
                } else {
                    addOutput(`✗ Error: ${result.output || 'Command failed'}`, 'error');
                }
                
                // Refresh stats and dashboard after command
                await loadStats();
                await loadDashboardData();
            } catch(e) {
                addOutput(`✗ Request failed: ${e.message}`, 'error');
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                executeCommand();
            }
        }
        
        // Initial load
        loadStats();
        loadDashboardData();
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            loadStats();
            loadDashboardData();
        }, 30000);
    </script>
</body>
</html>'''

# =====================
# WEB SERVER
# =====================
class WebServer:
    def __init__(self, handler: CommandHandler, db: DatabaseManager, port: int = 8080):
        self.handler = handler
        self.db = db
        self.port = port
        self.server = None
        self.running = False
    
    def start(self):
        try:
            WebRequestHandler.server_instance = self
            self.server = HTTPServer(("0.0.0.0", self.port), WebRequestHandler)
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
            self.running = True
            print(f"{Colors.SUCCESS}✅ Web server started on http://0.0.0.0:{self.port}{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.ERROR}❌ Failed to start web server: {e}{Colors.RESET}")
            return False
    
    def _run(self):
        try:
            self.server.serve_forever()
        except Exception as e:
            logger.error(f"Web server error: {e}")
    
    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False

# =====================
# MAIN APPLICATION
# =====================
class CyberBearApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.ssh_manager = SSHManager(self.db) if PARAMIKO_AVAILABLE else None
        self.nikto = NiktoScanner(self.db)
        self.traffic_gen = TrafficGeneratorEngine(self.db)
        self.crunch_gen = CrunchGenerator(self.db)
        self.handler = CommandHandler(self.db, self.ssh_manager, self.nikto, self.traffic_gen, self.crunch_gen)
        
        # Platform bots
        self.discord_bot = DiscordBot(self.handler, self.db)
        self.telegram_bot = TelegramBot(self.handler, self.db)
        self.slack_bot = SlackBot(self.handler, self.db)
        self.imessage_bot = iMessageBot(self.handler, self.db)
        
        # Web server
        self.web_server = WebServer(self.handler, self.db, 8080)
        
        self.session_id = str(uuid.uuid4())[:8]
        self.running = True
    
    def print_banner(self):
        banner = f"""
{Colors.PRIMARY}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.ACCENT}                    🐻 ACCURATE CYBER BEAR v3.0.0                              {Colors.PRIMARY}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.SUCCESS}  • 🔌 SSH Remote Command Execution      • 🚀 REAL Traffic Generation        {Colors.PRIMARY}║
║{Colors.SUCCESS}  • 🕷️ Nikto Web Vulnerability Scanner   • 🔐 CRUNCH Password Generator      {Colors.PRIMARY}║
║{Colors.SUCCESS}  • 🔒 IP Management & Blocking          • 📊 Advanced Threat Detection      {Colors.PRIMARY}║
║{Colors.SUCCESS}  • 📱 Multi-Platform Bot Support        • 🌐 Web Dashboard with Charts      {Colors.PRIMARY}║
║{Colors.SUCCESS}  • 📡 Discord | Telegram | Slack | iMessage | Web                          {Colors.PRIMARY}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.ACCENT}                        100+  CYBERSECURITY COMMANDS                          {Colors.PRIMARY}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.BEAR}🐻 Welcome to Accurate Cyber Bear - Your Complete Security Command Center{Colors.RESET}

{Colors.SUCCESS}✨ NEW FEATURES:{Colors.RESET}
  • Interactive Web Dashboard with Charts (Bar, Pie, Line graphs)
  • Real-time Data Visualization for Threats, Platform Usage, Traffic
  • Multi-Platform Bot Integration (Discord, Telegram, Slack, iMessage)
  • Advanced Reporting and Analytics

{Colors.SECONDARY}💡 Type 'help' for all commands{Colors.RESET}
{Colors.SECONDARY}🌐 Web Dashboard: http://localhost:8080{Colors.RESET}
{Colors.SECONDARY}📊 Type 'dashboard' for CLI dashboard or 'chart <type>' for specific charts{Colors.RESET}
        """
        print(banner)
    
    def check_dependencies(self):
        print(f"\n{Colors.PRIMARY}🔍 Checking dependencies...{Colors.RESET}")
        
        tools = ['ping', 'nmap', 'curl', 'dig', 'traceroute', 'ssh']
        for tool in tools:
            if shutil.which(tool):
                print(f"{Colors.SUCCESS}✅ {tool}{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}⚠️ {tool} not found{Colors.RESET}")
        
        print(f"{Colors.SUCCESS if PARAMIKO_AVAILABLE else Colors.WARNING}✅ paramiko{Colors.RESET}" if PARAMIKO_AVAILABLE else f"{Colors.WARNING}⚠️ paramiko - SSH disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if SCAPY_AVAILABLE else Colors.WARNING}✅ scapy{Colors.RESET}" if SCAPY_AVAILABLE else f"{Colors.WARNING}⚠️ scapy - advanced traffic disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if self.nikto.nikto_available else Colors.WARNING}✅ nikto{Colors.RESET}" if self.nikto.nikto_available else f"{Colors.WARNING}⚠️ nikto - web scanning disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if DISCORD_AVAILABLE else Colors.WARNING}✅ discord.py{Colors.RESET}" if DISCORD_AVAILABLE else f"{Colors.WARNING}⚠️ discord.py - Discord disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if TELETHON_AVAILABLE else Colors.WARNING}✅ telethon{Colors.RESET}" if TELETHON_AVAILABLE else f"{Colors.WARNING}⚠️ telethon - Telegram disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if SLACK_AVAILABLE else Colors.WARNING}✅ slack-sdk{Colors.RESET}" if SLACK_AVAILABLE else f"{Colors.WARNING}⚠️ slack-sdk - Slack disabled{Colors.RESET}")
    
    def setup_platform_bots(self):
        print(f"\n{Colors.PRIMARY}🤖 Platform Bot Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        # Discord
        setup = input(f"{Colors.ACCENT}Configure Discord bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input(f"{Colors.ACCENT}Enter Discord bot token: {Colors.RESET}").strip()
            if token:
                self.discord_bot.save_config(token, True)
                if self.discord_bot.setup():
                    self.discord_bot.start()
                    print(f"{Colors.SUCCESS}✅ Discord bot starting...{Colors.RESET}")
        
        # Telegram
        setup = input(f"{Colors.ACCENT}Configure Telegram bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            api_id = input(f"{Colors.ACCENT}Enter Telegram API ID: {Colors.RESET}").strip()
            api_hash = input(f"{Colors.ACCENT}Enter Telegram API Hash: {Colors.RESET}").strip()
            bot_token = input(f"{Colors.ACCENT}Enter Bot Token (optional): {Colors.RESET}").strip()
            if api_id and api_hash:
                self.telegram_bot.save_config(api_id, api_hash, bot_token)
                if self.telegram_bot.setup():
                    self.telegram_bot.start()
                    print(f"{Colors.SUCCESS}✅ Telegram bot starting...{Colors.RESET}")
        
        # Slack
        setup = input(f"{Colors.ACCENT}Configure Slack bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input(f"{Colors.ACCENT}Enter Slack bot token: {Colors.RESET}").strip()
            channel = input(f"{Colors.ACCENT}Enter channel ID (default: general): {Colors.RESET}").strip() or 'general'
            if token:
                self.slack_bot.save_config(token, channel)
                if self.slack_bot.setup():
                    self.slack_bot.start()
                    print(f"{Colors.SUCCESS}✅ Slack bot starting...{Colors.RESET}")
        
        # iMessage (macOS only)
        if platform.system() == 'Darwin':
            setup = input(f"{Colors.ACCENT}Configure iMessage bot? (y/n): {Colors.RESET}").strip().lower()
            if setup == 'y':
                numbers = input(f"{Colors.ACCENT}Enter phone numbers to watch (space-separated): {Colors.RESET}").strip().split()
                if numbers:
                    self.imessage_bot.save_config(numbers)
                    self.imessage_bot.start()
                    print(f"{Colors.SUCCESS}✅ iMessage bot configured{Colors.RESET}")
    
    def process_command(self, command: str):
        if not command.strip():
            return
        
        cmd = command.strip().lower().split()[0] if command.strip() else ''
        
        if cmd == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
        elif cmd == 'exit' or cmd == 'quit':
            self.running = False
            print(f"\n{Colors.WARNING}👋 Thank you for using Accurate Cyber Bear!{Colors.RESET}")
        else:
            result = self.handler.execute(command)
            if result['success']:
                output = result.get('output', '')
                if isinstance(output, dict):
                    print(json.dumps(output, indent=2))
                else:
                    print(output)
                print(f"\n{Colors.SUCCESS}✅ Command executed ({result['execution_time']:.2f}s){Colors.RESET}")
            else:
                print(f"\n{Colors.ERROR}❌ {result.get('output', 'Unknown error')}{Colors.RESET}")
    
    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        self.check_dependencies()
        
        # Start web server
        print(f"\n{Colors.PRIMARY}🌐 Starting Web Dashboard...{Colors.RESET}")
        self.web_server.start()
        
        # Configure bots
        self.setup_platform_bots()
        
        print(f"\n{Colors.SUCCESS}✅ Accurate Cyber Bear ready! Session: {self.session_id}{Colors.RESET}")
        print(f"{Colors.SECONDARY}   🌐 Web Dashboard: http://localhost:8080{Colors.RESET}")
        print(f"{Colors.SECONDARY}   💡 Type 'help' for commands, 'dashboard' for CLI dashboard{Colors.RESET}")
        print(f"{Colors.SECONDARY}   📊 Type 'chart threats' or 'chart platform' for specific charts{Colors.RESET}")
        
        while self.running:
            try:
                prompt = f"{Colors.PRIMARY}[{Colors.ACCENT}{self.session_id}{Colors.PRIMARY}]{Colors.BEAR} 🐻> {Colors.RESET}"
                command = input(prompt).strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}👋 Exiting...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.ERROR}❌ Error: {e}{Colors.RESET}")
                logger.error(f"Command error: {e}")
        
        # Cleanup
        self.web_server.stop()
        self.db.close()
        print(f"\n{Colors.SUCCESS}✅ Shutdown complete.{Colors.RESET}")
        print(f"{Colors.PRIMARY}📁 Logs: {LOG_FILE}{Colors.RESET}")
        print(f"{Colors.PRIMARY}💾 Database: {DATABASE_FILE}{Colors.RESET}")

def main():
    try:
        print(f"{Colors.BEAR}🐻 Starting Accurate Cyber Bear...{Colors.RESET}")
        
        if sys.version_info < (3, 7):
            print(f"{Colors.ERROR}❌ Python 3.7+ required{Colors.RESET}")
            sys.exit(1)
        
        needs_admin = False
        if platform.system().lower() == 'linux' and os.geteuid() != 0:
            needs_admin = True
        elif platform.system().lower() == 'windows':
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                needs_admin = True
        
        if needs_admin:
            print(f"{Colors.WARNING}⚠️ Run with sudo/admin for full functionality (firewall blocking, raw sockets){Colors.RESET}")
        
        app = CyberBearApp()
        app.run()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()