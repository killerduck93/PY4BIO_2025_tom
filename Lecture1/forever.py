#!/usr/bin/env python

# The 'forever' program - a (Python) program,
# which does not stop until someone presses Ctrl-C.

import time

while ( True ):

    # Since Python 3.3 print() supports the keyword argument "flush" disabling output buffering.
    # Useful when running scripts within the IDE
    
    print( "Welcome to the Wonderful World of Bioinformatics!", flush=True )
    time.sleep(1)
