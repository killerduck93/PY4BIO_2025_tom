#!/usr/bin/env python3

# Import modules for CGI handling
import cgi
import cgitb # Optional; for debugging only

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
f_name = form.getvalue('f_name')
l_name = form.getvalue('l_name')
phone  = form.getvalue('phone')

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Say Hello</title>")
print("</head>")
print("<body")
print("<h2>Say Hello</h2>")
print("Hi %s!<p>" % (f_name))
print("Your details:<p>")
print("Name: %s %s<br>" % (f_name, l_name))
print("Phone number: %s" % (phone))
print("</body>")
print("</html>")

