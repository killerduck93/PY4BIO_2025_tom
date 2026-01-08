#!/usr/bin/env python

# The 'oddeven-2' program - another version of 'oddeven'.

HOWMANY = 4

count = 0
while ( count < HOWMANY ):
    count = count + 1

    if ( count % 2 == 0 ):
       print( "even" )
    else: # count % 2 is not zero.
       print( "odd" )
