#!/usr/bin/env python3

f_name = "Pieter"
l_name = "De Bleser"
phone  = 3306

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

