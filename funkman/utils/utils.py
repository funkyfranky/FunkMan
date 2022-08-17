"""
Utilities
"""

import configparser
import os

def hallo():
    print("Hallo from utils!")

def _GetVal(table, key, nil=""):
    """
    Get table value.
    """
    if key in table:
        return table[key]
    else:
        return nil
