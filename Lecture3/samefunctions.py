#samefunctions.py

""" This program calls two functions.
"""

from twofunctions import celsius, fahrenheit

degrees = float(input('Enter a temperature: '))
print('%.1f Fahrenheit is same as' % degrees + ' %.1f Celsius' % celsius(degrees))
print('%.1f Celsius is same as' % degrees + ' %.1f Fahrenheit' % fahrenheit(degrees))
input('Hit return when you are done')
