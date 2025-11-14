"""
Setup configuration for BrandManager (Topic Research Tool)
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="brand-manager",
    version="0.1.0",
    author="Brand Manager Team",
    description="AI-powered content topic research tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cassandramjaime/BrandManager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "topic-research=brand_manager.cli:main",
            "journalist-finder=brand_manager.journalist_cli:main",
        ],
    },
)
