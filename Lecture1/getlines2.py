#!/usr/bin/env python

# The 'getlines' program which processes lines.

import fileinput

for line in fileinput.input():
    print( line.rstrip()  )
