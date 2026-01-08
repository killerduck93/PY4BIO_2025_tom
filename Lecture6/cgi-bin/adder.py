#!/usr/bin/env python3
import cgi;
import cgitb
cgitb.enable()

def print_header():
    print("""Content-type: text/html\n
    <!DOCTYPE html>
    <html>
    <body>""")

def print_close():
    print("""</body>
    </html>""")

def display_data(param1, param2):
    print_header()
    print("<p>Param1 = " + param1 + "</p>")
    print("<p>Param2 = " + param2 + "</p>")
    print_close()

def display_error():
    print_header()
    print("<p>An Error occurred parsing the parameters passed to this script.</p>")
    print("<p>Try something like:</p>")
    print(r'<p><strong>http://localhost/SimpleCgi.py?param1=1&param2=2</strong></p>')
    print_close()

def main():
    form = cgi.FieldStorage()
    if ("param1") and ("param2") in form.keys():
        display_data(form["param1"].value, form["param2"].value)
    else:
        display_error()

main()
