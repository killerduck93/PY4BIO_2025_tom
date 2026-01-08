#!/usr/bin/env python3
import os

stream = os.popen('ls -1')
my_files = stream.read()
stream.close()

print(my_files)
