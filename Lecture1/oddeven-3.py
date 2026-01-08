#!/usr/bin/env python

# The 'oddeven-3' program - another version of 'oddeven'.

HOWMANY = 40

count = 0
while ( count < HOWMANY ):
    count = count + 1

    even_or_odd = lambda: "even" if ( count % 2 == 0 ) else "odd"
    print( even_or_odd() )
