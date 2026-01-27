"""
  NullShare - Main CLI interface
"""
import click
import os
import sys
from pathlib import Path
from typing import List, Optional
import time

from .server import ShareServer
from .qr_generator import generate_qr_terminal
from .utils import get_local_ip, find_available_port, validate_paths, clear_screen, format_file_size

# Try to import banner, but don't fail if it doesn't exist
try:
    from .banner import show_banner, show_share_banner
    HAS_BANNER = True
except ImportError:
    HAS_BANNER = False

@click.group(invoke_without_command=True)
@click.version_option(version='1.1.0', prog_name='NullShare')
@click.pass_context
def cli(ctx):
    """NullShare - Share files via QR code on local network.
    
    No internet, no cloud, just local WiFi file sharing.
    """
    if ctx.invoked_subcommand is None:
        # Show ASCII art banner if available
        if HAS_BANNER:
            show_banner()
        click.echo(ctx.get_help())

@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.option('--port', '-p', type=int, default=0, help='Port to use (0 = auto)')
@click.option('--no-zip', is_flag=True, help='Do not zip folders, share contents individually')
@click.option('--password', help='Set password protection')
@click.option('--timeout', '-t', type=int, help='Auto-stop after N seconds')
@click.option('--one-time', is_flag=True, help='Files can only be downloaded once')
@click.option('--no-qr', is_flag=True, help='Do not show QR code')
@click.option('--clean', is_flag=True, help='Clear screen before showing QR')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed information')
@click.option('--no-banner', is_flag=True, help='Do not show ASCII banner')
def share(paths, port, no_zip, password, timeout, one_time, no_qr, clean, verbose, no_banner):
    """Share files/folders via QR code."""
    
    if not paths:
        click.echo("\033[93mError: Please specify at least one file or folder to share.\033[0m")
        click.echo("\033[93mExample: nullshare share document.pdf\033[0m")
        sys.exit(1)
    
    # Show banner if not disabled and available
    if not no_banner and HAS_BANNER:
        if clean:
            clear_screen()
        show_share_banner()
        click.echo()
    
    # Validate paths
    valid_paths = validate_paths(paths)
    if not valid_paths:
        click.echo("\033[93mError: No valid paths to share.\033[0m")
        sys.exit(1)
    
    # Clear screen if requested (and banner not shown)
    if clean and (no_banner or not HAS_BANNER):
        clear_screen()
    
    # Find available port if not specified
    if port == 0:
        port = find_available_port()
    
    # Start the server
    server = ShareServer(
        paths=valid_paths,
        port=port,
        zip_folders=not no_zip,
        password=password,
        timeout=timeout,
        one_time=one_time
    )
    
    try:
        server.start()
    except Exception as e:
        click.echo(f"\033[93mError starting server: {e}\033[0m")
        sys.exit(1)
    
    # Get server URL
    ip = get_local_ip()
    url = server.get_url(ip)
    
    # Display information
    click.echo("\n" + "\033[91m=\033[0m"*60)
    click.echo("\033[91m       NullShare--File Sharing Infos!!\033[0m")
    click.echo("\033[91m=\033[0m"*60)
    
    click.echo(f"\n\033[91m+++ Server IP:   {click.style(ip, fg='cyan', bold=True)}\033[0m")
    click.echo(f"\033[91m+++ Port:       {click.style(str(port), fg='cyan', bold=True)}\033[0m")
    click.echo(f"\033[91m+++ URL:        {click.style(url, fg='cyan', underline=True, bold=True)}\033[0m")
    
    if password:
        click.echo(f"\033[91m+++ Password:   {click.style('Enabled', fg='cyan', bold=True)}\033[0m")
        click.echo(f"\033[91m+++ Token:      {click.style(server.access_token, fg='cyan', bold=True)}\033[0m")
    
    # Display files
    click.echo(f"\n\033[91m>>>> Sharing {click.style(str(len(valid_paths)), fg='cyan', bold=True)} item(s):\033[0m")
    for i, path in enumerate(valid_paths, 1):
        if path.is_file():
            size = format_file_size(path.stat().st_size)
            click.echo(f"\033[94m  {i}. File: {path.name} ({size})\033[0m")
        else:
            file_count = len(list(path.rglob('*')))
            click.echo(f"  {i}. Folder: {path.name}/ ({file_count} files)")
    
    # Display QR code
    if not no_qr:
        click.echo("\n\033[91m>>>> Scan this QR code with your phone camera:\033[0m")
        qr_text = generate_qr_terminal(url)
        click.echo(qr_text)
    
    click.echo("\n\033[91m>>>>>> Transfer Status:\033[0m")
    click.echo("\033[91m  • Connect phone to same WiFi\033[0m")
    click.echo("\033[91m  • Scan QR code or visit URL\033[0m")
    click.echo("\033[91m  • Download files directly to phone\033[0m")
    
    if timeout:
        click.echo(f"\n\033[91m>>>> Server will auto-stop in **{timeout}** seconds\033[0m")
    
    click.echo("\n" + "\033[93m=\033[0m"*60)
    click.echo("\n\033[93m   Press Ctrl+C to stop sharing\033[0m")
    click.echo("\033[93m=\033[0m"*60 + "\n")
    
    try:
        # Keep server running
        if verbose:
            click.echo("\n\033[91m*****Verbose mode: Server is running....\033[0m")
            start_time = time.time()
            download_count = 0
        
        while True:
            time.sleep(1)
            if verbose:
                current_time = time.time()
                elapsed = int(current_time - start_time)
                # Show stats every 10 seconds
                if elapsed % 10 == 0:
                    click.echo(f"[{elapsed}s] Server running - Downloads: {server.stats['total_downloads']}")
    except KeyboardInterrupt:
        click.echo("\n\n\033[93mStopping server...\033[0m")
        server.stop()
        click.echo("\033[93mServer stopped successfully!\033[0m")
        sys.exit(0)

