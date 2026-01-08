#!/usr/bin/env python

# The 'oddeven' program - a (Python) program,
# which iterates four times, printing 'odd' when count
# is an odd number, and 'even' when count is an even 
# number. 

HOWMANY = 4

count = 0
while ( count < HOWMANY ):
    count = count + 1

    if ( count == 1 ):
       print( "odd" )
    elif ( count == 2 ):
       print( "even" )
    elif ( count == 3 ):
       print( "odd" )
    else: # at this point count is four.
       print( "even" )
