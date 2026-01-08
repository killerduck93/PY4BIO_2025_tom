#!/usr/bin/env python

# The 'fivetimes' program 
# a (Python) program,
# which stops after five iterations.

HOWMANY = 5
count = 0
while ( True ):
    count = count + 1

    print( "Welcome to the Wonderful World of Bioinformatics!" )

    if ( count == HOWMANY ):
       break  # break here
