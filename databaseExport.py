import sys,json
import os
from datetime import datetime

from classes.dbClass import DbClassTable

import pycurl
from io import BytesIO 

import urllib

dbConfig = {
    "host" : "localhost",
    "user" : "root",
    "psw"  : "root"
}
sqltxt = """
        IP   VARCHAR(120),
        MAC  VARCHAR(120),
        time DATETIME,
	uploaded INT
        """
localDBTableSniffer = DbClassTable("snifferrasperry","data/","snifferrasperry","sniffer",sqltxt,dbConfig["host"],dbConfig["user"],dbConfig["psw"])

data = localDBTableSniffer.selectTablePart("*"," WHERE uploaded=0") #
convertedData = []
print(data)
for i in range(len(data)):
    appo = {}
    #print(data[i])
    appo["MAC"]=data[i][1]
    appo["date"]=data[i][2].strftime('%Y-%m-%d %H:%M:%S')
    appo["id"]=int(data[i][4])
    convertedData.append(appo)
if len(convertedData)>0:
    jsonString = json.dumps(convertedData)
    print(jsonString)

    post_params = [
        ('hotspotId',1),
        ('devices',jsonString),
    ]
    resp_data = urllib.urlencode(post_params)

    url = "http://"+sys.argv[1]+"/getsnifferUpdates"
    b_obj = BytesIO() 
    c = pycurl.Curl()
    c.setopt(c.WRITEDATA, b_obj)
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, resp_data)
    c.perform()
    c.getinfo(pycurl.RESPONSE_CODE)
    get_body = b_obj.getvalue()
    response = int(get_body.decode('utf8'))

    print("response ",response)
    if response==1:
        print("done")
        for i in range(len(convertedData)):
            print(convertedData[i]["id"])
            localDBTableSniffer.updateTable(convertedData[i]["id"],[1],"uploaded=%s")

    else:
        print("error")