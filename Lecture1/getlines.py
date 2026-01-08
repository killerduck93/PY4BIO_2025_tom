#!/usr/bin/env python

# The 'getlines' program which processes lines.

import sys

for line in sys.stdin:
    #  What is the function of rstrip? https://docs.python.org/3/library/stdtypes.html#str.rstrip
    print( line.rstrip() )
