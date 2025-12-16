"""
Setup configuration for HERE Traffic SDK
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version: str
version_ns = {}
with open("here_traffic_sdk/_version.py", "r", encoding="utf-8") as fh:
    exec(fh.read(), version_ns)
version = version_ns["__version__"]

setup(
    name="here-traffic-sdk",
    version=version,
    author="HERE Traffic SDK Contributors",
    description="Python SDK for HERE Traffic and Incident APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/here-traffic-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0,<9.0.0",
            "pytest-cov>=4.1.0,<6.0.0",
            "pytest-mock>=3.11.1,<4.0.0",
            "black>=23.0.0,<25.0.0",
            "mypy>=1.0.0,<2.0.0",
        ],
    },
)

