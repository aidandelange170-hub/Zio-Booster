"""
Setup script for Zio-Booster FPS Booster
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="zio-booster",
    version="1.0.0",
    author="Zio-Booster Development Team",
    author_email="zio-booster@example.com",
    description="A modern FPS booster application that optimizes your system in the background to increase frame rates and reduce temperature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/Zio-Booster",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zio-booster=src.main:main",
        ],
    },
)