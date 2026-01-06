#!/usr/bin/env python3
"""
Example usage of NullShare
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Demonstrate different ways to use NullShare."""
    
    print("NullShare Examples")
    print("=" * 50)
    
    # Create a test file
    test_file = Path("test_document.txt")
    test_file.write_text("This is a test file for NullShare.\nYou can share any file!")
    
    print("\n1. Basic file sharing:")
    print(f"   nullshare share {test_file.name}")
    
    print("\n2. Share with password:")
    print("   nullshare share --password secret sensitive.pdf")
    
    print("\n3. Share folder (auto-zip):")
    print("   nullshare share ~/Documents/Project/")
    
    print("\n4. Share with timeout (10 minutes):")
    print("   nullshare share --timeout 600 large_file.iso")
    
    print("\n5. One-time download only:")
    print("   nullshare share --one-time temporary_file.tmp")
    
    print("\n6. Custom port:")
    print("   nullshare share --port 9090 file.txt")
    
    # Clean up
    test_file.unlink()
    
    print("\n" + "=" * 50)
    print("Try running these commands to get started!")

if __name__ == "__main__":
    main()
