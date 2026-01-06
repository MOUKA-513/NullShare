"""
Main CLI interface for NullShare
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

@click.group(invoke_without_command=True)
@click.version_option(version='0.1.0', prog_name='NullShare')
@click.pass_context
def cli(ctx):
    """NullShare - Share files via QR code on local network.
    
    No internet, no cloud, just local WiFi file sharing.
    """
    if ctx.invoked_subcommand is None:
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
def share(paths, port, no_zip, password, timeout, one_time, no_qr, clean, verbose):
    """Share files/folders via QR code."""
    
    if not paths:
        click.echo("Error: Please specify at least one file or folder to share.")
        click.echo("Example: nullshare share document.pdf")
        sys.exit(1)
    
    # Validate paths
    valid_paths = validate_paths(paths)
    if not valid_paths:
        click.echo("Error: No valid paths to share.")
        sys.exit(1)
    
    # Find available port if not specified
    if port == 0:
        port = find_available_port()
    
    # Clear screen if requested
    if clean:
        clear_screen()
    
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
        click.echo(f"Error starting server: {e}")
        sys.exit(1)
    
    # Get server URL
    ip = get_local_ip()
    url = server.get_url(ip)
    
    # Display information
    click.echo("\n" + "="*60)
    click.echo("🚀 NullShare - File Sharing Server Started!")
    click.echo("="*60)
    
    click.echo(f"\n📡 Server IP:   {click.style(ip, fg='cyan', bold=True)}")
    click.echo(f"🔌 Port:       {click.style(str(port), fg='yellow')}")
    click.echo(f"🔗 URL:        {click.style(url, fg='green', underline=True)}")
    
    if password:
        click.echo(f"🔐 Password:   {click.style('Enabled', fg='red')}")
        click.echo(f"🔑 Token:      {click.style(server.access_token, fg='magenta')}")
    
    # Display files
    click.echo(f"\n📁 Sharing {click.style(str(len(valid_paths)), fg='blue', bold=True)} item(s):")
    for i, path in enumerate(valid_paths, 1):
        if path.is_file():
            size = format_file_size(path.stat().st_size)
            click.echo(f"  {i}. 📄 {path.name} ({size})")
        else:
            file_count = len(list(path.rglob('*')))
            click.echo(f"  {i}. 📁 {path.name}/ ({file_count} files)")
    
    # Display QR code
    if not no_qr:
        click.echo("\n📱 Scan this QR code with your phone camera:")
        qr_text = generate_qr_terminal(url)
        click.echo(qr_text)
    
    click.echo("\n⚡ Transfer Status:")
    click.echo("  • Connect phone to same WiFi")
    click.echo("  • Scan QR code or visit URL")
    click.echo("  • Download files directly to phone")
    
    if timeout:
        click.echo(f"\n⏱️  Server will auto-stop in {timeout} seconds")
    
    click.echo("\n" + "="*60)
    click.echo("Press Ctrl+C to stop sharing")
    click.echo("="*60 + "\n")
    
    try:
        # Keep server running
        while True:
            time.sleep(1)
            if verbose:
                # Show stats every 10 seconds
                pass
    except KeyboardInterrupt:
        click.echo("\n\n🛑 Stopping server...")
        server.stop()
        click.echo("✅ Server stopped successfully!")
        sys.exit(0)

@cli.command()
@click.option('--port', '-p', type=int, default=8000, help='Port to check')
def status(port):
    """Check if a NullShare server is running."""
    try:
        import requests
        response = requests.get(f'http://127.0.0.1:{port}/api/status', timeout=2)
        if response.status_code == 200:
            data = response.json()
            click.echo(f"✅ NullShare server is running on port {port}")
            click.echo(f"📁 Files being shared: {data['files_count']}")
            click.echo(f"⏱️  Uptime: {data['uptime']}")
            click.echo(f"📊 Total downloads: {data['total_downloads']}")
        else:
            click.echo(f"❌ No NullShare server found on port {port}")
    except:
        click.echo(f"❌ No NullShare server found on port {port}")

@cli.command()
@click.option('--port', '-p', type=int, default=8000, help='Port to stop')
def stop(port):
    """Stop a running NullShare server."""
    try:
        import requests
        response = requests.get(f'http://127.0.0.1:{port}/shutdown', timeout=2)
        if response.status_code == 200:
            click.echo(f"✅ NullShare server on port {port} stopped successfully")
        else:
            click.echo(f"❌ Could not stop server on port {port}")
    except:
        click.echo(f"❌ No NullShare server found on port {port}")

@cli.command()
def discover():
    """Discover NullShare servers on local network."""
    click.echo("🔍 Discovering NullShare servers on local network...")
    click.echo("(This feature is not implemented yet)")
    click.echo("\nRun 'nullshare share <file>' to start sharing!")

def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
