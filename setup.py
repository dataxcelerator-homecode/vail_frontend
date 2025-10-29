"""
Setup script for Keyboard Visualizer.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="keyboard-visualizer",
    version="1.0.0",
    author="Keyboard Visualizer Team",
    description="A tool for visualizing Vial keyboard layouts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/keyboard-visualizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.5.0",
        "tqdm>=4.65.0",
        "Flask>=2.3.0",
        "Werkzeug>=2.3.0",
    ],
    entry_points={
        "console_scripts": [
            "keyboard-visualizer=cli:main",
        ],
    },
)

