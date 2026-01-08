import sys

if len(sys.argv) < 2:
        sys.stderr.write("USAGE: python3 %s < value 1 > < value 2 > ... < value n >\n" % sys.argv[0])
        sys.exit(1)

values = sys.argv[1:]

try:
    # use list comprehension to convert all strings to float
    values = [float(i) for i in values]
except:
    raise AssertionError("Not all input values can be converted to float!!!")

print( 'values = ', values )
print( 'sum = ',sum(values) ) 
