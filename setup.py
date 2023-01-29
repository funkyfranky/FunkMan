# Import
from setuptools import setup, find_packages

# Call setup funtion
setup(
    author="funkyfranky",
    description="Interface between DCS/MOOSE and Discord via an UDP socket.",
    name="funkman",
    version="0.6.3",
    packages=find_packages(include=["funkman", "funkman.*"]),
    install_requires=[
        'discord>=2.0.0',
        'matplotlib',
        'numpy']
)