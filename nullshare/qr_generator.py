"""
QR Code generation and display for NullShare
"""
import qrcode
from qrcode.constants import ERROR_CORRECT_L
from typing import Optional
import sys
import os

def generate_qr_terminal(url: str) -> str:
    """
    Generate and display QR code in terminal using ASCII.
    Returns the QR code as a string.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_matrix = qr.get_matrix()
    border = 1
    qr_text = ""
    
    # Top border
    qr_text += "┌" + "─" * (len(qr_matrix[0]) + 2) + "┐\n"
    
    # Add top padding
    for _ in range(border):
        qr_text += "│" + " " * (len(qr_matrix[0]) + 2) + "│\n"
    
    # QR content
    for row in qr_matrix:
        qr_text += "│ "
        for bit in row:
            qr_text += "██" if bit else "  "
        qr_text += " │\n"
    
    # Add bottom padding
    for _ in range(border):
        qr_text += "│" + " " * (len(qr_matrix[0]) + 2) + "│\n"
    
    # Bottom border
    qr_text += "└" + "─" * (len(qr_matrix[0]) + 2) + "┘"
    
    return qr_text

def generate_qr_image(url: str, save_path: Optional[str] = None):
    """
    Generate QR code as an image.
    If save_path is provided, save the image.
    Returns the QR code image object.
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
