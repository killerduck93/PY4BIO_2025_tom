# check if the ratio of two integers a and b is larger than 0.5?

print( 'Enter integer a : ', end ='' )
a = int( input() )

print( 'Enter integer b : ', end ='' )
b = int( input() )

if a / b > 0.5:
    print( 'The ratio of ',a,' and ',b,' is larger than 0.5!' )
else:
    print( 'The ratio of ',a,' and ',b,' is smaller than 0.5! i.e. ',a/b )
