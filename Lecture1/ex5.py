'''
check for all tuples in [(3,2),(10,5),(1,-1)] if the square of the  first number can be divided by the second without rest?
'''

list_of_tuples = [(3,2),(10,5),(1,-1)]

for tuple in list_of_tuples:
    if tuple[ 0 ]**2 % tuple[ 1 ] == 0:
        print( tuple )
