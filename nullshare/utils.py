"""
Utility functions for NullShare
"""
import socket
import netifaces
import os
import sys
from pathlib import Path
from typing import List, Optional
import platform

def get_local_ip() -> str:
    """
    Get the local IP address of the machine.
    Tries multiple methods to get a non-localhost IP.
    """
    # Method 1: Try socket connection
    try:
        # Connect to a dummy address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # Doesn't actually connect
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
        s.close()
        if ip and ip != '127.0.0.1':
            return ip
    except Exception:
        pass
    
    # Method 2: Use netifaces to find first non-local IP
    try:
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr.get('addr', '')
                    if ip and not ip.startswith('127.'):
                        return ip
    except Exception:
        pass
    
    # Method 3: Fallback
    return '127.0.0.1'

def find_available_port(start_port: int = 8000, max_attempts: int = 100) -> int:
    """
    Find an available port starting from start_port.
    """
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports found in range {start_port}-{start_port + max_attempts}")

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def validate_paths(paths: List[str]) -> List[Path]:
    """
    Validate that paths exist and return Path objects.
    """
    valid_paths = []
    for path_str in paths:
        path = Path(path_str).expanduser().resolve()
        if not path.exists():
            print(f"Warning: Path does not exist: {path}")
            continue
        valid_paths.append(path)
    return valid_paths

def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if is_windows() else 'clear')
