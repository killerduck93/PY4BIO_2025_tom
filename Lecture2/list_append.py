data = []   # start with empty list

# loop to get numbers
number = input( "Enter a number (<ENTER> to quit) >> " )

while number != "":
    x = float(number)
    data.append( x )
    number = input( "Enter a number (<ENTER> to quit) >> " )

print( 'The list contains following numbers: ', data )


