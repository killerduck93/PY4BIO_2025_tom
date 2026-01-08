#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:41:06 2019

@author: piete
"""

# import cgi module
import cgi 

# get form data using the FieldStorage method, which returns an object
form = cgi.FieldStorage() 

# Get data from fields
user_name = form.getvalue('name')
user_city  = form.getvalue('city')

print("Content-Type: text/html")
print()

print("Welcome %s, from %s" % (user_name,user_city))