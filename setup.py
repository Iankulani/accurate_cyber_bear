#!/usr/bin/env python3
"""Setup script for Accurate Cyber Bear"""

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="accurate-cyber-bear",
    version="3.0.0",
    author="Ian Carter Kulani",
    author_email="ian@cyberbear.security",
    description="Ultimate Cybersecurity Command Center with Multi-Platform Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iank/accurate-cyber-bear",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cyber-bear=accurate_cyber_bear:main",
            "cbear=accurate_cyber_bear:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)