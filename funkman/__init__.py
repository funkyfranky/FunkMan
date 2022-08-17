__doc__ = """
FunkMan
========
A package to link DCS and Discord via MOOSE.
"""

__author__ = """Frank von Horsten"""
__version__ = "0.0.1"

#print("__init__ main")

# Import subpackages
from funkman.funkbot import funkbot   # noqa : F401
from funkman import funkplot  # noqa : F401
from funkman import funksock  # noqa : F401
from funkman import utils     # noqa : F401