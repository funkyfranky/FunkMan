__doc__ = """
FunkMan
========
A package to link DCS and Discord via MOOSE.
"""

__author__  = "funkyfranky"
__version__ = "0.6.2"

#print("__init__ main")

# Import subpackages
from funkman import funkbot   # noqa : F401
from funkman import funkplot  # noqa : F401
from funkman import funksock  # noqa : F401
from funkman import utils     # noqa : F401

from funkman.funkman import FunkMan
from funkman.funkbot.funkbot import FunkBot
from funkman.funksock.funksock import FunkSocket