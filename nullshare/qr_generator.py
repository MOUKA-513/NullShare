"""
NullShare QR Code generation and display
"""
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from typing import Optional, Dict, Any
import sys
import os
import io
import click
from PIL import Image

# Error correction levels mapping
ERROR_LEVELS = {
    'L': ERROR_CORRECT_L,  # 7% correction
    'M': ERROR_CORRECT_M,  # 15% correction
    'Q': ERROR_CORRECT_Q,  # 25% correction
    'H': ERROR_CORRECT_H,  # 30% correction
}


def generate_qr_terminal(url: str, box_size: int = 1, border: int = 1) -> str:
    """
    Generate and display QR code in terminal using ASCII.
    Returns the QR code as a string.
    
    Args:
        url: The URL to encode in the QR code
        box_size: Size of each QR module (default: 1)
        border: Border size around QR code (default: 1)
    
    Returns:
        ASCII representation of QR code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_matrix = qr.get_matrix()
    qr_text = ""
    
    # Top border
    qr_text += "┌" + "─" * (len(qr_matrix[0]) + border * 2) + "┐\n"
    
    # Add top padding
    for _ in range(border):
        qr_text += "│" + " " * (len(qr_matrix[0]) + border * 2) + "│\n"
    
    # QR content
    for row in qr_matrix:
        qr_text += "│" + " " * border
        for bit in row:
            qr_text += "██" if bit else "  "
        qr_text += " " * border + "│\n"
    
    # Add bottom padding
    for _ in range(border):
        qr_text += "│" + " " * (len(qr_matrix[0]) + border * 2) + "│\n"
    
    # Bottom border
    qr_text += "└" + "─" * (len(qr_matrix[0]) + border * 2) + "┘"
    
    return qr_text


def generate_colored_qr_terminal(
    url: str,
    color: str = "green",
    bg_color: str = None,
    box_size: int = 1
) -> str:
    """
    Generate colored QR code for terminal display.
    
    Args:
        url: The URL to encode in the QR code
        color: Foreground color name
        bg_color: Background color name
        box_size: Size of each QR module
    
    Returns:
        Colored ASCII representation of QR code
    """
    # Color mapping
    colors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
        'bright_black': '90',
        'bright_red': '91',
        'bright_green': '92',
        'bright_yellow': '93',
        'bright_blue': '94',
        'bright_magenta': '95',
        'bright_cyan': '96',
        'bright_white': '97',
    }
    
    if color not in colors:
        color = 'green'
    
    fg_code = colors[color]
    bg_code = f'48;5;232' if bg_color == 'black' else ''
    
    qr_text = generate_qr_terminal(url, box_size=box_size)
    
    # Colorize the QR code
    colored_lines = []
    for line in qr_text.split('\n'):
        colored_line = ""
        for char in line:
            if char == '█':
                if bg_code:
                    colored_line += f'\033[{fg_code};{bg_code}m{char}\033[0m'
                else:
                    colored_line += f'\033[{fg_code}m{char}\033[0m'
            elif char in ('┌', '┐', '└', '┘', '─', '│'):
                # Borders in cyan
                colored_line += f'\033[36m{char}\033[0m'
            else:
                colored_line += char
        colored_lines.append(colored_line)
    
    return '\n'.join(colored_lines)


def generate_qr_image(
    url: str, 
    save_path: Optional[str] = None,
    size: int = 400,
    fill_color: str = "black",
    back_color: str = "white",
    error_correction: str = "L",
    logo_path: Optional[str] = None,
    logo_size: float = 0.2
) -> Image.Image:
    """
    Generate QR code as PIL Image.
    
    Args:
        url: URL to encode
        save_path: Optional path to save image
        size: Image size in pixels
        fill_color: QR code color
        back_color: Background color
        error_correction: Error correction level (L, M, Q, H)
        logo_path: Optional logo to overlay
        logo_size: Logo size as fraction of QR code
    
    Returns:
        PIL Image object
    """
    if not url or len(url) == 0:
        raise ValueError("URL cannot be empty")
    
    try:
        # Get error correction level
        ec_level = ERROR_LEVELS.get(error_correction.upper(), ERROR_CORRECT_L)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=ec_level,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(
            fill_color=fill_color,
            back_color=back_color
        )
        
        # Resize to requested size
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Add logo if specified
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                logo_size_px = int(size * max(0.1, min(0.3, logo_size)))
                
                # Resize logo
                logo.thumbnail((logo_size_px, logo_size_px), Image.Resampling.LANCZOS)
                
                # Calculate position to center logo
                pos = ((img.size[0] - logo.size[0]) // 2, 
                       (img.size[1] - logo.size[1]) // 2)
                
                # Create a white background for logo (optional)
                logo_bg = Image.new('RGB', logo.size, back_color)
                logo_bg.paste(logo, (0, 0), logo if logo.mode == 'RGBA' else None)
                
                # Paste logo onto QR code
                img.paste(logo_bg, pos)
            except Exception as e:
                print(f"Warning: Could not add logo: {e}")
        
        # Save if path provided
        if save_path:
            save_dir = os.path.dirname(save_path)
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir)
            img.save(save_path)
            print(f"QR code saved to: {save_path}")
        
        return img
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate QR image: {e}")


def generate_qr_image_to_bytes(
    url: str,
    format: str = "PNG",
    **kwargs
) -> bytes:
    """
    Generate QR code and return as bytes.
    
    Args:
        url: URL to encode
        format: Image format (PNG, JPEG, etc.)
        **kwargs: Additional arguments for generate_qr_image
    
    Returns:
        Image bytes
    """
    img = generate_qr_image(url, **kwargs)
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    
    return buffer.getvalue()


def display_qr_in_terminal(
    url: str,
    show_instructions: bool = True,
    show_url: bool = True
) -> None:
    """
    Display QR code with instructions in terminal.
    
    Args:
        url: URL to display as QR code
        show_instructions: Whether to show usage instructions
        show_url: Whether to show the URL text
    """
    # Generate and display QR code
    try:
        qr_text = generate_colored_qr_terminal(url, color="green", box_size=1)
        
        # Clear line and display
        click.echo("\n" + "═" * 60)
        click.echo("Scan QR code with your phone:")
        click.echo("═" * 60 + "\n")
        click.echo(qr_text)
        
        if show_url:
            click.echo(f"\nURL: {click.style(url, fg='cyan', underline=True)}")
        
        if show_instructions:
            click.echo("\nInstructions:")
            click.echo("  • Ensure phone is on same WiFi network")
            click.echo("  • Open camera app and point at QR code")
            click.echo("  • Tap notification to open link")
            click.echo("  • Download files directly to phone")
        
        click.echo("\n" + "═" * 60)
        
    except Exception as e:
        click.echo(f"Error generating QR code: {e}", err=True)
        click.echo(f"URL to share: {url}")


def generate_qr_for_clipboard(url: str) -> str:
    """
    Generate QR code text for clipboard.
    
    Args:
        url: URL to encode
    
    Returns:
        ASCII QR code text
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        qr_matrix = qr.get_matrix()
        qr_text = ""
        
        for row in qr_matrix:
            for bit in row:
                qr_text += "██" if bit else "  "
            qr_text += "\n"
        
        return qr_text
        
    except Exception as e:
        return f"[QR Code Error: {e}]"


