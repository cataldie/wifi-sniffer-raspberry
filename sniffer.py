import sys
import os
import subprocess
output = subprocess.check_output("sudo arp-scan -l", shell=True)
#print(output)
curr_line = ""
data = {}
for char in output:
    if char=="\n":
        try:
            if curr_line[0].isdigit() and  curr_line[1].isdigit():
                print(curr_line)
        except:
            pass
        curr_line = ""
    else:
        curr_line += char 