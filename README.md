# NullShare 📡

**Share files instantly via QR code on your local network - no internet, no cloud, just local WiFi.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen" alt="Status">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/assets/demo.gif" width="600" alt="NullShare Demo">
</p>

## ✨ Features

- **⚡ Instant Sharing**: Share files with one command, no configuration needed
- **📱 QR Code**: Scan with phone camera - no app required!
- **🔒 Security**: Password protection & one-time download options
- **🌐 Local Network**: Works without internet on any WiFi network
- **📊 Multiple Files**: Share files, folders, or entire directories
- **🔄 Cross-Platform**: Works on Windows, Linux, and macOS
- **🎯 Auto-Discovery**: Find other NullShare servers on your network
- **⏱️ Auto-Cleanup**: Timeout feature for automatic shutdown
- **🎨 Beautiful CLI**: Professional ASCII art and color-coded interface

## 🚀 Quick Start

### Installation (One Command)

```bash
# Install from PyPI (recommended)
pip install nullshare

# Or install from source
git clone https://github.com/MOUKA-513/NullShare.git
cd NullShare
pip install .
```

## Quick Usage

# Share a file
```bash
nullshare share document.pdf
```
# Share a folder
```bash
nullshare share photos/
```
# Share with password
```bash 
nullshare share secret.txt --password mypass
```

# Share for one-time download
```bashnullshare share file.zip --one-time
```
# Auto-stop after 5 minutes
```bash
nullshare share presentation.pptx --timeout 300
```

## Installation Guide

# Standard Installation
```bash
# Using pip (easiest)
 pip install nullshare

# Using pip3 if you have both Python 2 and 3
pip3 install nullshare
```

## Kali Linux / Debian / Ubuntu
Newer Debian-based systems have system protection. Use one of these methods:

# Method 1: Virtual Environment (Recommended)

```bash
python3 -m venv nullshare-venv
source nullshare-venv/bin/activate
pip install nullshare
```
# Method 2: User Installation

```bash
pip install --user nullshare
```
# Method 3: Using pipx (for CLI tools)

```bash
sudo apt install pipx
pipx install nullshare
```
## Windows
```powershell
# Command Prompt or PowerShell
pip install nullshare

# If Python is not in PATH
python -m pip install nullshare
```
## macOS
```bash
brew install python  # If you don't have Python
pip install nullshare
```
## Usage Examples
# Basic File Sharing
```bash
# Share a single file
nullshare share photo.jpg

# Share multiple files
nullshare share file1.txt file2.pdf file3.mp4

# Share a folder (auto-zips)
nullshare share documents/

# Share folder without zipping
nullshare share code/ --no-zip
```
## Advanced Features
```bash
# Password protection
nullshare share confidential.pdf --password "secret123"

# One-time download (file deleted after first download)
nullshare share token.txt --one-time

# Auto-shutdown after 10 minutes
nullshare share movie.mp4 --timeout 600

# Use specific port
nullshare share data.csv --port 8080

# Disable QR code (show URL only)
nullshare share file.txt --no-qr

# Clean screen before showing QR
nullshare share image.png --clean
```
# Network Tools
```bash
# Discover other NullShare servers on network
nullshare discover --scan

# Check if server is running
nullshare status --port 8000

# Stop a running server
nullshare stop --port 8000
```
# Command Reference
```text
nullshare [OPTIONS] COMMAND [ARGS]...

Commands:
  share       Share files/folders via QR code
  status      Check if a NullShare server is running
  stop        Stop a running NullShare server
  discover    Discover NullShare servers on local network
  version     Show version information and check for updates
  download    Download files from a NullShare server URL

Options:
  --help      Show this message and exit
  --version   Show version
```
# Share Command Options
```text
nullshare share [OPTIONS] [PATHS]...

Options:
  -p, --port INTEGER        Port to use (0 = auto)
  --no-zip                  Do not zip folders, share contents individually
  --password TEXT           Set password protection
  -t, --timeout INTEGER     Auto-stop after N seconds
  --one-time                Files can only be downloaded once
  --no-qr                   Do not show QR code
  --clean                   Clear screen before showing QR
  -v, --verbose             Show detailed information
  --no-banner               Do not show ASCII banner
```
##📱 How It Works
1. Start Sharing: Run nullshare share your-file.txt

2. Get QR Code: NullShare generates a QR code with local IP URL

3. Scan on Phone: Open camera app and scan QR code

4. Download: Files download directly to phone

5. Auto-Cleanup: Server stops automatically or when you press Ctrl+C

```text
┌─────────────┐    Start     ┌─────────────┐    Generate    ┌─────────────┐
│   Your PC   │─────────────▶│  NullShare  │─────────────▶│    QR Code   │
│  (Server)   │              │   Server    │               │   & URL      │
└─────────────┘              └─────────────┘               └─────────────┘
        │                           │                              │
        │ Same WiFi Network         │                              │
        └───────────────────────────┼──────────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │     Phone Scans     │
                         │      QR Code        │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   Download Files    │
                         │   Directly to Phone │
                         └─────────────────────┘
```
## Troubleshooting
# Common Issues
* "Server not accessible from phone"
- Ensure both devices are on same WiFi network

- Check firewall settings (allow port 8000)

- Try using --port 80 or --port 8080

* "Externally managed environment" (Kali/Debian)
```bash 
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install nullshare
```
# Network Ports
* Default ports used:

- 8000: Default NullShare port

- 5454: Auto-selected if 8000 is busy

- Any port: Specify with --port YOUR_PORT
## 🤝 Contributing
We love contributions! Here's how to help:

1. Fork the repository

2. Create a feature branch (git checkout -b feature/amazing-feature)

3. Commit your changes (git commit -m 'Add amazing feature')

4. Push to the branch (git push origin feature/amazing-feature)

5. Open a Pull Request

## Development Setup
```bash
# Clone the repo
git clone https://github.com/MOUKA-513/NullShare.git
cd NullShare

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black nullshare/
```
## 📄 License
MIT License - see LICENSE file for details.

## 🙏 Acknowledgments
-  Flask team for the amazing web framework

- QRcode library developers

- All contributors and testers

- You for using NullShare! ❤️

### Links
* GitHub: https://github.com/MOUKA-513/NullShare
* Youtube : https://www.youtube.com/@MOUKA-513
* Twitter : https://www.x.com/m0ukaa513
* Instagram : https://www.instagram.com/mouka.513/
* 
<p align="center"> Made with ❤️ by <a href="https://github.com/MOUKA-513">MOUKA-513</a> </p><p align="center"> ⭐ Star this repo if you find it useful! </p> ```

