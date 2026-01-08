# print all word in ['Oranges', 'Bananas', 'Cucumbers', 'Apples'] starting with an O or A ?

list =  ['Oranges', 'Bananas', 'Cucumbers', 'Apples'] 

# using 'startswith'
for fruit in list:
    if fruit.startswith('O') or fruit.startswith('A'):
        print( fruit )

# using a regular expression
import re
for fruit in list: 
    if re.match( "^[AO]", fruit ):
        print( fruit )
