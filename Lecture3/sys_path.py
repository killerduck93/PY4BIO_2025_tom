import sys
import os

cwd = os.getcwd()

print( 'BEFORE append...' )
print( str.join('\n', sys.path ) )

print( 'AFTER append...' )
# Add directories as usual, with append!
sys.path.append( cwd )
print( str.join('\n', sys.path ) )
