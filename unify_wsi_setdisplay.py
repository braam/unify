#!/usr/bin/python
# coding=utf-8

'''
Example using Python to create a WSI connection to Unify Openscape Business systems.
WSI functions from https://wiki.unify.com/images/f/fd/OSBiz_WSI.pdf 
*\@ braam.vanhavermaet*bkm.be
Version: 1.0

>> Change the global variables to fit your environment.
'''

import sys, os
import requests, socket
import xml.etree.ElementTree as ET
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urlparse import urlparse


#>> Global variables
OSbizURL = "https://10.242.2.200:8802/cgi-bin/" #Include trailing slash
User = "8867"
Pass = "xxxxxx"
sessionID = ""
displayText = ""
#<< end Global variables


## ** HACKS
#Disable securtiy warnings, by self signed certificates using requests.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
## HACKS **
 

'''
 ** Functions
'''
def checkWSI():
    url = urlparse(OSbizURL)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3) #timeout to check in seconds.
    result = sock.connect_ex((url.hostname,url.port))
    if result == 0:
        return True
    else:
        return False


def getWSI(cmd):
    page = requests.get(OSbizURL+"gadgetapi?cmd="+cmd, verify=False)
    return page.content


def doLogin():
    global sessionID
    xml = getWSI("Login&gsUser="+User+"&gsPass="+Pass)
    root = ET.fromstring(xml)
    sessionID = root[0].text #loginID is next to root tag.
    if sessionID == 0:
        print "Login failed, please check your credentials.. \n!>>->> Bye."
    else: 
        pass #successful, sessionID already set.
	
	
def doLogout():
    global sessionID
    xml = getWSI("Logout&gsSession="+sessionID)


def setDisplayText(ext): #Max 24 chars on Openstage 40T.
    global sessionID
    global displayText
    xml = getWSI("SetDisplay&device="+ext+"&contentsOfDisplay="+displayText+"&gsSession="+sessionID)
    root = ET.fromstring(xml)
    if root == "<SetDisplay/>":
        print "Succesfully setDisplayText."
    else:
        print "Error setting text. " + root


def clearDisplay(ext):
    global sessionID
    xml = getWSI("ClearDisplay&device="+ext+"&gsSession="+sessionID)
    root = ET.fromstring(xml)
    if root == "<ClearDisplay/>":
        print "Succesfully cleared display."
    else:
        print "Error clearing display. " + root
    

'''
 ** @@MAIN@@
'''
#Retrieve displayText from argument.
if len(sys.argv) >1:
        displayText = str(sys.argv[1])
else:
        print "Usage: " + os.path.basename(__file__) + " <text>" + "\n!>>->> Bye."
        exit()

if checkWSI(): #Check first WSI connection on port 8802, then proceed with login.
    doLogin()
    setDisplayText("8867")

else:
    print "ERROR, WSI connection not possible to: " + OSbizURL
    exit()

