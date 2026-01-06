from setuptools import setup, find_packages

setup(
    name="nullshare",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "flask>=2.3.0",
        "qrcode>=7.4.0",
        "pillow>=10.0.0",
        "colorama>=0.4.6",
        "netifaces>=0.11.0",
    ],
    entry_points={
        "console_scripts": [
            "nullshare=nullshare.cli:main",
        ],
    },
    python_requires=">=3.8",
)
