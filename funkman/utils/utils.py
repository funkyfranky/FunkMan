"""
Utilities
"""

def _GetVal(table, key, nil=""):
    """
    Get table value.
    """
    if key in table:
        value=table[key]
        if value=="false":
            return False
        elif value=="true":
            return True
        else:
            return value
    else:
        return nil
