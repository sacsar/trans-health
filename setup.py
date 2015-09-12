#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name = "trans-health",
    version = "0.1.0",
    packages = find_packages("src/", "tests/"),
    package_dir = {"": "src"},
    setup_requires=["nose>=1.0"],
    install_requires=[
        "coverage",
        "spec",
        "flask",
        "nose"
    ]
)
