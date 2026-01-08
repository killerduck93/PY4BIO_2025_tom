#!/usr/bin/env python3
# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()

seqtype = form.getvalue('moltype')

print( "Content-type:text/html\r\n\r\n")
print( "<html>")
print( "<head>")
print( "<title>moltype.py CGI Program</title>")
print( "</head>")
print( "<body>")
print( "<h1> Hello Bioinformatician </h1>" )
print( "</body>")

if seqtype:
    print("Your sequence is %s" % (seqtype))
else:
    print("<hr>")
    print(r'<form method="post" action="moltype.py" enctype="multipart/form-data">')
    print(r'What molecule type is your sequence? <input type="text" name="moltype" value="protein" /></form>')
    print("<hr>")

print("</html>")
