import sys
import os
import subprocess

class NetworkSniffer():
    def __init__(self):
        self.sniffer = []
    def getSniffer(self,nameFlag=False):
        # clear the sniffer
        self.sniffer = []
        # get the data form arp-scan
        output = subprocess.check_output("sudo arp-scan -l", shell=True)
        # convert the data to a dictonary
        curr_line = ""
        for char in output:
            if char=="\n":
                try:
                    if curr_line[0].isdigit() and  curr_line[1].isdigit() and  curr_line[2].isdigit():
                        line_array = curr_line.split()
                        #line_array is a whole line [ IP MAC Name]
                        d = {}
                        d["IP"] = line_array[0]
                        d["MAC"] = line_array[1]
                        if nameFlag:
                            d["Name"] = line_array[2]
                        self.sniffer.append(d)
                except:
                    pass
                curr_line = ""
            else:
                curr_line += char 
        return self.sniffer