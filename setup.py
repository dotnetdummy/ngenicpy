"""Setup script for Ngenicpy package."""

from setuptools import find_packages, setup

with open("README.md", "r", -1, "utf-8") as f:
    long_description = f.read()

setup(
    name="ngenicpy",
    version="0.4.0",
    description="Python package for simple access to Ngenic Tune API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carl Ripa",
    author_email="cj.ripa@gmail.com",
    url="https://github.com/dotnetdummy/ngenicpy",
    packages=find_packages(exclude=["tests"]),
    install_requires=["httpx>=0.28.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
