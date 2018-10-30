<# Bypass one-time-run: powershell.exe -noprofile -executionpolicy bypass -file .\OSBiz_WSI_presence.ps1
 WSI functions from https://wiki.unify.com/images/f/fd/OSBiz_WSI.pdf 
 *\@ braam.vanhavermaet*bkm.be
 Version: 1.0

 >> Change the global variables to fit your environment.
#>

#Set passed arguments (Needs to be the first line of the script!)
 param (
    [int]$presence,
    [string]$ptime
 )

#For now let's set ptime to tomorrow
$ptime =  (Get-Date).adddays(1)
$ptime = $ptime.ToString('yyy/MM/dd HH:mm' + "Z")


#Global variables
$OSBizURL = "https://10.242.2.200:8802/cgi-bin"
$User = "8867"
$Pass = "xxxxxx"


# IGNORE SELF SINGED CERTIFICATES.
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

# Login and get SessionID
$url = "$OSBIzURL/gadgetapi?cmd=Login&gsUser=$User&gsPass=$Pass"
Invoke-WebRequest -Uri $url | Select-Object -ExpandProperty content | Out-File WSI.xml
[xml]$xml = Get-Content WSI.xml

$SessionID = $xml.LOGIN.ID
Write-Host $xml.LOGIN.ERROR


# Set presence with numerical state
# NUM   STATE
# ---   -----
# 1     Office
# 2     Meeting
# 3     Sick
# 4     Break
# 5     GoneOut
# 6     Holiday
# 7     Lunch
# 8     Home
# 9     DND
#$urlPresence = "$OSBizURL/gadgetapi?cmd=SetPresence&user=$User&presence=$presence&ptime=$ptime&gsSession=$SessionID"
$urlPresence = "$OSBizURL/gadgetapi?cmd=SetPresence&user=$User&presence=$presence&gsSession=$SessionID"
Invoke-WebRequest -Uri $urlPresence | Select-Object -ExpandProperty content | Out-File WSI_presence.xml
[xml]$xml = Get-Content WSI_presence.xml

Write-Host $xml.ERROR.REASON


#Clean up XML files
Remove-Item WSI.xml
Remove-Item WSI_presence.xml