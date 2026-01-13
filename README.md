# NullShare 📡➡️📱

- Share files from your computer to phone instantly via QR code.  
- No internet, no cloud, just local WiFi.

<div align="center">

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/images/Screenshot%20From%202026-01-07%2016-29-04.png" width="45%" alt="NullShare Desktop Interface">
  <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/images/Screenshot%20From%202026-01-07%2016-29-54.png" width="45%" alt="NullShare Mobile Interface">
</p>

---

## 📋 Table of Contents

- ✨ Features
- 🚀 Quick Start
- 📦 Installation
- 💻 Basic Usage
- 📖 How It Works
- 🛠️ CLI Commands
- 🎯 Examples
- 🏗️ Architecture
- 🔧 Development
- 📁 Project Structure
- 🐛 Troubleshooting
- 📄 License
- 🙏 Acknowledgments
- 📞 Support

---

## ✨ Features

- ⚡ **Blazing Fast** – LAN transfer speeds
- 🔒 **100% Private** – Files never leave your local network
- 📱 **No App Needed** – Works in any mobile browser
- 🎯 **One Command** – Simple CLI interface
- 🐧 **Cross-Platform** – Windows, Linux, macOS
- 🔐 **Password Protection** – Optional security
- ⏱️ **Auto-Timeout** – Server stops automatically
- 📦 **Folder Support** – Auto-zips folders

---

## 🚀 Quick Start

### 📦 Installation

```bash
# Install from source
git clone https://github.com/MOUKA-513/NullShare.git
cd NullShare
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
### 💻 Basic Usage
```bash
# Share a single file
nullshare share document.pdf

# Share a folder
nullshare share ~/Photos/

# Password protection
nullshare share --password secret file.txt

# Auto-timeout (5 minutes)
nullshare share --timeout 300 file.txt
```
### 📖 How It Works
1️⃣ Start Sharing
```bash
nullshare share myfile.pdf
```
2️⃣ Scan QR Code

- Open phone camera

- Scan QR code from terminal
  <p align="center"> <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/images/Screenshot%20From%202026-01-07%2016-29-04.png" width="400" alt="QR Code Interface"> </p>

- Ensure same WiFi network

3️⃣ Download

- Browser opens automatically

- Tap download
  <p align="center"> <img src="https://raw.githubusercontent.com/MOUKA-513/NullShare/main/images/Screenshot%20From%202026-01-07%2016-29-54.png" width="400" alt="Download Interface"> </p>
- Transfer at WiFi speed


### 🛠️ CLI Commands

- Share Files/Folders
```bash
nullshare share <file1> <file2> ...
```
| Option              | Description            | Default |
| ------------------- | ---------------------- | ------- |
| `--port PORT`       | Port to use (0 = auto) | 0       |
| `--no-zip`          | Don't zip folders      | False   |
| `--password TEXT`   | Password protection    | None    |
| `--timeout SECONDS` | Auto-stop              | 300     |
| `--one-time`        | Download once          | False   |
| `--no-qr`           | Hide QR code           | False   |
| `--clean`           | Clear screen           | False   |
| `--verbose`         | Verbose output         | False   |

- Help
```bash
nullshare --help
nullshare share --help
```
### 🛠️ CLI Commands

```bash
nullshare share image1.jpg image2.png document.pdf
nullshare share .
nullshare share --port 9090 file.txt
nullshare share --password mypass secret.pdf
nullshare share --one-time invoice.pdf
```
### 🏗️ Architecture

```bash
┌─────────────┐     QR Code     ┌─────────────┐
│   Desktop   │────────────────▶│    Phone    │
│   (Server)  │◀──WiFi Transfer │  (Browser)  │
└─────────────┘                 └─────────────┘
       │                               │
  Python + Flask                 Mobile Browser
       │                               │
  Local HTTP Server             Web Interface
```
## Flow:
  1. CLI starts local Flask server
  2. QR code generated with IP + port
  3. Phone connects via browser
  4. File transfers over WiFi
  5. Server auto-stops 

### 🔧 Development
- Setup
```bash
git clone https://github.com/MOUKA-513/NullShare.git
cd NullShare
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
```
- Testing & Quality
```bash
pytest
black nullshare/
flake8 nullshare/
mypy nullshare/
```
###📁 Project Structure
```bash
NullShare/
├── nullshare/
│   ├── cli.py
│   ├── server.py
│   ├── qr_generator.py
│   ├── utils.py
│   └── templates/
├── tests/
├── examples/
├── images/
├── pyproject.toml
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```
### 🤝 Contributing
 - Report bugs
 - Suggest features
 - Submit pull requests
 - Improve documentation
   
### 🐛 Troubleshooting
## Phone can't connect
 - Same WIFI
 - Check firewall
 - Disable VPN
## QR not working
 - Ensure http://
 - Good lighting
## Slow transfer
 - Large files take time
 - Check WIFI signal

### 📄 License
MIT License ---- see _LICENSE_ file.
### 🙏 Acknowledgments
Inspired by Snapdrop & LocalSend
Built with Flask, Click, QRCode
### 📞 Support
 - 📧 Issues: GitHub Issues
 - ⭐ Star the repo if you like it!
<div align="center"> <p><strong>Made with ❤️ by <a href="https://github.com/MOUKA-513">MOUKA-513</a></strong></p> <p> <a href="https://github.com/MOUKA-513/NullShare/stargazers"> <img src="https://img.shields.io/github/stars/MOUKA-513/NullShare?style=social"> </a> <a href="https://github.com/MOUKA-513/NullShare/forks"> <img src="https://img.shields.io/github/forks/MOUKA-513/NullShare?style=social"> </a> </p> </div>






