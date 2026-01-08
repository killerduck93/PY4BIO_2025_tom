# check which element of [1,5,-1,8,7] are also inside [8,7,10,5,0,0]

list_1 = [1,5,-1,8,7]
list_2 = [8,7,10,5,0,0]

print( 'list_1 : ', list_1 )
print( 'list_2 : ', list_2 )

for item in list_1:
    if item in list_2:
        print( item, ' exists in ',list_2 )

