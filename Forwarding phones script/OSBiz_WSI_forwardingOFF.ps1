<# Bypass one-time-run: powershell.exe -noprofile -executionpolicy bypass -file .\OSBiz_WSI_forwardingOFF.ps1 forks.csv
 WSI functions from https://wiki.unify.com/images/f/fd/OSBiz_WSI.pdf 
 *\@ braam.vanhavermaet*bkm.be
 Version: 1.0

 >> Change the global variables to fit your environment.
 !! Associated Dialing Services need to be activated on the user for controlling other users.
#>

#Set passed arguments (Needs to be the first line of the script!)
 param (
    [string]$csvpath
 )


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
$cmdLogin = "$OSBIzURL/gadgetapi?cmd=Login&gsUser=$User&gsPass=$Pass"
Invoke-WebRequest -Uri $cmdLogin | Select-Object -ExpandProperty content | Out-File WSI.xml
[xml]$xml = Get-Content WSI.xml

$SessionID = $xml.LOGIN.ID
#If error, show it.
Write-Host $xml.LOGIN.ERROR


# Import CSV file and loop through it
foreach ($line in (import-csv $csvpath)) {
    $extension = $line.extension
    $forkNum = $line.forkNum
	
	#encoding of '#' in url syntax: '%23'
	$cmdForkOFF = "$OSBizURL/gadgetapi?cmd=MkCall&callingDevice=$User&calledDirectoryNumber=*83$extension%231&gsSession=$SessionID"
	Invoke-WebRequest -Uri $cmdForkOFF | Select-Object -ExpandProperty content | Out-File WSI_fork.xml
	
	[xml]$xml = Get-Content WSI_fork.xml
	#If error, show it.
	Write-Host $xml.CSTAErrorCode
	
	#Sleep 2 sec.
	Start-Sleep -s 2
}


#Logout WSI session
$cmdLogout = "$OSBIzURL/gadgetapi?cmd=Logout&gsSession=$SessionID"
Invoke-WebRequest -Uri $cmdLogout | Select-Object -ExpandProperty content | Out-File WSI.xml


#Clean up XML files
Remove-Item WSI.xml
Remove-Item WSI_fork.xml
