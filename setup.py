from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openmembase",
    version="1.0.0",
    author="CoPaw",
    author_email="copaw@example.com",
    description="Enterprise Unified Memory Database - Memory-LanceDB + Project KB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/copaw/openmembase",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Database",
    ],
    python_requires=">=3.8",
    install_requires=[
        "lancedb>=0.29.0",
        "numpy>=1.20.0",
        "httpx>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "openmembase=openmembase.cli:cli_main",
        ],
    },
)
