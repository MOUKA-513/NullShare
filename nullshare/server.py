"""
HTTP Server for NullShare
"""
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import zipfile
import io
import threading
import time
from datetime import datetime
import hashlib
import secrets

try:
    from flask import Flask, send_file, render_template, abort, request, jsonify
except ImportError:
    print("Error: Flask is not installed. Install it with: pip install flask")
    sys.exit(1)

class ShareServer:
    """HTTP server for sharing files."""
    
    def __init__(
        self,
        paths: List[Path],
        port: int = 8000,
        zip_folders: bool = True,
        password: Optional[str] = None,
        timeout: Optional[int] = None,
        live_mode: bool = False,
        one_time: bool = False
    ):
        self.paths = paths
        self.port = port
        self.zip_folders = zip_folders
        self.password = password
        self.timeout = timeout
        self.live_mode = live_mode
        self.one_time = one_time
        self.downloaded_files = set()
        
        # Generate access token if password is set
        self.access_token = secrets.token_urlsafe(16) if password else None
        
        # Statistics
        self.stats = {
            'start_time': datetime.now(),
            'total_requests': 0,
            'total_downloads': 0,
            'clients': set()
        }
        
        # Create Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
        
        # Set up routes
        self._setup_routes()
        
        # Server thread
        self.server_thread: Optional[threading.Thread] = None
        self.running = False
        
    def _setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.before_request
        def before_request():
            self.stats['total_requests'] += 1
            self.stats['clients'].add(request.remote_addr)
            
            # Check password if set
            if self.password and self.access_token:
                token = request.args.get('token')
                if token != self.access_token:
                    return "Unauthorized: Invalid or missing token", 401
        
        @self.app.route('/')
        def index():
            """Main page showing files."""
            files_info = self._get_files_info()
            return render_template(
                'index.html',
                files=files_info,
                total_files=len(files_info),
                server_start=self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S'),
                access_token=self.access_token
            )
        
        @self.app.route('/download/<path:filename>')
        def download_file(filename):
            """Download a file."""
            file_path = self._find_file_path(filename)
            
            if not file_path:
                abort(404, description="File not found")
            
            if self.one_time and filename in self.downloaded_files:
                abort(410, description="File was already downloaded and removed")
            
            self.stats['total_downloads'] += 1
            
            if self.one_time:
                self.downloaded_files.add(filename)
            
            if file_path.is_dir() and self.zip_folders:
                return self._send_zipped_folder(file_path)
            
            return send_file(
                str(file_path),
                as_attachment=True,
                download_name=file_path.name
            )
        
        @self.app.route('/api/status')
        def api_status():
            """API endpoint for server status."""
            return jsonify({
                'status': 'running',
                'port': self.port,
                'files_count': len(self._get_files_info()),
                'uptime': str(datetime.now() - self.stats['start_time']),
                'total_requests': self.stats['total_requests'],
                'total_downloads': self.stats['total_downloads'],
                'unique_clients': len(self.stats['clients'])
            })
        
        @self.app.route('/shutdown')
        def shutdown():
            """Endpoint to shutdown the server."""
            if request.remote_addr in ['127.0.0.1', 'localhost']:
                self.stop()
                return 'Server shutting down...'
            return 'Unauthorized', 403
    
    def _get_files_info(self) -> List[Dict[str, Any]]:
        """Get information about all shared files."""
        files_info = []
        
        for path in self.paths:
            if path.is_file():
                size = path.stat().st_size
                files_info.append({
                    'name': path.name,
                    'size': size,
                    'size_human': self._format_size(size),
                    'type': 'file',
                    'url': f'/download/{path.name}'
                })
            elif path.is_dir():
                if self.zip_folders:
                    # Calculate total size of folder
                    total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                    files_info.append({
                        'name': f'{path.name}.zip',
                        'size': total_size,
                        'size_human': self._format_size(total_size),
                        'type': 'folder',
                        'url': f'/download/{path.name}.zip',
                        'file_count': len(list(path.rglob('*')))
                    })
                else:
                    # List all files in folder
                    for file_path in path.rglob('*'):
                        if file_path.is_file():
                            size = file_path.stat().st_size
                            rel_path = file_path.relative_to(path)
                            files_info.append({
                                'name': str(rel_path),
                                'size': size,
                                'size_human': self._format_size(size),
                                'type': 'file',
                                'url': f'/download/{rel_path}'
                            })
        
        return files_info
    
    def _find_file_path(self, filename: str) -> Optional[Path]:
        """Find the actual file path from filename."""
        for path in self.paths:
            if path.is_file() and path.name == filename:
                return path
            elif path.is_dir():
                # Check for direct file match
                if path.name == filename.replace('.zip', ''):
                    return path
                # Check for nested files
                file_path = path / filename
                if file_path.exists() and file_path.is_file():
                    return file_path
        return None
    
    def _send_zipped_folder(self, folder_path: Path):
        """Create and send a zipped folder."""
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    # Preserve directory structure
                    arcname = file_path.relative_to(folder_path)
                    zf.write(file_path, arcname)
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{folder_path.name}.zip'
        )
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def start(self):
        """Start the HTTP server in a separate thread."""
        if self.running:
            return
        
        self.running = True
        
        # Start server in a thread
        self.server_thread = threading.Thread(
            target=self.app.run,
            kwargs={
                'host': '0.0.0.0',
                'port': self.port,
                'debug': False,
                'threaded': True,
                'use_reloader': False
            },
            daemon=True
        )
        
        self.server_thread.start()
        
        # Set timeout if specified
        if self.timeout:
            def stop_after_timeout():
                time.sleep(self.timeout)
                if self.running:
                    self.stop()
            
            threading.Thread(target=stop_after_timeout, daemon=True).start()
        
        # Wait a moment for server to start
        time.sleep(0.5)
    
    def stop(self):
        """Stop the HTTP server."""
        self.running = False
        
        # Try to shutdown gracefully
        try:
            import requests
            requests.get(f'http://127.0.0.1:{self.port}/shutdown', timeout=1)
        except:
            pass
        
        # Force stop if still running
        if self.server_thread and self.server_thread.is_alive():
            time.sleep(1)
    
    def wait_for_stop(self):
        """Wait for server to stop."""
        if self.server_thread:
            self.server_thread.join()
    
    def get_url(self, ip: str = None) -> str:
        """Get the URL for accessing the server."""
        if not ip:
            from .utils import get_local_ip
            ip = get_local_ip()
        
        if self.access_token:
            return f"http://{ip}:{self.port}/?token={self.access_token}"
        return f"http://{ip}:{self.port}/"
