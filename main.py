import sys
import os
from datetime import datetime

from classes.sniffer import NetworkSniffer
from classes.dbClass import DbClassTable
from classes.setInterval import setInterval

#set up the classes
sniffer = NetworkSniffer()
dbConfig = {
    "host" : "localhost",
    "user" : "root",
    "psw"  : "root"
}
sqltxt = """
        IP   VARCHAR(120),
        MAC  VARCHAR(120),
        time DATETIME 
        """
localDBTableSniffer = DbClassTable("snifferrasperry","data/","snifferrasperry","sniffer",sqltxt,dbConfig["host"],dbConfig["user"],dbConfig["psw"])

def mainFn():
    #check the network
    sniffer.getSniffer()
    print(sniffer.sniffer)
    #save to local db
    for s in sniffer.sniffer:
        current_time = datetime.now()
        data = [
            s["IP"],
            s["MAC"],
            current_time
        ]
        sqltxt ="""
            (IP ,MAC ,time)
            VALUES
            (%s ,%s  ,%s)
            """
        localDBTableSniffer.insertRow(data,sqltxt)

if __name__ == "__main__":
    try:
        # run mainFn every "interval" second and end at "end"
        print("Running the sniffer every "+str(sys.argv[1])+"s until "+str(sys.argv[2])+"s")
        inter=setInterval(float(sys.argv[1]),mainFn,float(sys.argv[2]))
    except:
        try:
            print("Running the sniffer every "+str(sys.argv[1])+"s endless ")
            # run mainFn every "interval" second and with no end
            inter=setInterval(float(sys.argv[1]),mainFn)
        except:
            interval = 5
            end = 25
            print("Running the sniffer every "+str(interval)+"s until "+str(end)+"s")
            inter=setInterval(interval,mainFn,end)