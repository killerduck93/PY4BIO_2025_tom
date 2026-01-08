import sys
import random

something_important = random.choice([True, False])

if something_important == False:
    print( "Oh no, something is wrong!!!")
    sys.exit()
else:
    while True: 
        print("Live is fine...")