# For backward compatibility with original code
def generate_qr_image_simple(url: str, save_path: Optional[str] = None) -> Image.Image:
    """
    Simple QR code generator (legacy function).
    
    Args:
        url: URL to encode
        save_path: Optional path to save image
    
    Returns:
        PIL Image object
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    if save_path:
        img.save(save_path)
    
    return img


# Test function
if __name__ == "__main__":
    # Test the QR code generator
    test_url = "https://example.com"
    
    print("Testing QR Code Generator\n")
    
    # Test 1: Simple terminal QR
    print("1. Simple Terminal QR:")
    print(generate_qr_terminal(test_url))
    
    print("\n" + "="*60 + "\n")
    
    # Test 2: Colored terminal QR
    print("2. Colored Terminal QR:")
    print(generate_colored_qr_terminal(test_url, color="blue"))
    
    print("\n" + "="*60 + "\n")
    
    # Test 3: Display with instructions
    print("3. Full Display with Instructions:")
    display_qr_in_terminal(test_url)
    
    # Test 4: Generate image (save to file)
    print("\n4. Generating image file...")
    try:
        img = generate_qr_image(
            test_url, 
            save_path="test_qr.png",
            size=300,
            fill_color="blue",
            back_color="white"
        )
        print(f"Image generated: {img.size} pixels")
    except Exception as e:
        print(f"Error generating image: {e}")
