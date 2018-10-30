@echo off
setlocal EnableDelayedExpansion

:: ********************************************************************************************
:: *              Script for creating the Unify DHCP Options                                  *
:: * FOR MORE INFO                                                                            *
:: * http://wiki.unify.com/wiki/VLAN_ID_Discovery_over_DHCP                                   *
:: * >>> BKM  (braam.vanhavermaet*bkm.be                                                      *
:: ********************************************************************************************

netsh Dhcp Server show Server | find "=" > NUL || goto noserver
cls

echo **************************************************************************
echo *                                                                        *
echo * This script add the Unify DHCP Options to your local DHCP Server *
echo * a backup copy will be saved to the local directory                     *
echo * press CTRL-C to cancel or any other key to continue                    *
echo *                                                                        *
echo **************************************************************************
pause > NUL

set /p DLS="Enter DLS Server: "
set /p VLAN="Enter VLAN ID: "
call :ConvertDecToHex %VLAN% HexVLAN

netsh Dhcp Server Dump > dhcp_server_before_unify_script.bak

netsh Dhcp Server Add Class "OptiIpPhone" "Unify OptiIpPhone VoIP Options" 4f707469497050686f6e65 1 b
netsh Dhcp Server Add Optiondef 1 "HardwareCode" STRING 0 vendor="OptiIpPhone" comment="Siemens" Siemens
netsh Dhcp Server Add Optiondef 2 "VLAN ID" BYTE 1 vendor="OptiIpPhone" comment="VoIP VLAN ID" 0 0 0 %HexVLAN%
netsh Dhcp Server Add Optiondef 3 "DLS Server" STRING 0 vendor="OptiIpPhone" comment="DLS Server" sdlp://%DLS%:18443


exit


:ConvertDecToHex 
set LOOKUP=0123456789abcdef
set HEXSTR=
set PREFIX=

if "%1" EQU "" (
 set "%2=0"
 Goto:eof
 )
 set /a A=%1 || exit /b 1
 if !A! LSS 0 set /a A=0xfffffff + !A! + 1 & set PREFIX=f
 :loop
 set /a B=!A! %% 16 & set /a A=!A! / 16
 set HEXSTR=!LOOKUP:~%B%,1!%HEXSTR%
 if %A% GTR 0 Goto :loop
 set "%2=%PREFIX%%HEXSTR%"
 Goto:eof


:noserver
echo *******************
echo **** E R R O R ****
echo *******************
echo.
echo Please check your DHCP Server
echo *****************************
echo this script is only for Windows Server 2003 and above
echo with running Microsoft DHCP Server
echo Try any of the listed Server below
for /F "delims=: tokens=2" %%d in ('ipconfig /all^|findstr /I /C:"DHCP-Server"') do @echo %%d
echo Press any key to exit
pause > NUL
exit