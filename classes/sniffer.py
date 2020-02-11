import sys
import os
import subprocess
import time
import shutil

class NetworkSniffer():
    def __init__(self):
        self.sniffer = []
        self.flag = False
    def getSnifferV1(self,nameFlag=False):
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
    def checkIfMonitorIsSupported(self,device):
        print("Checking is the device supports monitor mode")
        output = subprocess.check_output('iw list | grep "Supported interface modes" -A 7', shell=True)
        index = 0
        for s in output:
            if s=="m":
                if output[index:index+7]=="monitor":
                    print("The device supports the monitor mode")
                    return True
            index += 1
        return False
    def enableMonitorMode(self,device):
        subprocess.check_output('sudo airmon-ng start '+device, shell=True)
    def checkIfMonitorModeIsOn(self,device):
            output = subprocess.check_output('ifconfig  '+device+'mon', shell=True)
            index = 0
            for s in output:
                if s=="\n":
                    return True
                if s=="e":
                    if output[index:index+5]=="error":
                        print("The device is not in monitor mode")
                        return False
                index += 1
            return True
    def getSniffer(self,device):
        # clear the sniffer and the folder
        folderName = "data/"
        self.sniffer = []
        if (os.path.exists(folderName) ):
            shutil.rmtree(folderName)
            os.mkdir(folderName)
        else:
            os.mkdir(folderName)
        
        x = 5#some amount of seconds
        delay = 1.0
        timeout = int(x / delay)
        
        popen = subprocess.Popen(['sudo airodump-ng '+ device+'mon --write data/test.csv'])
        #while the process is still executing and we haven't timed-out yet
        while popen.poll() is None and timeout > 0:
            #do other things too if necessary e.g. print, check resources, etc.
            time.sleep(delay)
            print(timeout)
            timeout -= delay