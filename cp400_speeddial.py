#!/usr/bin/python
# coding=utf-8

'''
Example using Python to create a connection to Unify Openscape CP 400 Phones. 
*\@ braam.vanhavermaet*bkm.be
Version: 1.0

>> Change the global variables to fit your environment.

++ Don't forget to first let the systemclient come online without credentials. Otherwise it won't work! (reg-number needed for password) ++
'''

import mechanize
import cookielib
import ssl
import sys, os
from bs4 import BeautifulSoup


#>> Global variables
UCServer = ""
RegPassword = ""
PHONE_IP = "10.243.24.10"
PASSWORD = "123456"

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
def doLogin():
	br.open("https://" + PHONE_IP + "/page.cmd?page=WEBMp_Admin_Login")
	br.select_form(nr=0)
	br.form['AdminPassword'] = PASSWORD
	br.submit()

	#html = br.response().read()
	#Need a way for checking successful login...

def setUCServer():
	br.open("https://" + PHONE_IP + "/page.cmd?page=WEBM_Admin_WSI")
	br.select_form(nr=0)
	br.form['wsi-server-address'] = UCServer
	br.submit()

	html = BeautifulSoup(br.response().read(), 'lxml')
	if checkSuccess(html):
		print "UCServer successfully set."

def setHFA_Auth():
	# First get extension
	br.open("https://" + PHONE_IP + "/page.cmd?page=WEBM_Admin_Gateway")
	r = BeautifulSoup(br.response().read(), 'lxml')
	ext = r.find('input', attrs={'name':'reg-number'})["value"]

        br.select_form(nr=0)
        br.form['reg-password'] = RegPassword + ext
        br.submit()

        html = BeautifulSoup(br.response().read(), 'lxml')
	if checkSuccess(html):
		print "HFA Authentication successfully set for: " + ext

def checkSuccess(html):
	try:
		html.find_all('div', attrs={'class':'success'})
		return True
	except:
		pass

#<< end Functions


'''
 ** @@MAIN@@
'''
#Retrieve UCServer from argument.
if len(sys.argv) >2:
        UCServer = str(sys.argv[1])
	RegPassword = str(sys.argv[2])
else:
        print "Usage: " + os.path.basename(__file__) + " <UCServer-IP> <RegPassword>" + "\n!>>->> Bye."
        exit()

doLogin()
setUCServer()
setHFA_Auth()

exit()
