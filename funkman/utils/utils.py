"""
Utilities
"""

import csv
import numpy as np

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

def ReadTrapsheet(filename: str):
    """
    Read a trap sheet into a dictionary as numpy arrays.
    """        
    d={}
    try:
        with open(filename) as f:
            reader = csv.DictReader(f)

            for k in reader.fieldnames:
                d[k]=np.array([])

            for row in reader:
                for k in reader.fieldnames:
                    svalue = row[k]
                    try:
                        fvalue = float(svalue)
                        #print("float value: ", fvalue)
                        d[k] = np.append(d[k],fvalue)
                    except ValueError:
                        #print("Not a float", svalue)
                        d[k]=svalue
    except:
        print('ERROR!')

    return d