#!/usr/bin/env pwsh
# Accurate Cyber Bear - PowerShell Installation Script

param(
    [switch]$Silent,
    [string]$InstallDir = "C:\Program Files\AccurateCyberBear",
    [string]$ConfigDir = "$env:USERPROFILE\.accurate_cyber_bear"
)

# Configuration
$ErrorActionPreference = "Stop"
$script:Version = "3.0.0"

# Colors
function Write-Success { Write-Host "✓ $($args[0])" -ForegroundColor Green }
function Write-Error { Write-Host "✗ $($args[0])" -ForegroundColor Red }
function Write-Info { Write-Host "ℹ $($args[0])" -ForegroundColor Cyan }
function Write-Warning { Write-Host "⚠ $($args[0])" -ForegroundColor Yellow }

# Check admin rights
function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check Python installation
function Test-Python {
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Python 3\.[0-9]+") {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

# Install Python
function Install-Python {
    Write-Info "Installing Python 3.11..."
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $installer = "$env:TEMP\python-installer.exe"
    
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installer
    Start-Process -FilePath $installer -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $installer -Force
    
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Install Chocolatey (optional)
function Install-Chocolatey {
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Info "Installing Chocolatey package manager..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }
}

# Main installation function
function Install-CyberBear {
    Write-Host "`n🐻 ACCURATE CYBER BEAR INSTALLER v$Version" -ForegroundColor Cyan
    Write-Host "=========================================" -ForegroundColor Cyan
    
    # Check admin
    if (-not (Test-Admin)) {
        Write-Error "Please run as Administrator"
        if (-not $Silent) { Read-Host "Press Enter to exit" }
        exit 1
    }
    
    # Check Python
    Write-Info "Checking Python installation..."
    if (-not (Test-Python)) {
        Write-Warning "Python not found, installing..."
        Install-Python
    } else {
        Write-Success "Python found"
    }
    
    # Create directories
    Write-Info "Creating directories..."
    $directories = @(
        $InstallDir,
        $ConfigDir,
        "$InstallDir\logs",
        "$InstallDir\reports",
        "$InstallDir\wordlists"
    )
    foreach ($dir in $directories) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    Write-Success "Directories created"
    
    # Copy files
    Write-Info "Copying files..."
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Copy-Item "$scriptDir\..\accurate_cyber_bear.py" "$InstallDir\" -Force
    Copy-Item "$scriptDir\..\requirements.txt" "$InstallDir\" -Force
    Write-Success "Files copied"
    
    # Install Python packages
    Write-Info "Installing Python packages (this may take a few minutes)..."
    & pip install --upgrade pip
    & pip install -r "$InstallDir\requirements.txt"
    Write-Success "Python packages installed"
    
    # Create configuration
    Write-Info "Creating configuration..."
    $configPath = "$ConfigDir\config.json"
    if (-not (Test-Path $configPath)) {
        $config = @{
            version = $Version
            install_path = $InstallDir
            data_path = $ConfigDir
            log_level = "INFO"
            web_port = 8080
            api_port = 8081
            enable_discord = $false
            enable_telegram = $false
            enable_slack = $false
            enable_imessage = $false
            auto_start = $false
        }
        $config | ConvertTo-Json | Set-Content $configPath
    }
    Write-Success "Configuration created"
    
    # Create launcher script
    Write-Info "Creating launcher..."
    $launcherContent = @"
@echo off
cd /d "$InstallDir"
python accurate_cyber_bear.py %*
"@
    $launcherPath = "$InstallDir\cyber-bear.bat"
    Set-Content -Path $launcherPath -Value $launcherContent
    
    # Add to PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($currentPath -notlike "*$InstallDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallDir", "Machine")
    }
    Write-Success "Launcher created"
    
    # Create desktop shortcut
    Write-Info "Creating desktop shortcut..."
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = "$desktopPath\Cyber Bear.lnk"
    $WScriptShell = New-Object -ComObject WScript.Shell
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $launcherPath
    $shortcut.Save()
    Write-Success "Desktop shortcut created"
    
    # Configure firewall
    Write-Info "Configuring Windows Firewall..."
    netsh advfirewall firewall add rule name="Cyber Bear Web" dir=in action=allow protocol=TCP localport=8080 | Out-Null
    netsh advfirewall firewall add rule name="Cyber Bear API" dir=in action=allow protocol=TCP localport=8081 | Out-Null
    Write-Success "Firewall rules added"
    
    # Installation complete
    Write-Host "`n=========================================" -ForegroundColor Cyan
    Write-Host "   INSTALLATION COMPLETE!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Info "Installation Directory: $InstallDir"
    Write-Info "Config Directory: $ConfigDir"
    Write-Info "Run with: cyber-bear.bat"
    Write-Info "Or use desktop shortcut"
    Write-Host ""
    
    if (-not $Silent) {
        Read-Host "Press Enter to exit"
    }
}

# Run installation
try {
    Install-CyberBear
} catch {
    Write-Error "Installation failed: $($_.Exception.Message)"
    if (-not $Silent) { Read-Host "Press Enter to exit" }
    exit 1
}