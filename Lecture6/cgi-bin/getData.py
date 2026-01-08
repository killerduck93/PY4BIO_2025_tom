#!/usr/bin/env python3
# Import modules for CGI handling
import cgi, cgitb
# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
first_name = form.getvalue('first_name')
last_name  = form.getvalue('last_name')
print("Content-type:text/html")
print("")
print("")
print("<p> Hello - Second CGI Program")
print("")
print("")
print("<p> Hello %s %s" % (first_name, last_name))
print("")
print("")
