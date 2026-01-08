import sys

if len(sys.argv) != 2:
        sys.stderr.write("USAGE: python3 %s < value >\n" % sys.argv[0])
        sys.exit(1)

value = sys.argv[1]

try:
    value = float(value)
except:
    raise AssertionError("Couldn't make the input a float!")

print(value + 25)
