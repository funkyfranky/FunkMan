"""
Utilities
"""

import csv
import numpy as np

def _GetVal(table, key, nil="", precision=None):
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
            if precision!=None:
                return str(round(value, precision))
            else:
                return value
    else:
        return nil

def ReadTrapsheet(filename: str) -> dict:
    """Read a trap sheet into a dictionary as numpy arrays."""

    print(f"Reading trap sheet from file={filename}")

    d={}
    try:
        with open(filename) as f:

            # Read csv.
            reader = csv.DictReader(f)

            # Init array.
            for k in reader.fieldnames:
                d[k]=np.array([])

            for row in reader:
                for k in reader.fieldnames:
                    svalue = row[k]
                    try:
                        fvalue = float(svalue)
                        if k=="X":
                            # Invert X. The re-inversion is done in funkplot now.
                            fvalue=-fvalue
                        elif k=="Alt":
                            # Convert altitude from feet to meters. Back conversion is done in funkplot now.
                            fvalue=fvalue*0.3048
                        d[k] = np.append(d[k], fvalue)
                    except ValueError:
                        d[k]=svalue
    except:
        print('ERROR!')

    return d