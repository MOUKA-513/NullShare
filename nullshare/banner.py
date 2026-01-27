"""
 NullShare Banner display 
"""
import click
import shutil
from . import __version__

def get_terminal_width():

    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def show_banner():

    banner = r"""
        )           (     (       (        )           (
 ( /(           )\ )  )\ )    )\ )  ( /(   (       )\  )
 )\())     (   (()/(  (()/(  (()/(  )\())  )\     (()/(  (
((_)\      )\   /(_))  /(_)) /(_))((_)\((((_)(      /(_)))\
 _((_) _  ((_) (_))   (_))  (_))    _((_))\ _ )\   (_)) ((_)
| \| | | | | | | | |  | |   / __|  |  | |(_)_ \(_) | _ \| __|
| .` | | |_| | | |__  | |__ \__ \  | __ |  / _ \   |   /| _|
|_|\_|  \___/  |____| |____| |___/ |_||_| /_/ \_\  |_|_\|___|
"""
    
    terminal_width = get_terminal_width()
    lines = banner.strip('\n').split('\n')
    
    click.echo("\n" * 2)
    
    for line in lines:
        if line.strip():
            centered_line = line.center(terminal_width)
            click.echo(click.style(centered_line, fg='red', bold=True))
    
    click.echo("\n" * 2)
    
    creator_text = f"Created by: MOUKA-513"
    version_text = f"Version: {__version__}"
    tagline = "No internet, no cloud, just local WiFi file sharing"
    
    click.echo(click.style(creator_text.center(terminal_width), fg='red', bold=True))
    click.echo(click.style(version_text.center(terminal_width), fg='red', bold=True))
    
    click.echo()
    click.echo(click.style(tagline.center(terminal_width), fg='red'))
    click.echo(click.style("─" * terminal_width, fg='red'))
    click.echo()

def show_share_banner():
    """Display a banner for the share command - ALL IN RED."""
    terminal_width = get_terminal_width()
    border_line = "─" * (terminal_width - 4)
    
    click.echo(click.style(f"┌{border_line}┐", fg='red'))
    click.echo(click.style("│", fg='red') + 
              click.style("   NullShare File Sharing Server   ", fg='red', bold=True).center(terminal_width - 2) + 
              click.style("│", fg='red'))
    click.echo(click.style("│", fg='red') + 
              click.style(f"   Version: {__version__} • MOUKA-513   ", fg='red').center(terminal_width - 2) + 
              click.style("│", fg='red'))
    click.echo(click.style(f"└{border_line}┘", fg='red'))
