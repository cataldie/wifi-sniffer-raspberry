import sys
import os
import subprocess
import time
import signal
import psutil
import shutil
import thread
import csv

class NetworkSniffer():
    def __init__(self):
        self.sniffer = []
        self.flag = False
        self.device = ""
        self.folderName = "data/"
        self.pathToFile = "data/test"
        self.delay = 1.0
        self.duration = 50
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
    def checkIfMonitorIsSupported(self):
        print("Checking if the device supports monitor mode")
        try:
            output = subprocess.check_output('iw list | grep "Supported interface modes" -A 7', shell=True)
            index = 0
            for s in output:
                if s=="m":
                    if output[index:index+7]=="monitor":
                        print("The device supports the monitor mode")
                        return True
                index += 1
            print("The device does not support monitor mode")
            return False
        except:
            print("The device does not support monitor mode")
            return False
    def enableMonitorMode(self):
        subprocess.check_output('sudo airmon-ng start '+self.device, shell=True)
    def checkIfMonitorModeIsOn(self):
            output = subprocess.check_output('ifconfig  '+self.device+'mon', shell=True)
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
    def getSniffer(self):
        self.subProcessAirodump()
        self.fetchTheData()
        
    def subProcessAirodump(self):
        print("seraching...")
        # clear the sniffer and the folder
        self.sniffer = []
        if (os.path.exists(self.folderName) ):
            shutil.rmtree(self.folderName)
            os.mkdir(self.folderName)
        else:
            os.mkdir(self.folderName)
        
        timeout = int(self.duration / self.delay)
        cmd = ["sudo", "airodump-ng" ,self.device+"mon", "--write" , self.pathToFile]
        popen = subprocess.Popen(cmd,
                stderr=subprocess.STDOUT,  # Merge stdout and stderr
                stdout=subprocess.PIPE)
        #while the process is still executing and we haven't timed-out yet
        while popen.poll() is None and timeout > 0:
            #do other things too if necessary e.g. print, check resources, etc.
            time.sleep(self.delay)
            #print(timeout)
            timeout -= self.delay
        p = psutil.Process(popen.pid)
        child_pid = p.children(recursive=True)
        for pid in child_pid:
            os.kill(pid.pid, signal.SIGTERM)
        print("seraching just ended")
    def fetchTheData(self):
        print("Fetching the data")
        fullFileName = self.pathToFile+"-01.csv"
        #print(fullFileName)
        initDone = False
        with open(fullFileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if initDone and len(row)>0:
                    #print(row)
                    d = {}
                    d["MAC"]                = row[0]
                    d["first-time-seen"]    = row[1]
                    d["last-time-seen"]     = row[2]
                    d["power"]              = row[3]
                    d["packets"]            = row[4]
                    if row[5]==' (not associated) ':
                        d["status"] = 0
                    else:
                        d["status"] = 1

                    #print(d)
                    self.sniffer.append(d)
                if len(row)>0 and row[0]=="Station MAC":
                    initDone = True
                    #print(row)

            print('Processed '+str(line_count)+' lines.')