#!/usr/bin/python
# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
if form.getvalue('textcontent'):
   text_content = form.getvalue('textcontent')
else:
   text_content = "Not entered"

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Text Area CGI Program</title>")
print("</head>")
print("<body>")
print("<h3> Entered Text Content is: <br>%s</h3>" % text_content)
print("</body>")
print("</html>")
