#!/usr/bin/env python3
import subprocess

result = subprocess.check_output("ls -l", shell=True)
result = str(result, 'utf-8')

print(result)
