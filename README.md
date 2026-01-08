
# NullShare 📡➡️📱

**Share files from your computer to phone instantly via QR code. No internet, no cloud, just local WiFi.**

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/MOUKA-513/NullShare/pulls)

</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/images/Screenshot%20From%202026-01-07%2016-29-04.png" width="45%" alt="NullShare Desktop Interface">
  <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/images/Screenshot%20From%202026-01-07%2016-29-54.png" width="45%" alt="NullShare Mobile Interface">
</p>

## 📋 Table of Contents
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [💻 Basic Usage](#-basic-usage)
- [📖 How It Works](#-how-it-works)
- [🛠️ CLI Commands](#️-cli-commands)
- [🎯 Examples](#-examples)
- [🏗️ Architecture](#️-architecture)
- [🔧 Development](#-development)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [🐛 Troubleshooting](#-troubleshooting)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📞 Support](#-support)

## ✨ Features

- ⚡ **Blazing Fast** - LAN transfer speeds (much faster than internet)
- 🔒 **100% Private** - Files never leave your local network
- 📱 **No App Needed** - Works in any mobile browser
- 🎯 **One Command** - Simple CLI interface
- 🐧 **Cross-Platform** - Windows, Linux, macOS
- 🔐 **Password Protection** - Optional security for sensitive files
- ⏱️ **Auto-Timeout** - Server stops automatically after transfer
- 📦 **Folder Support** - Auto-zips folders for easy download

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install nullshare

# Or install from source
git clone https://github.com/MOUKA-513/NullShare.git
cd NullShare
pip install -e .
Basic Usage
bash
# Share a single file
nullshare share document.pdf

# Share a folder (auto-zips)
nullshare share ~/Photos/

# Share with password protection
nullshare share --password secret file.txt

# Share with auto-timeout (5 minutes)
nullshare share --timeout 300 file.txt
📖 How It Works
1. Start Sharing
bash
nullshare share myfile.pdf
2. Scan QR Code
Open your phone's camera

Scan the QR code shown in terminal

Make sure phone is on same WiFi

3. Download
Webpage opens in phone browser

Tap download button

File transfers at WiFi speed

<p align="center"> <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/images/Screenshot%20From%202026-01-07%2016-29-04.png" width="400" alt="QR Code Interface"> </p>
🛠️ CLI Commands
Share Files/Folders
bash
nullshare share <file1> <file2> ...
Options:

Option	Description	Default
--port PORT	Port to use (0 = auto)	0
--no-zip	Don't zip folders	False
--password TEXT	Set password protection	(none)
--timeout SECONDS	Auto-stop after N seconds	300
--one-time	Files can only be downloaded once	False
--no-qr	Don't show QR code	False
--clean	Clear screen before showing QR	False
--verbose	Show detailed information	False
--help	Show help message	-
Server Management
bash
nullshare status        # Check if server is running
nullshare stop         # Stop running server
nullshare discover     # Discover servers on network
Help
bash
nullshare --help       # Show all commands
nullshare share --help # Show share command help
🎯 Examples
bash
# Share multiple files
nullshare share image1.jpg image2.png document.pdf

# Share current directory
nullshare share .

# Share with custom port
nullshare share --port 9090 file.txt

# Share sensitive files with password
nullshare share --password mypass secret_document.pdf

# Share for one-time download only
nullshare share --one-time invoice.pdf
🏗️ Architecture
text
┌─────────────┐     QR Code     ┌─────────────┐
│   Desktop   │─────────────────│    Phone    │
│   (Server)  │◄──WiFi Transfer─│  (Browser)  │
└─────────────┘                 └─────────────┘
       │                               │
  Python + Flask                 Any Mobile Browser
       │                               │
  Local HTTP Server             Web Interface
       │                               │
  File/Zip Serving              File Download
Technical Flow:

CLI starts a local HTTP server with Flask

Generates QR code with local IP and port

Mobile device scans QR and connects via browser

File transfer happens over local WiFi network

Server auto-terminates after timeout or completion

🔧 Development
Setup Development Environment
bash
# Clone repository
git clone https://github.com/MOUKA-513/NullShare.git
cd NullShare

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
Testing & Quality
bash
# Run tests
pytest

# Run linter
black nullshare/
flake8 nullshare/

# Run type checking
mypy nullshare/
📁 Project Structure
text
NullShare/
├── nullshare/          # Main package
│   ├── cli.py         # Command-line interface
│   ├── server.py      # HTTP server
│   ├── qr_generator.py # QR code generation
│   ├── utils.py       # Utilities
│   └── templates/     # Web templates
├── tests/             # Test suite
├── examples/          # Usage examples
├── images/            # Screenshots and assets
├── pyproject.toml     # Project configuration
├── requirements.txt   # Dependencies
├── setup.py          # Package setup
├── LICENSE           # MIT License
└── README.md         # This file
🤝 Contributing
Contributions are welcome! Here's how you can help:

Report Bugs - Open an issue with detailed information

Suggest Features - Share your ideas for improvement

Submit Pull Requests - Fix bugs or add features

Improve Documentation - Help make NullShare easier to use

Please read our Contributing Guidelines before submitting.

Development Workflow:
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

🐛 Troubleshooting
Problem: Phone can't connect
✅ Solution: Ensure both devices are on same WiFi network
✅ Solution: Check firewall allows connections on the port
✅ Solution: Try disabling VPN on either device

Problem: QR code doesn't work
✅ Solution: Make sure URL in QR starts with http:// not https://
✅ Solution: Some cameras need good lighting for QR scanning

Problem: Slow transfer
✅ Solution: This uses local network speed - much faster than internet
✅ Solution: Large files (>1GB) may take a few minutes
✅ Solution: Ensure good WiFi signal strength

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Inspired by local file sharing tools like Snapdrop and LocalSend

Built with amazing Python libraries: Flask, Click, QRCode

Thanks to all contributors and users who provide feedback

📞 Support
📧 Issues: GitHub Issues

💬 Discussion: GitHub Discussions

⭐ Star: If you find this useful, please star the repository!

<div align="center"> <p><strong>Made with ❤️ by <a href="https://github.com/MOUKA-513">MOUKA-513</a></strong></p> <p> <a href="https://github.com/MOUKA-513/NullShare/stargazers"> <img src="https://img.shields.io/github/stars/MOUKA-513/NullShare?style=social" alt="GitHub Stars"> </a> <a href="https://github.com/MOUKA-513/NullShare/forks"> <img src="https://img.shields.io/github/forks/MOUKA-513/NullShare?style=social" alt="GitHub Forks"> </a> </p> </div> ```
