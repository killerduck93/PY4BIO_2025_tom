#!/usr/bin/env python3
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only

print("Content-Type: text/html")
print("")

arguments = cgi.FieldStorage()

print("Looping over all keys:<br>")
for i in arguments.keys(): 
    print("%s<br>" % (arguments[i].value))

print("Extracting the values per key:<br>")
print("argument a: %s<br>" % (arguments['a'].value))
print("argument b: %s<br>" % (arguments['b'].value))
print("argument c: %s<br>" % (arguments['c'].value))
print("argument bananas: %s<br>" % (arguments['bananas'].value))
