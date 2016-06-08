# calcJaneCost.py
#
# Weiyun Ma
# May 2016
#
# This file calculates the total cost of the reconciliation for 
# each file in the janeOut folder. It writes the results
# into corresponding .txt files in the janeCosts folder.
#
# Run with
#   python calcJaneCost.py

import os
import os.path
from cStringIO import StringIO

# Global variables (can be customized in the future)
#dVal = 2
#tVal = 3
#lVal = 1

def janeCost(janeOutFile, dVal, tVal, lVal):

    File = open(janeOutFile, 'r')

    ans = 0

    for line in File:
        if line.startswith("Duplication: "):
            num = int(line[13:])
            ans += num * dVal
        elif line.startswith("Host Switch: "):
            num = int(line[12:])
            ans += num * tVal
        elif line.startswith("Loss: "):
            num = int(line[6:])
            ans += num * lVal
    return ans
