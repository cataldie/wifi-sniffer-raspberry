#!/bin/bash

function json_escape () {
    printf '%s' "$1" | python -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
}

user="root"
psw="root"
query="select * from snifferrasperry.sniffer"

OIFS="$IFS" ; IFS=$'\n' ; oset="$-" ; set -f

# Set a value:
MAC=()

while IFS="$OIFS" read -a line 
do 	
    if [[ ${line[0]} != "IP" ]] 
    then
	echo ${line[1]//:/-}
    	MAC+=(${line[1]//:/-})
    fi
done < <(mysql -u${user} -p${psw} -e "${query}")

MACstring = ""
for i in "${MAC[@]}"
do
   : 
   # do whatever on $i  #$(json_escape ${i})
   dummy=$(json_escape ${i})
   echo "dummy"${dummy}
   MACstring+=${dummy}
done

hotspotId="1"
devices="Test"
MACstring=$(json_escape ${MAC[0]})
echo " mac string "${MACstring}
postDataJson="{\"hotspotId\":\"$hotspotId\",\"devices\":\"$MACstring\"}"

response=$(curl -d ${postDataJson} -H "Content-Type: application/json" -X POST http://185.238.148.144:3000/getsnifferUpdates)
echo ${response}

if [[ ${response} == "1" ]]
then
	echo "the server response good"
fi
