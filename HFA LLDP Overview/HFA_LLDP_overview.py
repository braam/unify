#!/usr/bin/python
# coding=utf-8

'''
Example using Python to create a connection to Unify Openscape/CP HFA phones and get LLDP switch information with internal number overiew. 
*\@ braam.vanhavermaet*bkm.be
Version: 1.0

>> Change the global variables to fit your environment.
'''

import mechanize
import cookielib
import ssl
import sys, os
import pandas as pd
from bs4 import BeautifulSoup


#>> Global variables
PASSWORD = "123456"
lldp_list = []

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#<< end Global variables


#>> Hacks
# Disable security warnings, by self signed certificates using requests.
ssl._create_default_https_context = ssl._create_unverified_context
#<< end Hacks


#>> Functions
def doLogin(PHONE_IP):
	br.open("https://" + PHONE_IP + "/page.cmd?page=WEBMp_Admin_Login")
	br.select_form(nr=0)
	br.form['AdminPassword'] = PASSWORD
	br.submit()

	#html = br.response().read()
	#Need a way for checking successful login...

def getSubscriberNumber(PHONE_IP):
	br.open("https://" + PHONE_IP + "/page.cmd?page=WEBM_Admin_Gateway")
	html = BeautifulSoup(br.response().read(), 'lxml')

	return html.find('input', {'name': 'reg-number'}).get('value')

def getLLDPinfo(PHONE_IP):
	doLogin(PHONE_IP)
	internalNumber = getSubscriberNumber(PHONE_IP)

	br.open("https://" + PHONE_IP + "/page.cmd?page=WEBM_Admin_LLDP_TLV")
	html = BeautifulSoup(br.response().read(), 'lxml')
	for table_row in html.findAll('tr')[2::3]: #we only need the 2 till third row and the second cell, this contains the received TLVS
		cells = table_row.findAll('td')
		received_td = cells[1].text.replace("\n", " ").strip() #remove newline chars and to much spaces.
		received_td_list = received_td.split()
		switchName = received_td_list[16]
		switchPort = received_td_list[27]
		
	lldp_record = [internalNumber, switchName, switchPort, PHONE_IP]	
	lldp_list.append(lldp_record)

def exportToCSV():
	pd.DataFrame(lldp_list).to_csv("LLDP_overview_HFA.csv",header=["Callno", "SwitchName", "SwitchPort", "Phone IP"],index=False)

#<< end Functions


'''
 ** @@MAIN@@
'''
#Retrieve Filepath from argument.
if len(sys.argv) >1:
	Filepath = sys.argv[1]
else:
    print "Usage: " + os.path.basename(__file__) + " <Filepath> \n!>>->> Bye."
    exit()

if not os.path.isfile(Filepath):
    print("Filepath {} does not exist. Exiting...".format(Filepath))
    exit()

with open(Filepath) as fp:
	cnt = 0
	for line in fp:
		PHONE_IP = line.strip()
		getLLDPinfo(PHONE_IP)

exportToCSV()

exit()
