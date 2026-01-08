# firstfunctions.py

""" 
This program contains two functions that convert C into F and F into C
"""

def celsius (temperature) :
    return (temperature - 32)*5/9

def fahrenheit (temperature) :
   return (temperature*9/5 + 32)

degrees = float(input('Enter a temperature: '))

print('%.1f Fahrenheit is same as' % degrees + ' %.1f Celsius' % celsius(degrees))
print('%.1f Celsius is same as' % degrees + ' %.1f Fahrenheit' % fahrenheit(degrees))
input('Hit return when you are done')
