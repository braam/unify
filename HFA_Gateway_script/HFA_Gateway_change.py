#!/usr/bin/python
# coding=utf-8

'''
Example using Python to create a connection to Unify Openscape/CP HFA phones and update the Gateway Server. 
*\@ braam.vanhavermaet*bkm.be
Version: 1.0

>> Change the global variables to fit your environment.
'''

import mechanize
import cookielib
import ssl
import sys, os
from bs4 import BeautifulSoup


#>> Global variables
GWServer = ""
PHONE_IP = ""
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

def setGWServer():
	br.open("https://" + PHONE_IP + "/page.cmd?page=WEBM_Admin_Gateway")
	br.select_form(nr=0)
	br.form['reg-addr'] = GWServer
	br.submit()

	html = BeautifulSoup(br.response().read(), 'lxml')
	if checkSuccess(html):
		print "Phone @" + PHONE_IP + ": Successfully update Gateway Server."

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
	GWServer = str(sys.argv[1])
	Filepath = sys.argv[2]
else:
    print "Usage: " + os.path.basename(__file__) + " <GwServer>" + " <Filepath> \n!>>->> Bye."
    exit()

if not os.path.isfile(Filepath):
    print("Filepath {} does not exist. Exiting...".format(Filepath))
    exit()

with open(Filepath) as fp:
	cnt = 0
	for line in fp:
		PHONE_IP = line.strip()
		doLogin()
		setGWServer()

exit()