@cli.command()
@click.option('--port', '-p', type=int, default=8000, help='Port to check')
@click.option('--json', '-j', is_flag=True, help='Output in JSON format')
def status(port, json):
    """Check if a NullShare server is running."""
    try:
        import requests
        response = requests.get(f'http://127.0.0.1:{port}/api/status', timeout=2)
        if response.status_code == 200:
            data = response.json()
            if json:
                import json as json_module
                click.echo(json_module.dumps(data, indent=2))
            else:
                click.echo(f"✓ NullShare server is running on port {port}")
                click.echo(f"  Files being shared: {data['files_count']}")
                click.echo(f"  Uptime: {data['uptime']}")
                click.echo(f"  Total downloads: {data['total_downloads']}")
                click.echo(f"  Unique clients: {data['unique_clients']}")
        else:
            if json:
                click.echo('{"status": "not_found", "port": ' + str(port) + '}')
            else:
                click.echo(f"\033[93m✗ No NullShare server found on port {port}\033[0m")
    except:
        if json:
            click.echo('{"status": "not_found", "port": ' + str(port) + '}')
        else:
            click.echo(f"\033[93m✗ No NullShare server found on port {port}\033[0m")

@cli.command()
@click.option('--port', '-p', type=int, default=8000, help='Port to stop')
@click.option('--force', '-f', is_flag=True, help='Force stop without confirmation')
def stop(port, force):
    """Stop a running NullShare server."""
    try:
        import requests
        if not force:
            click.confirm(f"\033[93mAre you sure you want to stop the server on port {port}?\033[0m", abort=True)
        
        response = requests.get(f'http://127.0.0.1:{port}/shutdown', timeout=2)
        if response.status_code == 200:
            click.echo(f"✓ NullShare server on port {port} stopped successfully")
        else:
            click.echo(f"✗ Could not stop server on port {port}")
    except:
        click.echo(f"✗ No NullShare server found on port {port}")

@cli.command()
@click.option('--scan', '-s', is_flag=True, help='Scan network for servers')
def discover(scan):
    """Discover NullShare servers on local network."""
    if not scan:
        click.echo("Discovering NullShare servers on local network...")
        click.echo("\nOptions:")
        click.echo("  --scan, -s    Scan network for active servers")
        click.echo("\nRun 'nullshare share <file>' to start sharing!")
        return
    
    click.echo("\033[93mScanning local network for NullShare servers...\033[0m")
    click.echo("\033[93m(This may take a few seconds)\n\033[0m")
    
    try:
        import requests
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import socket
        
        # Get local network
        local_ip = get_local_ip()
        network_prefix = ".".join(local_ip.split(".")[:3])
        
        found_servers = []
        
        def check_host(ip):
            try:
                socket.setdefaulttimeout(0.5)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, 8000))
                s.close()
                
                # Try to get status
                response = requests.get(f'http://{ip}:8000/api/status', timeout=1)
                if response.status_code == 200:
                    data = response.json()
                    found_servers.append({
                        'ip': ip,
                        'port': 8000,
                        'files': data['files_count'],
                        'uptime': data['uptime']
                    })
                    return ip
            except:
                pass
            return None
        
        # Scan ports 8000-8010 on network
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(1, 255):
                ip = f"{network_prefix}.{i}"
                futures.append(executor.submit(check_host, ip))
            
            for future in as_completed(futures):
                pass  # Results collected in found_servers
        
        if found_servers:
            click.echo(f"Found {len(found_servers)} NullShare server(s):\n")
            for server in found_servers:
                click.echo(f"  • {server['ip']}:{server['port']}")
                click.echo(f"    Files: {server['files']}, Uptime: {server['uptime']}")
                click.echo(f"    URL: http://{server['ip']}:{server['port']}/")
                click.echo()
        else:
            click.echo("No NullShare servers found on the network.")
            click.echo("\nTo start sharing: nullshare share <file>")
            
    except Exception as e:
        click.echo(f"Error scanning network: {e}")
        click.echo("\nRun 'nullshare share <file>' to start sharing!")

@cli.command()
@click.option('--update', is_flag=True, help='Check for updates')
def version(update):
    """Show version information and check for updates."""
    from . import __version__
    
    click.echo(f"NullShare v{__version__}")
    click.echo("Created by MOUKA-513")
    click.echo("No internet, no cloud, just local WiFi file sharing")
    
    if update:
        click.echo("\nChecking for updates...")
        try:
            import requests
            # Try to get latest version from PyPI or GitHub
            response = requests.get('https://pypi.org/pypi/nullshare/json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data['info']['version']
                if latest_version != __version__:
                    click.echo(f"\nUpdate available: v{__version__} → v{latest_version}")
                    click.echo("Run: pip install --upgrade nullshare")
                else:
                    click.echo("✓ You have the latest version!")
            else:
                click.echo("Could not check for updates. Check manually:")
                click.echo("  https://github.com/MOUKA-513/NullShare")
        except:
            click.echo("Could not connect to update server.")

@cli.command()
@click.argument('url')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def download(url, output):
    """Download files from a NullShare server URL."""
    try:
        import requests
        from urllib.parse import urlparse
        
        click.echo(f"Downloading from: {url}")
        
        if output:
            output_path = Path(output)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = Path.cwd()
        
        # Try to get file list
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            # Simple download - in real app, parse HTML for file list
            click.echo("Connected to server!")
            click.echo("(Note: Direct download from CLI is not fully implemented)")
            click.echo("Visit the URL in your browser to download files.")
        else:
            click.echo("Could not connect to server.")
            
    except Exception as e:
        click.echo(f"Error: {e}")

def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
