"""
Utilities
"""

def _GetVal(table, key, nil=""):
    """
    Get table value.
    """
    if key in table:
        return table[key]
    else:
        return nil
