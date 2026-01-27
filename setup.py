#!/usr/bin/env python3
"""Setup script for NullShare."""

from setuptools import setup, find_packages

setup(
    name="nullshare",
    version="1.1.0",
    author="MOUKA-513",
    description="Share files via QR code on local network - no internet, no cloud, just local WiFi.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "nullshare": ["templates/*.html"],
    },
    install_requires=[
        "click>=8.0.0",
        "Flask>=2.0.0",
        "qrcode>=7.0.0",
        "Pillow>=9.0.0",
        "requests>=2.25.0",
        "netifaces>=0.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "nullshare=nullshare.cli:main",
            "ns=nullshare.cli:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "file-sharing",
        "qr-code", 
        "local-network",
        "wifi",
        "flask",
        "cli",
    ],
    project_urls={
        "Homepage": "https://github.com/MOUKA-513/NullShare",
        "Bug Tracker": "https://github.com/MOUKA-513/NullShare/issues",
    },
)
