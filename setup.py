# Import
from setuptools import setup, find_packages

# Call setup funtion
setup(
    author="funkyfranky",
    description="Interface between DCS/MOOSE and Discord via an UDP socket.",
    name="funkman",
    version="0.3.0",
    packages=find_packages(include=["funkman", "funkman.*"]),
    install_requires=[
        'discord>=1.7.3',
        'matplotlib',
        'numpy']
)